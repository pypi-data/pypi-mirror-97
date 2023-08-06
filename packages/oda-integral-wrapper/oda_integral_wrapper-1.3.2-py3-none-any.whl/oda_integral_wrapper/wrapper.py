import numpy as np
from astropy.io import fits
import oda_api.api
import copy
import matplotlib
from astropy import units as u
from astroquery.simbad import Simbad
import astropy.wcs as wcs
import matplotlib.pylab as plt
from astropy.coordinates import SkyCoord
from astropy import table
import requests

__author__ = "Carlo Ferrigno"

__all__ = ['INTEGRALwrapper']

# Hopefully, this is stable enough
oda_public_host = 'https://www.astro.unige.ch/cdci/astrooda/dispatch-data'


from autologging import logged

@logged
class INTEGRALwrapper(object):

    # we assume that:
    # - product is compatible with oda_api
    # - the list of science windows can be ordered

    def __init__(self, host_type='production'):

        self.product = 'None'

        instrument = 'isgri'
        # if('jemx' in product):
        #     instrument='jemx'

        host = oda_public_host

        if host_type == 'staging-1-3':
            host = 'http://in.internal.odahub.io/staging-1-3/dispatcher'

        if host_type == 'staging' or host_type == 'staging-1-2':
            host = 'http://cdcihn.isdc.unige.ch/staging-1.2/dispatcher'

        if host_type == 'test':
            host = 'http://cdciweb01.isdc.unige.ch:8084/astrooda'

        try:
            self.disp = oda_api.api.DispatcherAPI(url=host)
            self.disp.get_instrument_description(instrument)
        except:
            try:
                self.disp = oda_api.api.DispatcherAPI(url=host)
                self.disp.get_instrument_description(instrument)
            except:
                raise ConnectionError

    def long_scw_list_call(self, in_total_scw_list, s_max=50, wait=True, **arguments):
        import time
        total_scw_list = sorted(in_total_scw_list)

        self.product = arguments['product']

        if len(total_scw_list) > s_max:
            ind_max = int(len(total_scw_list) / s_max)
            scw_lists = [total_scw_list[i * s_max:(i + 1) * s_max] for i in range(ind_max)]
            if ind_max * s_max < len(total_scw_list):
                scw_lists.append(total_scw_list[ind_max * s_max:])
        else:
            scw_lists = [total_scw_list]

        self.all_data = []
        tot_num = 0

        disp_by_call = {}
        data_by_call = {}
        n_poll = 0
        while True:
            for n_call, scw_list in enumerate(scw_lists):
                if n_poll == 0:
                    self.__log.info("At call %d we elaborate %d scw" % (n_call, len(scw_list)))
                    tot_num += len(scw_list)
                #     silent = False
                # else:
                #     if n_poll % 10 == 0:
                #         silent = False
                #     else:
                #         silent = True

                ys = "%06d" % n_call

                if ys not in disp_by_call:
                    disp_by_call[ys] = oda_api.api.DispatcherAPI(url=self.disp.url, wait=False)

                _disp = disp_by_call[ys]

                data = data_by_call.get(ys, None)

                if data is None or not _disp.is_failed():
                    if not _disp.is_submitted:
                        scw_list_str = ",".join([s for s in sorted(set(scw_list))])
                        data = _disp.get_product(scw_list=scw_list_str, **arguments)
                    else:
                        _disp.poll()

                    data_by_call[ys] = data

                    if not _disp.is_complete:
                        continue
                    else:
                        data_by_call[ys] = _disp.get_product(scw_list=scw_list_str, **arguments)


            n_complete = len([call for call, _disp in disp_by_call.items() if _disp.is_complete])
            self.__log.debug(f"complete {n_complete} / {len(disp_by_call)}")
            if n_complete == len(disp_by_call):
                self.__log.info("done!")
                break
            self.__log.debug("not done")
            n_poll += 1
            if not wait:
                return None
            time.sleep(5)

        loc_keys = data_by_call.keys()

        for kk in sorted(loc_keys):
            self.__log.debug(kk)
            self.all_data.append(data_by_call[kk])

        self.__log.debug(len(total_scw_list), tot_num)

        if 'spectrum' in self.product:
            return self.sum_spectra()

        if 'lc' in self.product:
            return self.stitch_lc()

        if 'ima' in self.product:
            additional_paramters = {}
            for key in ['detection_threshold', 'projection']:
                if key in arguments.keys():
                    additional_paramters.update({key: arguments[key]})
            #try:
            ret_value = self.combine_mosaics(**additional_paramters)
            #except:
            #    self.__log.warning("did not manage to combine mosaics, returning the full list of mosaics")
            #    ret_value = self.all_data

            return ret_value

        return self.all_data

    def combine_mosaics(self, projection='first', detection_threshold=6.):
        import copy
        summed_data = copy.deepcopy(self.all_data[0])
        import mosaic
        from astropy import table
        import oda_api.data_products

        list_hdus = [dd.mosaic_image_0_mosaic.to_fits_hdu_list() for dd in self.all_data]
        summed_mosaic = mosaic.mosaic_list(list_hdus, pixels=projection, mock=False)

        sources = [dd.dispatcher_catalog_1.table[np.logical_and(
            dd.dispatcher_catalog_1.table['significance'] >= detection_threshold,
            dd.dispatcher_catalog_1.table['ISGRI_FLAG'] > 0)]
                   for dd in self.all_data]
        # If there are new sources, the tyoe is 'object', we need to replace it
        for ss in sources:
            ss.replace_column('ERR_RAD', ss.columns['ERR_RAD'].astype(np.float64))
            # print(ss['ERR_RAD'].dtype)

        # We stack the table but take just the first occurrence of each source
        stacked_table_known = table.unique(table.vstack(sources, join_type='exact'), keys='src_names')

        new_sources_list = [dd.dispatcher_catalog_1.table[dd.dispatcher_catalog_1.table['ISGRI_FLAG'] == 0] for dd in
                            self.all_data]
        n_new = 1
        for ss in new_sources_list:
            if len(ss) == 0:
                new_sources_list.remove(ss)
                continue
            for row in ss:
                row['src_names'] = 'NEW_%02d' % n_new
                row['ERR_RAD'] = -1
                n_new += 1
            ss.replace_column('ERR_RAD', ss.columns['ERR_RAD'].astype(np.float64))
            # print(ss['ERR_RAD'].dtype)

        stacked_table = table.unique(table.vstack(new_sources_list + [stacked_table_known], join_type='exact'),
                                     keys='src_names')

        idx_f, idx_s = find_duplicates(stacked_table)

        # TODO tests with duplicates

        if idx_f is None:
            self.__log.info("No duplicates in final catalog")
        else:
            self.__log.info("Removing %d duplicates" % len(idx_f))
            stacked_table.remove_rows(idx_s)

        summed_data.dispatcher_catalog_1.table = stacked_table
        summed_data.mosaic_image_0_mosaic.data_unit = summed_data.mosaic_image_0_mosaic.data_unit[0:1] + \
                                                      [oda_api.data_products.NumpyDataUnit.from_fits_hdu(hh) for hh in
                                                       summed_mosaic.to_hdu_list()[1:]
                                                       if hh.header['IMATYPE'] != 'NIMAGE']

        self.summed_data=summed_data

        self.compute_fluxes()

        return summed_data

    def compute_fluxes(self):

        if not hasattr(self, 'summed_data'):
            raise RuntimeWarning('No summed mosaic, no computation of fluxes')

        stacked_table = self.summed_data.dispatcher_catalog_1.table
        cat_for_image = INTEGRALwrapper.get_source_list_from_table(stacked_table)
        import oda_integral_wrapper.fitimage as fitimage
        # import importlib
        # importlib.reload(fitimage)
        fit_image = fitimage.FitMosaicSources(self.summed_data.mosaic_image_0_mosaic.data_unit, cat_for_image)
        fitted_fluxes = fit_image.get_fluxes()
        stacked_table['FLUX'] = fitted_fluxes[0][1]
        stacked_table['FLUX_ERR'] = fitted_fluxes[0][2]
        stacked_table['significance'] = fitted_fluxes[0][1] / np.array(fitted_fluxes[0][2])

        self.summed_data.dispatcher_catalog_1.table = stacked_table

    def write_ds9_region_file(self, filename='ds9.reg', color='green', new_color='white'):

        if not hasattr(self, 'summed_data'):
            raise RuntimeWarning('No summed mosaic, ds9 region file not written')


        ff = open(filename, 'w')
        out_str = 'global move=0\nglobal color=%s\n' % color
        for row in  self.summed_data.dispatcher_catalog_1.table:
            out_str += 'fk5;point(%f, %f)  # point=circle text={%s}' % (row['ra'], row['dec'], row['src_names'])
            if 'NEW' in row['src_names']:
                out_str += ' color=%s\n' % new_color
            else:
                out_str += '\n'
        ff.write(out_str)
        ff.close()


    @staticmethod
    def get_source_list_from_table(my_table):
        src_dict = []
        for row in my_table:
            src_dict.append((row['src_names'], (row['ra'], row['dec'])))
        return src_dict



    def get_sources(self):
        sources = set()

        # It works both on collection and single instance
        try:
            for data in self.all_data:
                # print(set([l.meta_data['src_name'] for l in data._p_list]))
                sources = sources.union(set([l.meta_data['src_name'] for l in data._p_list]))
        except:
            sources = sources.union(set([l.meta_data['src_name'] for l in self.all_data._p_list]))

        return sources

    def stitch_lc(self):

        combined_data = copy.deepcopy(self.all_data[0])

        if not 'lc' in combined_data._p_list[0].name:
            raise ValueError('This is not a light curve and you try to stitch them')

        sources = self.get_sources()

        # gets indexes of source and lc in combined data
        for source in sources:
            for j, dd in enumerate(combined_data._p_list):
                if dd.meta_data['src_name'] == source:
                    IND_src_combined = j
                    for ii, du in enumerate(dd.data_unit):
                        if 'LC' in du.name:
                            IND_lc_combined = ii

            for data in self.all_data[1:]:
                for dd in data._p_list:
                    if dd.meta_data['src_name'] == source:
                        print('Source ' + source)

                        hdu = combined_data._p_list[IND_src_combined].data_unit[IND_lc_combined].to_fits_hdu()

                        for du in dd.data_unit:
                            if 'LC' in du.name:

                                self.__log.info('Original LC size %s' % hdu.data.shape[0])

                                new_data = hdu.data.copy()
                                new_data.resize(((hdu.data.shape[0] + du.data.shape[0])))

                                for i, col in enumerate(hdu.columns):
                                    # print(col)
                                    new_data[col.name] = np.concatenate((hdu.data[col.name], du.data[col.name]))

                                hdu.data = new_data.copy()

                                hdu.header['ONTIME'] += du.header['ONTIME']
                                try:
                                    hdu.header['EXPOSURE'] += du.header['EXPOSURE']
                                    hdu.header['EXP_SRC'] += du.header['EXP_SRC']
                                except:
                                    pass

                                if du.header['TSTART'] < hdu.header['TSTART']:
                                    hdu.header['TSTART'] = du.header['TSTART']

                                if du.header['TSTOP'] > hdu.header['TSTOP']:
                                    hdu.header['TSTOP'] = du.header['TSTOP']

                                try:
                                    if du.header['TLAST'] > hdu.header['TLAST']:
                                        hdu.header['TLAST'] = du.header['TLAST']
                                except:
                                    pass

                                try:
                                    hdu.header['TELAPSE'] = hdu.header['TSTOP'] - hdu.header['TSTART']
                                except:
                                    pass

                        self.__log.info('Stitched LC size %s' % hdu.data.shape[0])
                        combined_data._p_list[IND_src_combined].data_unit[IND_lc_combined] = du.from_fits_hdu(hdu)

        return combined_data

    @staticmethod
    def plot_lc(combined_lc, source_name, systematic_fraction=0, ng_sig_limit=3):

        from scipy import stats
        for j, dd in enumerate(combined_lc._p_list):
            if dd.meta_data['src_name'] == source_name:
                IND_src_combined = j
                for ii, du in enumerate(dd.data_unit):
                    if 'LC' in du.name:
                        IND_lc_combined = ii

        for dd in combined_lc._p_list:
            if dd.meta_data['src_name'] == source_name:
                #self.__log.info('Source ' + source_name)
                hdu = combined_lc._p_list[IND_src_combined].data_unit[IND_lc_combined].to_fits_hdu()

        x = hdu.data['TIME']
        y = hdu.data['RATE']
        dy = hdu.data['ERROR']

        ind = np.argsort(x)
        x = x[ind]
        y = y[ind]
        dy = dy[ind]

        dy = np.sqrt(dy ** 2 + (y * systematic_fraction) ** 2)

        meany = np.sum(y / dy ** 2) / np.sum(1. / dy ** 2)
        err_mean = np.sum(1 / dy ** 2)

        fig = plt.figure()
        _ = plt.errorbar(x, y, yerr=dy, marker='o', capsize=0)
        _ = plt.axhline(meany, color='green', linewidth=3)
        _ = plt.xlabel('Time [IJD]')
        _ = plt.ylabel('Rate')

        ndof = len(y) - 1
        prob_limit = stats.norm().sf(ng_sig_limit)
        chi2_limit = stats.chi2(ndof).isf(prob_limit)
        band_width = np.sqrt(chi2_limit / err_mean)

        _ = plt.axhspan(meany - band_width, meany + band_width, color='green', alpha=0.3,
                        label=f'{ng_sig_limit} $\sigma$, {100 * systematic_fraction}% syst')

        plot_title = source_name
        _ = plt.title(plot_title)

        return fig

    @staticmethod
    def extract_catalog_from_image(image, include_new_sources=False, det_sigma=5, objects_of_interest=[],
                                          flag=1, isgri_flag=2, update_catalog=False):
        import json
        catalog_str = INTEGRALwrapper.extract_catalog_string_from_image(image, include_new_sources, det_sigma, objects_of_interest,
                                              flag, isgri_flag, update_catalog)
        return json.loads(catalog_str)

    @staticmethod
    def extract_catalog_string_from_image(image, include_new_sources=False, det_sigma=5, objects_of_interest=[],
                                          flag=1, isgri_flag=2, update_catalog=False):

        # Example: objects_of_interest=['Her X-1']
        #         objects_of_interest=[('Her X-1', Simbad.query )]
        #         objects_of_interest=[('Her X-1', Skycoord )]
        #         objects_of_interest=[ Skycoord(....) ]

        sources = image.dispatcher_catalog_1.table[image.dispatcher_catalog_1.table['significance'] >= det_sigma]

        if len(sources) == 0:
            INTEGRALwrapper.__log.warning('No sources in the catalog with det_sigma > %.1f' % det_sigma)
            return 'none'

        if not include_new_sources:
            ind = [not 'NEW' in ss for ss in sources['src_names']]
            clean_sources = sources[ind]
        else:
            clean_sources = sources

        for ooi in objects_of_interest:
            if isinstance(ooi, tuple):
                ooi, t = ooi
                if isinstance(t, SkyCoord):
                    source_coord = t

            elif isinstance(ooi, SkyCoord):
                t = Simbad.query_region(ooi)
            elif isinstance(ooi, str):
                t = Simbad.query_object(ooi)
            else:
                raise Exception("fail to elaborate object of interest")

            if isinstance(t, table.Table):
                source_coord = SkyCoord(t['RA'], t['DEC'], unit=(u.hourangle, u.deg), frame="fk5")

            INTEGRALwrapper.__log.info("Elaborating object of interest: ", ooi, source_coord)
            ra = source_coord.ra.deg
            dec = source_coord.dec.deg
            INTEGRALwrapper.__log.info("RA=%g Dec=%g" % (ra, dec))
            ind = clean_sources['src_names'] == ooi
            if np.count_nonzero(ind) > 0:
                INTEGRALwrapper.__log.info('Found ' + ooi + ' in catalog')
                clean_sources['FLAG'][ind] = flag
                clean_sources['ISGRI_FLAG'][ind] = isgri_flag
            else:
                INTEGRALwrapper.__log.info('Adding ' + ooi + ' to catalog')
                clean_sources.add_row((0, ooi, 0, ra, dec, 0, isgri_flag, flag, 1e-3, 0, 0))

        unique_sources = table.unique(clean_sources, keys=['src_names'])

        copied_image = copy.deepcopy(image)
        copied_image.dispatcher_catalog_1.table = unique_sources

        if update_catalog:
            image.dispatcher_catalog_1.table = unique_sources

        return copied_image.dispatcher_catalog_1.get_api_dictionary()

    @staticmethod
    def sum_spectral_products(spectrum_results, source_name):

        d = spectrum_results[0]

        ID_spec = -1
        ID_arf = -1
        ID_rmf = -1

        for ID, s in enumerate(d._p_list):
            if ('spectrum' in s.meta_data['product']):
                ID_spec = ID
            if ('arf' in s.meta_data['product']):
                ID_arf = ID
            if ('rmf' in s.meta_data['product']):
                ID_rmf = ID

            if ID_arf > 0 and ID_spec > 0 and ID_rmf > 0:
                break
        INTEGRALwrapper.__log.info('Initialize with IDs for spe, arf and rmf %d %d %d' % (ID_spec, ID_arf, ID_rmf))

        d = spectrum_results[0]
        spec = d._p_list[ID_spec].data_unit[1].data
        arf = d._p_list[ID_arf].data_unit[1].data
        rmf = d._p_list[ID_rmf].data_unit[2].data
        # ch=spec['CHANNEL']
        rate = spec['RATE'] * 0.
        err = spec['STAT_ERR'] * 0.
        syst = spec['SYS_ERR'] * 0.
        rate.fill(0)
        err.fill(0)
        syst.fill(0)
        # qual=spec['QUALITY']
        matrix = rmf['MATRIX'] * 0.
        specresp = arf['SPECRESP'] * 0.
        tot_expos = 0.
        tot_src_expos = 0.
        tot_ontime = 0.

        tstart = 1e10
        tstop = -1e10

        corr_expos = np.zeros(len(rate))
        # print(len(rate))
        for d in spectrum_results:

            ID_spec = -1
            ID_arf = -1
            ID_rmf = -1

            for ID, s in enumerate(d._p_list):
                if (s.meta_data['src_name'] == source_name):
                    if ('spectrum' in s.meta_data['product']):
                        ID_spec = ID
                    if ('arf' in s.meta_data['product']):
                        ID_arf = ID
                    if ('rmf' in s.meta_data['product']):
                        ID_rmf = ID

            if ID_arf < 0 or ID_spec < 0 or ID_rmf < 0:
                INTEGRALwrapper.__log.warning('Not found products for source %s' % source_name)
                break

            INTEGRALwrapper.__log.info('For source %s the IDs for spe, arf and rmf are %d %d %d' % (source_name, ID_spec, ID_arf, ID_rmf))

            spec = d._p_list[ID_spec].data_unit[1].data
            arf = d._p_list[ID_arf].data_unit[1].data
            rmf = d._p_list[ID_rmf].data_unit[2].data
            expos = d._p_list[ID_spec].data_unit[1].header['EXPOSURE']

            tot_expos += expos
            try:
                tot_src_expos += d._p_list[ID_spec].data_unit[1].header['EXP_SRC']
            except:
                pass

            tot_ontime += d._p_list[ID_spec].data_unit[1].header['ONTIME']

            loc_tstart = d._p_list[ID_spec].data_unit[1].header['TSTART']
            loc_tstop = d._p_list[ID_spec].data_unit[1].header['TSTOP']

            if loc_tstart < tstart:
                tstart = loc_tstart
            if loc_tstop > tstop:
                tstop = loc_tstop

            INTEGRALwrapper.__log.debug(expos)
            for j in range(len(rate)):
                if (spec['QUALITY'][j] == 0):
                    rate[j] = rate[j] + spec['RATE'][j] / (spec['STAT_ERR'][j]) ** 2
                    err[j] = err[j] + 1. / (spec['STAT_ERR'][j]) ** 2
                    syst[j] = syst[j] + (spec['SYS_ERR'][j]) ** 2 * expos
                    corr_expos[j] = corr_expos[j] + expos
            matrix = matrix + rmf['MATRIX'] * expos
            specresp = specresp + arf['SPECRESP'] * expos

        for i in range(len(rate)):
            if err[i] > 0.:
                rate[i] = rate[i] / err[i]
                err[i] = 1. / np.sqrt(err[i])
        matrix = matrix / tot_expos
        specresp = specresp / tot_expos
        syst = np.sqrt(syst / (corr_expos + 1.))
        INTEGRALwrapper.__log.info('Total exposure:', tot_expos)

        return rate, err, matrix, specresp, syst, tot_expos, tot_src_expos, tot_ontime, \
               tstart, tstop

    def sum_spectra(self):

        summed_data = copy.deepcopy(self.all_data[0])

        if len(summed_data._p_list) == 0 :
            self.__log.warning('Spectrum does not contain data !')
            return summed_data

        if not 'spectrum' in summed_data._p_list[0].meta_data['product']:
            raise ValueError('This is not a spectrum and you try to sum spectra')

        sources = self.get_sources()

        # print(sources)

        for source in sources:

            ID_spec = -1
            ID_arf = -1
            ID_rmf = -1

            for ID, s in enumerate(summed_data._p_list):
                if (s.meta_data['src_name'] == source):
                    if ('spectrum' in s.meta_data['product']):
                        ID_spec = ID
                    if ('arf' in s.meta_data['product']):
                        ID_arf = ID
                    if ('rmf' in s.meta_data['product']):
                        ID_rmf = ID

            if ID_arf < 0 or ID_spec < 0 or ID_rmf < 0:

                self.__log.warning('Not found products for source %s' % source)
                break

            self.__log.info('For source %s the IDs for spe, arf and rmf are %d %d %d' % (source, ID_spec, ID_arf, ID_rmf))

            rate, err, matrix, specresp, syst, tot_expos, tot_src_expos, tot_ontime, \
            tstart, tstop = self.sum_spectral_products(self.all_data, source)

            summed_data._p_list[ID_spec].data_unit[1].data['RATE'] = rate
            summed_data._p_list[ID_spec].data_unit[1].data['STAT_ERR'] = err
            summed_data._p_list[ID_spec].data_unit[1].data['SYS_ERR'] = syst

            summed_data._p_list[ID_spec].data_unit[1].header['EXPOSURE'] = tot_expos
            summed_data._p_list[ID_spec].data_unit[1].header['EXP_SRC'] = tot_src_expos
            summed_data._p_list[ID_spec].data_unit[1].header['ONTIME'] = tot_ontime
            summed_data._p_list[ID_spec].data_unit[1].header['TELAPSE'] = tstop - tstart

            summed_data._p_list[ID_spec].data_unit[1].header['TSTART'] = tstart
            summed_data._p_list[ID_spec].data_unit[1].header['TSTOP'] = tstop

            summed_data._p_list[ID_arf].data_unit[1].data['SPECRESP'] = specresp

            summed_data._p_list[ID_rmf].data_unit[2].data['MATRIX'] = matrix

        return summed_data

    @staticmethod
    def write_lc_fits_files(lc, source_name, subcases_pattern, output_dir='.'):
        lcprod = [l for l in lc._p_list if l.meta_data['src_name'] == source_name]
        if (len(lcprod) < 1):
            INTEGRALwrapper.__log.warning("source %s not found in light curve products" % source_name)
            return "none", 0, 0, 0

        if (len(lcprod) > 1):
            INTEGRALwrapper.__log.warning(
                "source %s is found more than once light curve products, writing only the first one" % source_name)

        instrument = lcprod[0].data_unit[1].header['INSTRUME']

        lc_fn = output_dir + "/%s_lc_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)
        lcprod[0].write_fits_file(lc_fn)

        ff = fits.open(lc_fn)  # , mode='update'
        mjdref = float(ff[1].header['MJDREF'])
        tstart = float(ff[1].header['TSTART']) + mjdref
        tstop = float(ff[1].header['TSTOP']) + mjdref
        try:
            exposure = ff[1].header['EXPOSURE']
        except:
            exposure = -1

        ff.close()

        return lc_fn, tstart, tstop, exposure

    @staticmethod
    def write_spectrum_fits_files(spectrum, source_name, subcases_pattern, grouping=[0, 0, 0], systematic_fraction=0,
                                  output_dir='.'):

        # Grouping argument is [minimum_energy, maximum_energy, number_of_bins]
        # number of bins > 0, linear grouping
        # number_of_bins < 0, logarithmic binning

        specprod = [l for l in spectrum._p_list if l.meta_data['src_name'] == source_name]

        if (len(specprod) < 1):
            INTEGRALwrapper.__log.warning("source %s not found in spectral products" % source_name)
            return "none", 0, 0, 0

        instrument = specprod[0].data_unit[1].header['INSTRUME']

        out_name = source_name.replace(' ', '_').replace('+', 'p')
        spec_fn = output_dir + "/%s_spectrum_%s_%s.fits" % (instrument, out_name, subcases_pattern)
        arf_fn = output_dir + "/%s_arf_%s_%s.fits" % (instrument, out_name, subcases_pattern)
        rmf_fn = output_dir + "/%s_rmf_%s_%s.fits" % (instrument, out_name, subcases_pattern)

        INTEGRALwrapper.__log.info("Saving spectrum %s with rmf %s and arf %s" % (spec_fn, rmf_fn, arf_fn))

        specprod[0].write_fits_file(spec_fn)
        specprod[1].write_fits_file(arf_fn)
        specprod[2].write_fits_file(rmf_fn)

        ff = fits.open(spec_fn, mode='update')

        ff[1].header['RESPFILE'] = rmf_fn
        ff[1].header['ANCRFILE'] = arf_fn
        mjdref = ff[1].header['MJDREF']
        tstart = float(ff[1].header['TSTART']) + mjdref
        tstop = float(ff[1].header['TSTOP']) + mjdref
        exposure = ff[1].header['EXPOSURE']
        ff[1].data['SYS_ERR'] = np.zeros(len(ff[1].data['SYS_ERR'])) + systematic_fraction
        ind = np.isfinite(ff[1].data['RATE'])
        ff[1].data['QUALITY'][ind] = 0

        if np.sum(grouping) != 0:

            if grouping[1] <= grouping[0] or grouping[2] == 0:
                raise RuntimeError('Wrong grouping arguments')

            ff_rmf = fits.open(rmf_fn)

            e_min = ff_rmf['EBOUNDS'].data['E_MIN']
            e_max = ff_rmf['EBOUNDS'].data['E_MAX']

            ff_rmf.close()

            ind1 = np.argmin(np.abs(e_min - grouping[0]))
            ind2 = np.argmin(np.abs(e_max - grouping[1]))

            n_bins = np.abs(grouping[2])

            ff[1].data['GROUPING'][0:ind1] = 0
            ff[1].data['GROUPING'][ind2:] = 0

            ff[1].data['QUALITY'][0:ind1] = 1
            ff[1].data['QUALITY'][ind2:] = 1

            if grouping[2] > 0:
                step = int((ind2 - ind1 + 1) / n_bins)
                INTEGRALwrapper.__log.info('Linear grouping with step %d' % step)
                for i in range(1, step):
                    j = range(ind1 + i, ind2, step)
                    ff[1].data['GROUPING'][j] = -1
            else:
                ff[1].data['GROUPING'][ind1:ind2] = -1
                e_step = (e_max[ind2] / e_min[ind1]) ** (1.0 / n_bins)
                INTEGRALwrapper.__log.info('Geometric grouping with step %.3f' % e_step)
                loc_e = e_min[ind1]
                while (loc_e < e_max[ind2]):
                    ind_loc_e = np.argmin(np.abs(e_min - loc_e))
                    ff[1].data['GROUPING'][ind_loc_e] = 1
                    loc_e *= e_step

        ff.flush()
        ff.close()

        return spec_fn, tstart, tstop, exposure

    @staticmethod
    def write_lc_fits_files(lc, source_name, subcases_pattern, output_dir='.'):

        lcprod = [l for l in lc._p_list if l.meta_data['src_name'] == source_name]
        if (len(lcprod) < 1):
            INTEGRALwrapper.__log.warning("source %s not found in light curve products" % source_name)
            return "none", 0, 0, 0

        if (len(lcprod) > 1):
            INTEGRALwrapper.__log.warning(
                "source %s is found more than once light curve products, writing only the first one" % source_name)

        instrument = lcprod[0].data_unit[1].header['INSTRUME']

        lc_fn = output_dir + "/%s_lc_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)
        lcprod[0].write_fits_file(lc_fn)

        ff = fits.open(lc_fn)  # , mode='update'
        mjdref = ff[1].header['MJDREF']
        tstart = float(ff[1].header['TSTART']) + mjdref
        tstop = float(ff[1].header['TSTOP']) + mjdref
        try:
            exposure = ff[1].header['EXPOSURE']
        except:
            exposure = -1

        ff.close()

        return lc_fn, tstart, tstop, exposure

    @staticmethod
    def show_spectral_products(summed_data):
        for dd, nn in zip(summed_data._p_list, summed_data._n_list):
            INTEGRALwrapper.__log.debug(nn)
            dd.show_meta()
            # for kk in dd.meta_data.items():
            if 'spectrum' in dd.meta_data['product']:
                INTEGRALwrapper.__log.debug(dd.data_unit[1].header['EXPOSURE'])
            dd.show()

    @staticmethod
    def plot_image(ext_sig, sources, det_sigma=7, objects_of_interest=[], cmap=matplotlib.cm.gist_earth,
                   levels=np.linspace(1, 10, 10)):
        # ext_sig,ext_exp=self.open_image(i_eband)
        # m_on = ~np.isnan(ext_sig.data) & (ext_exp.data > np.nanmax(ext_exp.data) / 1e10)
        # self.ext_sig.data[~m_on] = np.NaN
        # a=hist(ext.data[m_on],bins=linspace(-10,50,100),log=True)

        plt.figure(figsize=(8, 6))

        j, i = plt.meshgrid(range(ext_sig.data.shape[0]), range(ext_sig.data.shape[1]))
        w = wcs.WCS(ext_sig.header)
        ra, dec = w.wcs_pix2world(np.column_stack([i.flatten(), j.flatten()]), 0).transpose()
        ra = ra.reshape(i.shape)
        dec = dec.reshape(j.shape)

        coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
        # coord_gal = coord.transform_to("galactic")
        # l = coord_gal.l.deg
        # b = coord_gal.b.deg

        # cmap.set_under("w")

        data = np.transpose(ext_sig.data)
        data = np.ma.masked_equal(data, np.NaN)

        ## CF display image crossing ra =0
        zero_crossing = False
        # print("******************", ra.max(), ra.min())
        # print("******************", np.abs(ra.max() - 360.0), np.abs(ra.min()))
        if np.abs(ra.max() - 360.0) < 0.01 and np.abs(ra.min()) < 0.01:
            zero_crossing = True
            ind_ra = ra > 180.
            ra[ind_ra] -= 360.
            INTEGRALwrapper.__log.info("Sorting for RA crossing zero")
            # print("ra shape ", ra.shape)
            ind_sort = np.argsort(ra, axis=-1)

            # print("Sorted RA", ind_sort.shape)
            # print(ind_sort)

            ra = np.take_along_axis(ra, ind_sort, axis=-1)
            # ra = ra[ind_sort]

            # tmp = [ ra[ii] for ii in ind_sort]
            #
            # ra=tmp.copy()
            # print("ordered ra shape ", ra.shape)
            # tmp = [data[ii] for ii in ind_sort]
            #
            # data = tmp.copy()
            data = np.take_along_axis(data, ind_sort, axis=-1)
            # print("data shape ", data.shape)
            #
            # print("Finished sorting")

        ## CF end
        cs = plt.contourf(ra, dec, data, cmap=cmap, levels=levels,
                          extend="both", zorder=0)

        # print("Made contours")
        cs.cmap.set_under('k')
        cs.set_clim(np.min(levels), np.max(levels))

        cb = plt.colorbar(cs)

        plt.tight_layout()
        # plt.xlim([ra[np.transpose(m_on)].max(), ra[np.transpose(m_on)].min()])
        # plt.ylim([dec[np.transpose(m_on)].min(), dec[np.transpose(m_on)].max()])
        plt.xlim([ra.max(), ra.min()])
        plt.ylim([dec.min(), dec.max()])

        ras = np.array([x for x in sources['ra']])
        decs = np.array([x for x in sources['dec']])
        names = np.array([x for x in sources['src_names']])
        sigmas = np.array([x for x in sources['significance']])
        # Defines relevant indexes for plotting regions

        m_new = np.array(['NEW' in name for name in names])

        # m_offaxis = self.source_results.MEAN_VAR > 5
        # m_noisy = self.source_results.DETSIG_CORR < 5
        m_noisy = sigmas < 5

        # plot new sources as pink circles

        try:
            m = m_new & (sigmas > det_sigma)
            ra_coord = ras[m]
            dec_coord = decs[m]
            new_names = names[m]
            if zero_crossing:
                ind_ra = ra_coord > 180.
                try:
                    ra_coord[ind_ra] -= 360.
                except:
                    pass
        except:
            ra_coord = []
            dec_coord = []
            new_names = []

        plt.scatter(ra_coord, dec_coord, s=100, marker="o", facecolors='none',
                    edgecolors='pink',
                    lw=3, label="NEW any", zorder=5)
        for i in range(len(ra_coord)):
            # print("%f %f %s\n"%(ra_coord[i], dec_coord[i], names[i]))
            plt.text(ra_coord[i],
                     dec_coord[i] + 0.5,
                     new_names[i], color="pink", size=15)

        # CF Plots object of interest as green
        for ooi in objects_of_interest:
            if isinstance(ooi, tuple):
                ooi, t = ooi
                c = t
            elif isinstance(ooi, SkyCoord):
                t = Simbad.query_region(ooi)
                c = SkyCoord(t['RA'], t['DEC'], unit=(u.hourangle, u.deg), frame="fk5")
            elif isinstance(ooi, str):
                t = Simbad.query_object(ooi)
                c = SkyCoord(t['RA'], t['DEC'], unit=(u.hourangle, u.deg), frame="fk5")
            else:
                raise Exception("fail")

            INTEGRALwrapper.__log.debug("object:", ooi, c)

            plt.scatter(c.ra.deg, c.dec.deg, marker="o", facecolors='none',
                        edgecolors='white',
                        lw=3, label="Added", zorder=5)
            # for i in range(len(c)):
            plt.text(c.ra.deg,
                     c.dec.deg + 0.5,
                     str(ooi), color="white", size=15)

        # m = m_new & m_offaxis
        # p.scatter(self.coord[m].ra.deg, self.coord[m].dec.deg, s=100, marker="o", facecolors='none', edgecolors='red',
        #        lw=3,label="NEW off-axis")

        # m = m_new & ~m_offaxis & ~m_noisy
        # p.scatter(self.coord[m].ra.deg, self.coord[m].dec.deg, s=100, marker="o", facecolors='none',
        #        edgecolors='white', lw=3,label="NEW unsuspicious")

        # for i in self.source_results.index[m]:
        #    p.text(self.imcat_coords[i].ra.deg,self.imcat_coords[i].dec.deg,self.imcat.NAME[i],color="white",size=15)

        try:
            m = ~m_new & (sigmas > det_sigma - 1)
            ra_coord = ras[m]
            dec_coord = decs[m]
            cat_names = names[m]
            if zero_crossing:
                ind_ra = ra_coord > 180.
                try:
                    ra_coord[ind_ra] -= 360.
                except:
                    pass
        except:
            ra_coord = []
            dec_coord = []
            cat_names = []

        plt.scatter(ra_coord, dec_coord, s=100, marker="o", facecolors='none',
                    edgecolors='magenta', lw=3, label="known", zorder=5)
        for i in range(len(ra_coord)):
            # print("%f %f %s\n"%(ra_coord[i], dec_coord[i], names[i]))
            plt.text(ra_coord[i],
                     dec_coord[i] + 0.5,
                     cat_names[i], color="magenta", size=15)

        # for i in sorted(self.source_results.index,key=lambda i:-self.source_results.DETSIG[i])[:10]:
        #    ra_coord=self.source_results.iloc[i].RA_FIN
        #    if zero_crossing and ra_coord >180.:
        #        ra_coord -=360.
        #    p.text(ra_coord,
        #           self.source_results.iloc[i].DEC_FIN+0.5,
        #           self.source_results.NAME[i],color="yellow",size=15)

        # if self.ghost_coord is not None:
        #    p.scatter(self.ghost_coord.ra.deg, self.ghost_coord.dec.deg, s=130, marker="o", facecolors='#FFFF60', edgecolors='#FF6060',
        #            lw=0, alpha=0.1)
        # p.legend()

        # plt.gca().set_axis_bgcolor('white')

        plt.grid(color="grey", zorder=10)

        plt.xlabel("RA")
        plt.ylabel("Dec")

    @staticmethod
    def get_pointings(ra, dec, radius, tstart='2003-01-01T00:00:00', tstop='2020-04-01T00:00:00', type='cons'):

        url = oda_public_host + '/gw/timesystem/api/v1.0/scwlist/' + type + '/'
        url += tstart + '/' + tstop + '?'
        url += 'ra=%.4f&dec=%.4f&radius=%.2f&min_good_isgri=1000&return_columns=SWID,RA_SCX,DEC_SCX' % (
            ra, dec, radius)
        INTEGRALwrapper.__log.debug(url)
        return requests.get(url).json()

    @staticmethod
    def get_utc_from_revnum(revnum):
        url = oda_public_host + '/gw/timesystem/api/v1.0/converttime/REVNUM/%04d/IJD' % revnum
        ijd = requests.get(url).json()
        ijd_start = ijd.split()[1]
        ijd_stop = ijd.split()[2]
        url2 = oda_public_host + '/gw/timesystem/api/v1.0/converttime/IJD/%s/UTC'
        utc_start = requests.get(url2 % ijd_start).json()
        utc_stop = requests.get(url2 % ijd_stop).json()
        return utc_start, utc_stop

    # This is copied from integralclient by V. Savchenko
    @staticmethod
    def converttime(informat, intime, outformat, debug=True):
        import time
        url = oda_public_host + '/gw/timesystem/api/v1.0/converttime/' + \
              informat + '/' + t2str(intime) + '/' + outformat
        ntries_left = 3

        while ntries_left > 0:
            try:
                r = requests.get(url)
                if r.status_code != 200:
                    raise ValueError('error converting ' + url + '; from timesystem server: ' + str(r.text))

                if outformat == "ANY":
                    try:
                        return r.json()
                    except:
                        pass
                return r.text.strip().strip("\"")

            except Exception as e:
                if 'is close' in repr(e):
                    raise

                ntries_left -= 1

                if ntries_left > 0:

                    time.sleep(5)
                    continue
                else:
                    raise


