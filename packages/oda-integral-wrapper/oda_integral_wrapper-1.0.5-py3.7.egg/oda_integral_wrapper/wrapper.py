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

__all__=['INTEGRALwrapper']



class INTEGRALwrapper(object):

    #we assume that:
    # - product is compatible with oda_api
    # - the list of science windows can be ordered

    def __init__(self,product='None', default_host='production'):


        self.product=product

        instrument='isgri'
        if('jemx' in product):
            instrument='jemx'

        host='https://www.astro.unige.ch/cdci/astrooda/dispatch-data'

        if default_host is 'staging':
            host='http://cdcihn/staging-1.2/dispatcher'

        if default_host is 'test':
            host='http://cdciweb01.isdc.unige.ch:8084/astrooda'

        try:
            self.disp = oda_api.api.DispatcherAPI(host=host)
            self.disp.get_instrument_description(instrument)
        except:
            try:
                self.disp = oda_api.api.DispatcherAPI(host=host)
                self.disp.get_instrument_description(instrument)
            except:
                raise ConnectionError




    def long_scw_list_call(self, in_total_scw_list, s_max=50, **arguments):
        
        total_scw_list = sorted(in_total_scw_list)

        self.product=arguments['product']

        if len(total_scw_list) > s_max:
            ind_max=int(len(total_scw_list)/s_max)
            scw_lists = [total_scw_list[i*s_max:(i+1)*s_max] for i in range(ind_max)]
            if ind_max*s_max < len(total_scw_list):
                scw_lists.append(total_scw_list[ind_max*s_max:])
        else:
            scw_lists=[total_scw_list]
        
        
        self.all_data=[]
        tot_num=0
        for scw_list in scw_lists:
            print(len(scw_list))
            tot_num+=len(scw_list)
            scw_list_str=",".join([s for s in sorted(set( scw_list))])
            data=self.disp.get_product(scw_list=scw_list_str, **arguments)
            self.all_data.append(data)
        
        print(len(total_scw_list) , tot_num)



        if 'spectrum' in self.product:
            return self.sum_spectra()


        if 'lc' in self.product:
            return self.stitch_lc()

        #TODO implement mosaic (difficult)
        
        return self.all_data
        


    def get_sources(self):
        sources=set()
        
        
        #It works both on collection and single instance
        try:
            for data in self.all_data:
                #print(set([l.meta_data['src_name'] for l in data._p_list]))
                sources=sources.union(set([l.meta_data['src_name'] for l in data._p_list]))
        except:
            sources=sources.union(set([l.meta_data['src_name'] for l in self.all_data._p_list]))
            

        return sources


    def stitch_lc(self):

        combined_data = copy.deepcopy(self.all_data[0])

        if not 'lc' in combined_data._p_list[0].name:
            raise ValueError('This is not a light curve and you try to stitch them')

        sources = self.get_sources()

        #gets indexes of source and lc in combined data
        for source in sources:
            for j,dd in enumerate(combined_data._p_list):
                if dd.meta_data['src_name'] == source:
                    IND_src_combined = j
                    for ii, du in enumerate(dd.data_unit):
                        if 'LC' in du.name:
                            IND_lc_combined = ii


            for data in self.all_data[1:]:
                for dd in data._p_list:
                    if dd.meta_data['src_name'] == source:
                        print('Source '+ source )

                        hdu = combined_data._p_list[IND_src_combined].data_unit[IND_lc_combined].to_fits_hdu()

                        for du in dd.data_unit:
                            if 'LC' in du.name:

                                print('Original LC size %s'%hdu.data.shape[0])

                                new_data = hdu.data.copy()
                                new_data.resize(((hdu.data.shape[0] + du.data.shape[0])))

                                for i, col in enumerate(hdu.columns):
                                    #print(col)
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
                                    hdu.header['TELAPSE'] = hdu.header['TSTOP']-hdu.header['TSTART']
                                except:
                                    pass

                        print('Stitched LC size %s'%hdu.data.shape[0])
                        combined_data._p_list[IND_src_combined].data_unit[IND_lc_combined] = du.from_fits_hdu(hdu)

        return combined_data

    @staticmethod
    def extract_catalog_string_from_image(image, include_new_sources=False, det_sigma=5, objects_of_interest=[],
                                          flag=1, isgri_flag=2, update_catalog=False ):

        #Example: objects_of_interest=['Her X-1']
        #         objects_of_interest=[('Her X-1', Simbad.query )]
        #         objects_of_interest=[('Her X-1', Skycoord )]
        #         objects_of_interest=[ Skycoord(....) ]


        sources = image.dispatcher_catalog_1.table[image.dispatcher_catalog_1.table['significance'] >= det_sigma]

        if len(sources) ==0:
            print('No sources in the catalog with det_sigma > %.1f'%det_sigma)
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

            print("Elaborating object of interest: ", ooi, source_coord)
            ra=source_coord.ra.deg
            dec=source_coord.dec.deg
            print("RA=%g Dec=%g"%(ra,dec))
            ind=clean_sources['src_names'] == ooi
            if np.count_nonzero(ind) > 0 :
                print('Found '+ ooi + ' in catalog')
                clean_sources['FLAG'][ind]=flag
                clean_sources['ISGRI_FLAG'][ind] = isgri_flag
            clean_sources.add_row((0,ooi,0,ra,dec,0,isgri_flag,flag,1e-3))


        unique_sources = table.unique(clean_sources, keys=['src_names'])

        copied_image=copy.deepcopy(image)
        copied_image.dispatcher_catalog_1.table = unique_sources

        if update_catalog:
            image.dispatcher_catalog_1.table = unique_sources

        return copied_image.dispatcher_catalog_1.get_api_dictionary()


    @staticmethod
    def sum_spectral_products(spectrum_results, source_name):
        
        d=spectrum_results[0]

        ID_spec=-1
        ID_arf=-1
        ID_rmf=-1

        for ID, s in enumerate(d._p_list):
            if ('spectrum' in s.meta_data['product']):
                ID_spec = ID
            if ('arf' in s.meta_data['product']):
                ID_arf = ID
            if ('rmf' in s.meta_data['product']):
                ID_rmf = ID

            if ID_arf > 0 and ID_spec > 0 and ID_rmf > 0:
                break
        print('Initialize with IDs for spe, arf and rmf %d %d %d' % (ID_spec, ID_arf, ID_rmf))

        d=spectrum_results[0]
        spec=d._p_list[ID_spec].data_unit[1].data
        arf=d._p_list[ID_arf].data_unit[1].data
        rmf=d._p_list[ID_rmf].data_unit[2].data
        #ch=spec['CHANNEL']
        rate=spec['RATE']*0.
        err=spec['STAT_ERR']*0.
        syst=spec['SYS_ERR']*0.
        rate.fill(0)
        err.fill(0)
        syst.fill(0)
        #qual=spec['QUALITY']
        matrix=rmf['MATRIX']*0.
        specresp=arf['SPECRESP']*0.
        tot_expos=0.
        tot_src_expos=0.
        tot_ontime=0.

        tstart=1e10
        tstop=-1e10

        corr_expos=np.zeros(len(rate))
        #print(len(rate))
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

            if ID_arf < 0 or ID_spec <0  or ID_rmf < 0:
                print('Not found products for source %s'%source_name)
                break

            print('For source %s the IDs for spe, arf and rmf are %d %d %d' % (source_name, ID_spec, ID_arf, ID_rmf))

            spec=d._p_list[ID_spec].data_unit[1].data
            arf=d._p_list[ID_arf].data_unit[1].data
            rmf=d._p_list[ID_rmf].data_unit[2].data
            expos=d._p_list[ID_spec].data_unit[1].header['EXPOSURE']

            tot_expos += expos
            try:
                tot_src_expos += d._p_list[ID_spec].data_unit[1].header['EXP_SRC']
            except:
                pass

            tot_ontime +=  d._p_list[ID_spec].data_unit[1].header['ONTIME']

            loc_tstart =  d._p_list[ID_spec].data_unit[1].header['TSTART']
            loc_tstop =  d._p_list[ID_spec].data_unit[1].header['TSTOP']

            if loc_tstart < tstart:
                tstart=loc_tstart
            if loc_tstop > tstop:
                tstop=loc_tstop

            print(expos)
            for j in range(len(rate)):
                if(spec['QUALITY'][j]==0):          
                    rate[j]=rate[j]+spec['RATE'][j]/(spec['STAT_ERR'][j])**2
                    err[j]=err[j]+1./(spec['STAT_ERR'][j])**2
                    syst[j]=syst[j]+(spec['SYS_ERR'][j])**2*expos
                    corr_expos[j]=corr_expos[j]+expos
            matrix=matrix+rmf['MATRIX']*expos
            specresp=specresp+arf['SPECRESP']*expos

        for i in range(len(rate)):
            if err[i]>0.:
                rate[i]=rate[i]/err[i]
                err[i]=1./np.sqrt(err[i])
        matrix=matrix/tot_expos
        specresp=specresp/tot_expos
        syst=np.sqrt(syst/(corr_expos+1.))
        print('Total exposure:',tot_expos)
        
        return rate, err, matrix, specresp, syst, tot_expos, tot_src_expos, tot_ontime, \
            tstart, tstop





    def sum_spectra(self):
        
        summed_data=copy.deepcopy(self.all_data[0])
        
        if not 'spectrum' in summed_data._p_list[0].meta_data['product']:
            raise ValueError('This is not a spectrum and you try to sum spectra')
        
        sources=self.get_sources()
        
        #print(sources)

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

            if ID_arf < 0 or ID_spec <0  or ID_rmf < 0:
                print('Not found products for source %s'%source)
                break

            print('For source %s the IDs for spe, arf and rmf are %d %d %d' % (source, ID_spec, ID_arf, ID_rmf))

            rate, err, matrix, specresp, syst, tot_expos, tot_src_expos, tot_ontime, \
            tstart, tstop = self.sum_spectral_products(self.all_data, source)

            summed_data._p_list[ID_spec].data_unit[1].data['RATE']=rate
            summed_data._p_list[ID_spec].data_unit[1].data['STAT_ERR']=err
            summed_data._p_list[ID_spec].data_unit[1].data['SYS_ERR']=syst
            
            summed_data._p_list[ID_spec].data_unit[1].header['EXPOSURE']=tot_expos
            summed_data._p_list[ID_spec].data_unit[1].header['EXP_SRC']=tot_src_expos
            summed_data._p_list[ID_spec].data_unit[1].header['ONTIME']=tot_ontime
            summed_data._p_list[ID_spec].data_unit[1].header['TELAPSE']=tstop-tstart

            summed_data._p_list[ID_spec].data_unit[1].header['TSTART']=tstart
            summed_data._p_list[ID_spec].data_unit[1].header['TSTOP']=tstop
            
            summed_data._p_list[ID_arf].data_unit[1].data['SPECRESP']=specresp
            
            summed_data._p_list[ID_rmf].data_unit[2].data['MATRIX']=matrix


            
            
        return summed_data

    @staticmethod
    def write_lc_fits_files(lc, source_name, subcases_pattern, output_dir='.'):
        lcprod= [l for l in lc._p_list if l.meta_data['src_name'] == source_name]
        if (len(lcprod) < 1):
            print("source %s not found in light curve products" % source_name)
            return "none", 0, 0, 0

        if (len(lcprod) > 1 ):
            print("WARN: source %s is found more than once light curve products, writing only the first one" % source_name)


        instrument = lcprod[0].data_unit[1].header['INSTRUME']

        lc_fn=output_dir + "/%s_lc_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)
        lcprod[0].write_fits_file(lc_fn)

        ff = fits.open(lc_fn) #, mode='update'
        mjdref = ff[1].header['MJDREF']
        tstart = float(ff[1].header['TSTART']) + mjdref
        tstop = float(ff[1].header['TSTOP']) + mjdref
        try:
            exposure = ff[1].header['EXPOSURE']
        except:
            exposure=-1

        ff.close()

        return lc_fn, tstart, tstop, exposure

    @staticmethod
    def write_spectrum_fits_files(spectrum, source_name, subcases_pattern, grouping=[0, 0, 0], systematic_fraction=0,
                                  output_dir='.'):

        #Grouping argument is [minimum_energy, maximum_energy, number_of_bins]
        #number of bins > 0, linear grouping
        #number_of_bins < 0, logarithmic binning

        specprod = [l for l in spectrum._p_list if l.meta_data['src_name'] == source_name]

        if (len(specprod) < 1):
            print("source %s not found in spectral products" % source_name)
            return "none", 0, 0, 0

        instrument = specprod[0].data_unit[1].header['INSTRUME']

        spec_fn = output_dir + "/%s_spectrum_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)
        arf_fn = output_dir + "/%s_arf_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)
        rmf_fn = output_dir + "/%s_rmf_%s_%s.fits" % (instrument, source_name.replace(' ', '_'), subcases_pattern)

        print("Saving spectrum %s with rmf %s and arf %s" % (spec_fn, rmf_fn, arf_fn))

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
                print('Linear grouping with step %d' % step)
                for i in range(1, step):
                    j = range(ind1 + i, ind2, step)
                    ff[1].data['GROUPING'][j] = -1
            else:
                ff[1].data['GROUPING'][ind1:ind2] = -1
                e_step = (e_max[ind2] / e_min[ind1]) ** (1.0 / n_bins)
                print('Gometric grouping with step %.3f' % e_step)
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
            print("source %s not found in light curve products" % source_name)
            return "none", 0, 0, 0

        if (len(lcprod) > 1):
            print(
            "WARN: source %s is found more than once light curve products, writing only the first one" % source_name)

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
        for dd,nn in zip(summed_data._p_list, summed_data._n_list):
            print(nn)
            dd.show_meta()
            #for kk in dd.meta_data.items():
            if 'spectrum' in dd.meta_data['product']:
                print(dd.data_unit[1].header['EXPOSURE'])
            dd.show()


    @staticmethod
    def plot_image(ext_sig, sources, det_sigma=7, objects_of_interest=[]):
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

        cmap = matplotlib.cm.gist_earth
        # cmap.set_under("w")

        data = np.transpose(ext_sig.data)
        data = np.ma.masked_equal(data, np.NaN)

        ## CF display image crossing ra =0
        zero_crossing = False
        print("******************", ra.max(), ra.min())
        print("******************", np.abs(ra.max() - 360.0), np.abs(ra.min()))
        if np.abs(ra.max() - 360.0) < 0.01 and np.abs(ra.min()) < 0.01:
            zero_crossing = True
            ind_ra = ra > 180.
            ra[ind_ra] -= 360.
            print("sorting for RA crossing zero")
            print("ra shape ", ra.shape)
            ind_sort = np.argsort(ra, axis=-1)

            print("Sorted RA", ind_sort.shape)
            print(ind_sort)
            ra = ra[ind_sort]

            tmp = [ ra[ii] for ii in ind_sort]

            ra=tmp.copy()

            print("ordered ra shape ", ra.shape)

            tmp = [data[ii] for ii in ind_sort]

            data = tmp.copy()

            print("data shape ", data.shape)

            print("Finished sorting")

        ## CF end
        cs = plt.contourf(ra, dec, data, cmap=cmap, levels=np.linspace(1, 10, 10),
                          extend="both", zorder=0)

        #print("Made contours")
        cs.cmap.set_under('k')
        cs.set_clim(1, 10)

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
            elif isinstance(ooi, SkyCoord):
                t = Simbad.query_region(ooi)
            elif isinstance(ooi, str):
                t = Simbad.query_object(ooi)
            else:
                raise Exception("fail")

            c = SkyCoord(t['RA'], t['DEC'], unit=(u.hourangle, u.deg), frame="fk5")
            print("object:", ooi, c)

            plt.scatter(c.ra.deg, c.dec.deg, marker="o", facecolors='none',
                        edgecolors='green',
                        lw=3, label="Added", zorder=5)
            # for i in range(len(c)):
            plt.text(c.ra.deg,
                     c.dec.deg + 0.5,
                     str(ooi), color="green", size=15)

        # m = m_new & m_offaxis
        # p.scatter(self.coord[m].ra.deg, self.coord[m].dec.deg, s=100, marker="o", facecolors='none', edgecolors='red',
        #        lw=3,label="NEW off-axis")

        # m = m_new & ~m_offaxis & ~m_noisy
        # p.scatter(self.coord[m].ra.deg, self.coord[m].dec.deg, s=100, marker="o", facecolors='none',
        #        edgecolors='white', lw=3,label="NEW unsuspicious")

        # for i in self.source_results.index[m]:
        #    p.text(self.imcat_coords[i].ra.deg,self.imcat_coords[i].dec.deg,self.imcat.NAME[i],color="white",size=15)

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
    def get_pointings(ra, dec, radius, tstart='2003-01-01T00:00:00', tstop='2020-01-01T00:00:00', type='cons'):

        url='https://www.astro.unige.ch/cdci/astrooda/dispatch-data/gw/timesystem/api/v1.0/scwlist/'+type+'/'
        url+=tstart +'/' +tstop+'?'
        url+='ra=%.4f&dec=%.4f&radius=%.2f&min_good_isgri=1000&return_columns=SWID,RA_SCX,DEC_SCX' % (
                ra, dec, radius)

        return requests.get(url).json()

