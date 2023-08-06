"""
Library of DTT-style spectral tools.

"""

import numpy, matplotlib.mlab as m
from matplotlib.mlab import detrend_none, window_hanning
from matplotlib import cbook

__docformat__ = 'restructuredtext'


def psd(x, NFFT=256, res=None, Fs=None, detrend=detrend_none,
        window=window_hanning, noverlap=0, overlap=None, norm=True):
    """
    Power spectral density estimate.

    Returns ``(Pxx, freqs)`` as a tuple.

    See `matplotlib.mlab.psd` for more details.

    :Parameters:
      norm : bool
        If ``True``, the result is normalized in the same way that DTT
        displays it (single-sided amplitude rms per rtHz).  Otherwise
        it's single-sided mean squared amplitude per Hz.

    """
    if not Fs:
        if not hasattr(x, 'info') and 'rate' in x.info:
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        Fs = x.info['rate']
    if res is not None: NFFT = int(Fs/res)
    if overlap is not None: noverlap = int(NFFT*overlap)
    Pxx, f = m.psd(x, NFFT=NFFT, Fs=Fs, detrend=detrend, window=window,
                   noverlap=noverlap)
    # a misfeature in some versions of mlab returns Pxx with the wrong shape
    Pxx.shape = len(f),
    # m.psd returns single-sided power/Hz
    if norm: return numpy.sqrt(Pxx), f
    else: return Pxx, f


def csd(x, y, NFFT=256, res=None, Fs=None, detrend=detrend_none,
        window=window_hanning, noverlap=0, overlap=None, norm=True):
    """
    Cross spectral density estimate.

    Returns ``(Pxy, freqs)`` as a tuple.

    See `matplotlib.mlab.csd` for more details.

    :Parameters:
      norm : bool
        If ``True``, the result is normalized in the same way that DTT
        displays it (single-sided mean squared amplitude per Hz).
        Otherwise it's single-sided mean squared amplitude per Hz.

    """
    if not Fs:
        if (not hasattr(x, 'info') and 'rate' in x.info) \
               or (not hasattr(y, 'info') and 'rate' in y.info):
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        if x.info['rate'] != y.info['rate']:
            raise ValueError("sampling rates differ")
        Fs = x.info['rate']
    if res is not None: NFFT = int(Fs/res)
    if overlap is not None: noverlap = int(NFFT*overlap)
    Pxy, f = m.csd(x, y, NFFT=NFFT, Fs=Fs, detrend=detrend, window=window,
                   noverlap=noverlap)
    if norm: return Pxy, f
    else: return Pxy, f


def tfe(x, y, NFFT=256, res=None, Fs=None, detrend=detrend_none,
        window=window_hanning, noverlap=0, overlap=None):
    """
    Transfer function estimate.

    Returns ``(Pxy/Pxx, freqs)`` as a tuple.
    
    """
    if not Fs:
        if (not hasattr(x, 'info') and 'rate' in x.info) \
               or (not hasattr(y, 'info') and 'rate' in y.info):
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        if x.info['rate'] != y.info['rate']:
            raise ValueError("sampling rates differ")
        Fs = x.info['rate']
    if res is not None: NFFT = int(Fs/res)
    if overlap is not None: noverlap = int(NFFT*overlap)
    Pxy, f = csd(x, y, NFFT=NFFT, Fs=Fs, detrend=detrend, window=window,
                 noverlap=noverlap, norm=False)
    Pxx, f = psd(x, NFFT=NFFT, Fs=Fs, detrend=detrend, window=window,
                 noverlap=noverlap, norm=False)
    return numpy.divide(Pxy, Pxx), f


def cohere(x, y, NFFT=256, res=None, Fs=None, detrend=detrend_none,
           window=window_hanning, noverlap=0, overlap=None):
    """
    Coherence function (normalized cross spectral density estimate).

    Returns ``(Cxy, freqs)`` as a tuple.

    See `matplotlib.mlab.cohere` for more details.

    """
    if not Fs:
        if (not hasattr(x, 'info') and 'rate' in x.info) \
               or (not hasattr(y, 'info') and 'rate' in y.info):
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        if x.info['rate'] != y.info['rate']:
            raise ValueError("sampling rates differ")
        Fs = x.info['rate']
    if res is not None: NFFT = int(Fs/res)
    if overlap is not None: noverlap = int(NFFT*overlap)
    return m.cohere(x, y, NFFT=NFFT, Fs=Fs, detrend=detrend, window=window,
                    noverlap=noverlap)


class IncrementalSpectrum(object):
    def __init__(self, NFFT=256, res=None, Fs=2, detrend=detrend_none,
                 window=window_hanning, noverlap=0, overlap=None,
                 decay=False, norm=True):
        self.res = res
        self.rate = Fs
        if res is not None: self.nfft = int(self.rate/self.res)
        else:
            self.nfft = NFFT
            self.res = self.rate/float(self.nfft)
        self.detrend = detrend
        self.window = window
        if cbook.iterable(window):
            assert(len(window) == NFFT)
            self.window = window
        else: self.window = window(numpy.ones((self.nfft,)))
        # compute effective noise bandwidth of the window, and hence
        # the effective resolution bandwidth for this spectrum
        # cf. F.J. Harris, Proc. IEEE vol. 66 pp. 51--83
        self.rbw = self.res * len(self.window) * (self.window**2).sum() / \
                   (self.window.sum())**2
        self.overlap = overlap
        if overlap is not None: self.noverlap = int(self.nfft*self.overlap)
        else:
            self.noverlap = noverlap
            self.overlap = self.noverlap/float(self.nfft)
        self.decay = decay
        self.norm = norm
        self.avgcnt = 0

    def _sum(self, oldspect, newspect):
        if self.decay is False:
            old_wt = len(list(range(0, self.nfft*(self.avgcnt-1) + 1, self.noverlap)))
            new_wt = len(list(range(0, self.nfft*(self.newavgcnt-self.avgcnt-1) + self.noverlap + 1, self.noverlap)))
        else:
            old_wt = 1 - self.decay
            new_wt = self.decay
        return ((oldspect*old_wt + newspect*new_wt)/float(old_wt+new_wt))