def get_format_string(res, ep, em):
    # e_max=np.max(np.abs(ep), np.abs(em))
    e_min = np.min([np.abs(ep), np.abs(em)])
    myformat = "%.2f"

    if res == 0 or e_min == 0:
        return myformat

    decade = np.floor(np.log10(np.abs(res)))
    if e_min != res:
        decade_min = np.floor(np.log10(np.abs(res - e_min)))
    else:
        decade_min = np.floor(np.log10(np.abs(e_min)))

    # print("Getting Format")
    # print(res, em, ep, decade, decade_min)

    if (np.abs(decade) <= 2 and decade_min > 0):
        myformat = "%.0f"
    elif (np.abs(decade) == 0 and decade_min == 0):
        myformat = "%.1f"
    else:
        if (np.abs(decade) <= 2 and decade_min < 0):
            myformat = "%." + "%d" % (-decade_min) + "f"
            if np.abs(e_min / 10 ** (decade_min)) < 2:
                myformat = "%." + "%d" % (-decade_min + 1) + "f"
        else:
            myformat = "%." + "%d" % (np.abs(decade_min - decade)) + "e"
            if np.abs(e_min / 10 ** (decade_min)) < 2:
                myformat = "%." + "%d" % (np.abs(decade_min - decade) + 1) + "e"

    return myformat