def get_format_string(res, ep, em):
    # e_max=np.max(np.abs(ep), np.abs(em))
    e_min = np.min([np.abs(ep), np.abs(em)])
    myformat = "%.2f"

    if res == 0 or e_min == 0:
        return myformat

    decade = np.floor(np.log10(np.abs(res)))
    if e_min != res:
        decade_min = np.floor(np.log10(np.abs(res-e_min)))
    else:
        decade_min = np.floor(np.log10(np.abs(e_min)))

    #print("Getting Format")
    #print(res, em, ep, decade, decade_min)

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


def get_parameter_output_string(comp, par, par_range=True, threshold_plusminus=0.1, latex_out=False):

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
    if not par.frozen and par.link == '':

        format_str = get_format_string(val, uval, lval)
        if par_range:
            output_str = "%s %s " + format_str + " %s (" + format_str + "-" + format_str + ")"
            return_str = output_str % (comp.name, par.name, val, unit, lval, uval)
        else:
            #print(np.abs((lval + uval - 2*val) / (-lval+uval) * 2))
            if np.abs((lval + uval-2*val) / (-lval+uval) * 2) > threshold_plusminus:
                output_str = "%s %s " + format_str + " (" + format_str + " +" + format_str + ") %s"
                if latex_out:
                    output_str = "%s & %s & " + format_str + "$_{" + format_str + "}^{+" + format_str + "}$ & %s \\\\"
                return_str=output_str % (comp.name, par.name, val, lval-val, uval-val, unit)
            else:
                output_str = "%s %s " + format_str + " +/- " + format_str + " %s"
                if latex_out:
                    output_str = "%s & %s & " + format_str + " &$\pm$ " + format_str + " & %s \\\\"
                return_str = output_str % (comp.name, par.name, val, (uval-lval)/2, unit)

    elif not par.link == '':
        format_str = get_format_string(val, val, val)
        output_str = "%s %s " + format_str + " %s (%s)"
        if latex_out:
            output_str = "%s & %s & " + format_str + " & %s & (%s) \\\\"
        return_str=output_str % (comp.name, par.name, val, unit, par.link)
    else:
        format_str = get_format_string(val, val, val)
        output_str = "%s %s " + format_str + " %s "
        if latex_out:
            output_str = "%s & %s & " + format_str + " & -- & %s \\\\"
        return_str=output_str % (comp.name, par.name, par.values[0], par.unit)


    return return_str