class PSD(IncrementalSpectrum):
    def apply(self, data):
        # length of each new data block must be a multiple of NFFT
        if len(data) != self.nfft*(len(data)/self.nfft):
            raise BadDataLength(len(data))
        self.newavgcnt = self.avgcnt + len(data)/self.nfft
        # subtlety of incremental averaging: a chunk of old data must
        # be included in the FFT so it can be overlapped with the new data
        if self.avgcnt != 0: data = numpy.concatenate((self.lastoverlap, data))
        newps, freq = psd(data, NFFT=self.nfft, Fs=self.rate,
                          detrend=self.detrend, window=self.window,
                          noverlap=self.noverlap, norm=False)
        if self.avgcnt == 0: self.ps = newps
        else: self.ps = self._sum(self.ps, newps)
        self.lastoverlap = data[-self.noverlap:]
        self.avgcnt = self.newavgcnt
        if self.norm: return numpy.sqrt(self.ps), freq
        else: return self.ps, freq


class CSD(IncrementalSpectrum):
    def apply(self, xdata, ydata):
        # length of each new data block must be a multiple of NFFT
        if (len(xdata) != self.nfft*(len(xdata)/self.nfft)) \
               or (len(ydata) != self.nfft*(len(ydata)/self.nfft)) \
               or (len(xdata) != len(ydata)):
            raise BadDataLength((len(xdata), len(ydata)))
        self.newavgcnt = self.avgcnt + len(xdata)/self.nfft
        # subtlety of incremental averaging: a chunk of old data must
        # be included in the FFT so it can be overlapped with the new data
        if self.avgcnt != 0:
            xdata = numpy.concatenate((self.lastxoverlap, xdata))
            ydata = numpy.concatenate((self.lastyoverlap, ydata))
        newcs, freq = csd(xdata, ydata, NFFT=self.nfft, Fs=self.rate,
                          detrend=self.detrend, window=self.window,
                          noverlap=self.noverlap, norm=False)
        if self.avgcnt == 0: self.cs = newcs
        else: self.cs = self._sum(self.cs, newcs)
        self.lastxoverlap = xdata[-self.noverlap:]
        self.lastyoverlap = ydata[-self.noverlap:]
        self.avgcnt = self.newavgcnt
        if self.norm: return self.cs, freq
        else: return self.cs, freq


class TFE(object):
    def __init__(self, NFFT=256, res=None, Fs=2, detrend=detrend_none,
                 window=window_hanning, noverlap=0, overlap=None,
                 decay=False):
        self.Pxx = PSD(NFFT=NFFT, res=res, Fs=Fs, detrend=detrend,
                       window=window, noverlap=noverlap, overlap=overlap,
                       decay=decay, norm=False)
        self.Pxy = CSD(NFFT=NFFT, res=res, Fs=Fs, detrend=detrend,
                       window=window, noverlap=noverlap, overlap=overlap,
                       decay=decay, norm=False)
        self.nfft = self.Pxx.nfft
        self.res = self.Pxx.res
        self.rate = self.Pxx.rate
        self.detrend = self.Pxx.detrend
        self.window = self.Pxx.window
        self.rbw = self.Pxx.rbw
        self.noverlap = self.Pxx.noverlap
        self.overlap = self.Pxx.overlap
        self.decay = self.Pxx.decay
        self.avgcnt = self.Pxx.avgcnt

    def apply(self, xdata, ydata):
        pxy, f = self.Pxy.apply(xdata, ydata)
        pxx, f = self.Pxx.apply(xdata)
        self.avgcnt = self.Pxx.avgcnt
        return numpy.divide(pxy, pxx), f


class Cohere(object):
    def __init__(self, NFFT=256, res=None, Fs=2, detrend=detrend_none,
                 window=window_hanning, noverlap=0, overlap=None,
                 decay=False):
        self.Pxx = PSD(NFFT=NFFT, res=res, Fs=Fs, detrend=detrend,
                       window=window, noverlap=noverlap, overlap=overlap,
                       decay=decay, norm=False)
        self.Pyy = PSD(NFFT=NFFT, res=res, Fs=Fs, detrend=detrend,
                       window=window, noverlap=noverlap, overlap=overlap,
                       decay=decay, norm=False)
        self.Pxy = CSD(NFFT=NFFT, res=res, Fs=Fs, detrend=detrend,
                       window=window, noverlap=noverlap, decay=decay,
                       norm=False)
        self.nfft = self.Pxx.nfft
        self.res = self.Pxx.res
        self.rate = self.Pxx.rate
        self.detrend = self.Pxx.detrend
        self.window = self.Pxx.window
        self.rbw = self.Pxx.rbw
        self.noverlap = self.Pxx.noverlap
        self.overlap = self.Pxx.overlap
        self.decay = self.Pxx.decay
        self.avgcnt = self.Pxx.avgcnt

    def apply(self, xdata, ydata):
        if len(xdata) < 2*self.nfft:
            raise BadDataLength(len(xdata))
        pxy, f = self.Pxy.apply(xdata, ydata)
        pxx, f = self.Pxx.apply(xdata)
        pyy, f = self.Pxx.apply(xdata)
        self.avgcnt = self.Pxx.avgcnt
        return numpy.divide(numpy.abs(pxy)**2, pxx*pyy), f


class BadDataLength(Exception):
    pass
