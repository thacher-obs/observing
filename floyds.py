import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.signal import resample
from scipy import interpolate


#KO 3/29: Divided into two preliminary functions, read_spectra and bin_spectra
            #Have not yet accounted for input R as formula or spectral grasp
#KO/LK 3/29: Met study hall to discuss progress/next steps 
#KO/LK 4/4: Met study hall to regrid_spectra
#KO/LK 4/5: Met study hall to revise regrid_spectra

def read_spectra(specfile='lte03800-4.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits',
                 wavefile='WAVE_PHOENIX-ACES-AGSS-COND-2011.fits', plot=True):
     spec,spech = fits.getdata(specfile,header=True)
     wave,waveh = fits.getdata(wavefile,header=True)
     if plot:
         plt.ion()
         plt.figure(1)
         plt.clf()
         plt.plot(wave,spec)
                        
     return spec, wave

def regrid_spectra(specfile='lte03800-4.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits',
                 wavefile='WAVE_PHOENIX-ACES-AGSS-COND-2011.fits',R=550):
    spec = fits.getdata(specfile)
    wave = fits.getdata(wavefile)
    #wave_log = np.append(wave,np.log(wave))
    inds, = np.where((wave >= 5400) & (wave <= 10000))
    startwave = 5400
    stopwave = 10000
    lnwave = np.linspace(np.log(startwave),np.log(stopwave),len(wave))
    wave_logspace = np.exp(lnwave)
    wave_interpolate = interpolate.interp1d(wave_logspace, spec)
    plt.figure(5)
    plt.plot(wave_interpolate,spec,'r-')
    plt.xlim(np.min(wave[inds]),np.max(wave[inds])) 
    
    return wave_logspace, spec

def bin_spectra(specfile='lte03800-4.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits',
                 wavefile='WAVE_PHOENIX-ACES-AGSS-COND-2011.fits', R=550):
    spec = fits.getdata(specfile)
    wave = fits.getdata(wavefile)
    inds, = np.where((wave >= 5400) & (wave <= 10000))
    plt.figure(3)
    plt.clf()
    plt.plot(wave[inds],spec[inds])
    dl = np.median(wave[inds])/R
    num = np.int(np.round((np.max(wave[inds])-np.min(wave[inds]))/dl))
    wave_resamp = []
    spec_resamp = []
    for i in range(num):
        try:
            bin, = np.where( (wave >= np.min(wave[inds])+ dl*i) &
                      (wave < np.min(wave[inds]) + dl*(i+1)) )
            wave_resamp = np.append(wave_resamp,np.mean(wave[bin]))
            spec_resamp = np.append(spec_resamp,np.mean(spec[bin]))
        except:
            print 'Skipping iteration '+str(i)
    plt.figure(2)
    plt.plot(wave_resamp,spec_resamp,'r-')
    plt.xlim(np.min(wave[inds]),np.max(wave[inds])) 
    
    return wave_resamp, spec_resamp
        

# Load synthetic spectrum
#specfile = 'lte03800-4.50-0.0.PHOENIX-ACES-AGSS-COND-2011-HiRes.fits'
#spec,spech = fits.getdata(specfile,header=True)

# Load corresponding wavelength file
#wavefile = 'WAVE_PHOENIX-ACES-AGSS-COND-2011.fits'
#wave,waveh = fits.getdata(wavefile,header=True)

# Plot the entire spectrum
#plt.ion()
#plt.figure(1)
#plt.clf()
#plt.plot(wave,spec)

# Spectral grasp of FLOYDS
#inds, = np.where((wave >= 5400) & (wave <= 10000))
#plt.figure(2)
#plt.clf()
#plt.plot(wave[inds],spec[inds])

# Floyds specifications
#R = 550 # Resolution = lambda over delta lambda
#dl = np.median(wave[inds])/R
# Number of resolution elements across spectrum
#num = np.int(np.round((np.max(wave[inds])-np.min(wave[inds]))/dl))

# Resample spectrum to the resolution of Floyds
#wave_resamp = []
#spec_resamp = []
#for i in range(num):
    #try:
     #   bin, = np.where( (wave >= np.min(wave[inds])+ dl*i) &
      #                (wave < np.min(wave[inds]) + dl*(i+1)) )
       # wave_resamp = np.append(wave_resamp,np.mean(wave[bin]))
        #spec_resamp = np.append(spec_resamp,np.mean(spec[bin]))
    #except:
     #   print 'Skipping iteration '+str(i)

# Overplot the resampled spectrum
#plt.figure(2)
#plt.plot(wave_resamp,spec_resamp,'r-')
#plt.xlim(np.min(wave[inds]),np.max(wave[inds]))