def find_duplicates(data, separation=3):
    # Prints out duplicates and returns two arrays of indexes: first and second sources
    # separation is the threshold separation in arcminutes

    ind = np.ones(len(data), dtype=bool)
    c = SkyCoord(ra=data['ra'], dec=data['dec'])

    idx_self, d2d_self, d3d_self = c.match_to_catalog_sky(c, nthneighbor=2)

    ind_first_match = np.argwhere(d2d_self.arcmin < separation).flatten()

    #print("There are %d duplicates" % (len(ind_first_match)))

    if len(ind_first_match) == 0:
        return None, None

    ind_first_match = ind_first_match
    ind_second_match = idx_self[ind_first_match]

    for i in range(len(c)):
        if d2d_self[i].arcmin < separation:
            INTEGRALwrapper.__log.debug("%d %d %s %f %f %s %f %f %f" % (
                i, idx_self[i], data['src_names'].data[ind][i], data['ra'].data[ind][i],
                data['dec'].data[ind][i],
                data['src_names'].data[ind][idx_self[i]], data['ra'].data[ind][idx_self[i]],
                data['DEC_OBJ'].data[ind][idx_self[i]],
                d2d_self[i].arcmin))

    return ind_first_match, ind_second_match


def get_parameter_output_string(comp, par, par_range=True, threshold_plusminus=0.1, latex_out=False):

    xspec_input = True
    try:
        unit = par.unit
    except:
        xspec_input = False

    if xspec_input:
        # Xspec parameters
        val = par.values[0]
        unit = par.unit
        lval = par.error[0]
        uval = par.error[1]
        if comp.name == 'cflux' and par.name == 'lg10Flux':
            val = 10 ** (val + 10)
            lval = 10 ** (lval + 10)
            uval = 10 ** (uval + 10)
            unit = 'x1e-10 erg/s/cm^2'
        if comp.name == 'pegpwrlw' and par.name == 'norm':
            unit = 'x1e-12 erg/s/cm^2'
        output_par = not par.frozen and par.link == ''
        par_name = par.name
        comp_name = comp.name
    else:
        # pandas quantiles
        val = par[0.5]
        lval = par[0.16]
        uval = par[0.84]
        unit = ''

        if 'lg10Flux' in par:
            val = 10 ** (val + 10)
            lval = 10 ** (lval + 10)
            uval = 10 ** (uval + 10)

        par_name = comp.split('__')[0]
        comp_name = ''
        output_par = True


    if output_par:

        format_str = get_format_string(val, uval, lval)
        if par_range:
            output_str = "%s %s " + format_str + " %s (" + format_str + "-" + format_str + ")"
            return_str = output_str % (comp_name, par_name, val, unit, lval, uval)
        else:
            # print(np.abs((lval + uval - 2*val) / (-lval+uval) * 2))
            if np.abs((lval + uval - 2 * val) / (-lval + uval) * 2) > threshold_plusminus:
                output_str = "%s %s " + format_str + " (" + format_str + " +" + format_str + ") %s"
                if latex_out:
                    output_str = "%s & %s & " + format_str + "$_{" + format_str + "}^{+" + format_str + "}$ & %s \\\\"
                return_str = output_str % (comp_name, par_name, val, lval - val, uval - val, unit)
            else:
                output_str = "%s %s " + format_str + " +/- " + format_str + " %s"
                if latex_out:
                    output_str = "%s & %s & " + format_str + " &$\pm$ " + format_str + " & %s \\\\"
                return_str = output_str % (comp_name, par_name, val, (uval - lval) / 2, unit)

    elif not par.link == '':
        format_str = get_format_string(val, val, val)
        output_str = "%s %s " + format_str + " %s (%s)"
        if latex_out:
            output_str = "%s & %s & " + format_str + " & %s & (%s) \\\\"
        return_str = output_str % (comp.name, par.name, val, unit, par.link)
    else:
        format_str = get_format_string(val, val, val)
        output_str = "%s %s " + format_str + " %s "
        if latex_out:
            output_str = "%s & %s & " + format_str + " & -- & %s \\\\"
        return_str = output_str % (comp.name, par.name, par.values[0], par.unit)

    return return_str


# Copied from VS's integralclient
def t2str(t):
    if isinstance(t, float):
        return "%.20lg" % t

    if isinstance(t, int):
        return "%i" % t

    if isinstance(t, str):
        return t
