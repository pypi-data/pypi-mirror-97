"""
Collection of functions meant to be used for simple data-analysis tasks.

"""
import numpy as np
import scipy
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt

def whiten(strain, interp_psd, dt, phase_shift=0, time_shift=0):
    """Whitens strain data given the psd and sample rate, also applying a phase
    shift and time shift.

    Args:
        strain (ndarray): strain data
        interp_psd (interpolating function): function to take in freqs and output 
            the average power at that freq 
        dt (float): sample time interval of data
        phase_shift (float, optional): phase shift to apply to whitened data
        time_shift (float, optional): time shift to apply to whitened data (s)
    
    Returns:
        ndarray: array of whitened strain data
    """
    Nt = len(strain)
    # take the fourier transform of the data
    freqs = np.fft.rfftfreq(Nt, dt)

    # whitening: transform to freq domain, divide by square root of psd, then
    # transform back, taking care to get normalization right.
    hf = np.fft.rfft(strain)
    
    # apply time and phase shift
    hf = hf * np.exp(-1.j * 2 * np.pi * time_shift * freqs - 1.j * phase_shift)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht

def bandpass(strain, fband, fs):
    """Bandpasses strain data using a butterworth filter.
    
    Args:
        strain (ndarray): strain data to bandpass
        fband (ndarray): low and high-pass filter values to use
        fs (float): sample rate of data
    
    Returns:
        ndarray: array of bandpassed strain data
    """
    bb, ab = butter(4, [fband[0]*2./fs, fband[1]*2./fs], btype='band')
    normalization = np.sqrt((fband[1]-fband[0])/(fs/2))
    strain_bp = filtfilt(bb, ab, strain) / normalization
    return strain_bp

def next_power_of_2(x):
    """
    Silly functions to obtain the 'next power of 2' for any given
    number. It is useful for padding befor the computing
    the Welch's PSD.
    """  
    return 1 if x == 0 else 2**(x - 1).bit_length()


def taper(data, fs=1, side='leftright', duration=None, nsamples=None, window='tukey',**winkwgs):
    """Taper the ends of data smoothly to zero. Inspired by gwpy function
    Parameters
    ----------
    side : `str`, optional
        the side of the data to taper, must be one of `'left'`,
        `'right'`, or `'leftright'`
    duration : `float`, optional
        the duration of time to taper, will override `nsamples`
        if both are provided as arguments
    nsamples : `int`, optional
        the number of samples to taper, will be overridden by `duration`
        if both are provided as arguments
        
    Returns
    -------
    out : out_data
        a copy of data tapered at one or both ends
    Raises
    ------
    ValueError
        if `side` is not one of `('left', 'right', 'leftright')`
    """
    # check window properties
    if side not in ('left', 'right', 'leftright'):
        raise ValueError("side must be one of 'left', 'right', or 'leftright'")
        
    if duration:
        nsamples = int(duration * fs)
        
    out = data.copy()
    # if a duration or number of samples is not specified, automatically
    # identify the second stationary point away from each boundary,
    # else default to half the data width
    nleft, nright = 0, 0
    if not nsamples:
        mini, = signal.argrelmin(out)
        maxi, = signal.argrelmax(out)
        
    if 'left' in side:
        nleft = nsamples or max(mini[0], maxi[0])
        nleft = min(nleft, int(data.size/2))
    if 'right' in side:
        nright = nsamples or out.size - min(mini[-1], maxi[-1])
        nright = min(nright, int(data.size/2))
    
    # Define the window
    win_len = (nleft or 0)+(nright or 0)
    
    if winkwgs:
        win_par = ",".join([f"{k}={l}" for k, l in winkwgs.items()])
    else:
        win_par = ''
    
    
    win_func = eval("scipy.signal.windows.{}({}, {})".format(window, win_len, win_par))
    
    out[:(nleft or 0)] *= win_func[:(nleft or 0)]
    out[-(nright or 0):] *= win_func[-(nright or 0):]

    return out

# def psd

#         # number of sample for the fast fourier transform:
#         NFFT = 4 * fs
#         NOVL = -1 * NFFT / 2
#         psd_window = scipy.signal.tukey(NFFT, alpha=1./4)

#         Pxx_H1, freqs = mlab.psd(strain_H1[indxt_around], Fs=fs, NFFT=NFFT,
#                                  window=psd_window, noverlap=NOVL)
#         Pxx_L1, freqs= mlab.psd(strain_L1[indxt_around], Fs=fs, NFFT=NFFT, 
#                                 window=psd_window, noverlap=NOVL)

#         if (plot_others):
#             # smaller window if we're not doing Welch's method
#             short_indxt_away = np.where((time >= time_center - 2) & (
#                 time < time_center + 2))
#             # psd using a tukey window but no welch averaging
#             tukey_Pxx_H1, tukey_freqs = mlab.psd(
#                 strain_H1[short_indxt_away], Fs=fs, NFFT=NFFT, window=psd_window)
#             # psd with no window, no averaging
#             nowin_Pxx_H1, nowin_freqs = mlab.psd(
#                 strain_H1[short_indxt_away], Fs=fs, NFFT=NFFT, 
#                 window=mlab.window_none)

#         # We will use interpolations of the PSDs computed above for whitening:
#         psd_H1 = interp1d(freqs, Pxx_H1)
#         psd_L1 = interp1d(freqs, Pxx_L1)

#
#
#	Npt = int(infs/outfs)           # Number of samples per each segment: infs/outfs= infs*Tout
# 	Nsamples = int(len(signl)/float(Npt)) # Number of segments which the total data frame is divided into
# 	Npseg =  int(Npt/navrg)          # Number of points to include in each fft per segment
# 	Nfft = next_power_of_2(Npseg)

# 	if verbose: print("Npt: {}\nNsamples: {}\nNfft: {}".format(Npt,Nsamples,Nfft))

# 	idx = np.arange(0,Nsamples)*Npt
# 	t = np.arange(0,Nsamples)/outfs

# 	if not isinstance(bands[0],list): bands = [bands]

# 	Nbands = len(bands)

# 	# Initialize BLRMS matrix: (time vector) * (n. bands)
# 	b = np.zeros((len(t), Nbands))

	
# 	if verbose: print('PSD computation for each segment...\n frequency resolution: ',outfs*navrg,'Hz')
# 	# loop over each segment of data

# 	if nproc < 2:
# 	    for i,j in enumerate(idx):
# 	        # compute PSD
# 	        # Same as above
# 	        fr, sx = signal.welch(signl[j:j+Npt], window ='blackman', fs=infs,
# 					noverlap = Npseg/2,  nfft=Nfft, nperseg=Npseg)#, average = 'mean')