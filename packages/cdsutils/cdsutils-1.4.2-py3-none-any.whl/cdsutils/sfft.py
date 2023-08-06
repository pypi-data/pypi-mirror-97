"""
Implements a single-frequency Fourier transform by Clenshaw's
algorithm.

"""

__docformat__ = 'restructuredtext'

import numpy as _n
from scipy import weave as _weave
from matplotlib import cbook as _cbook
from matplotlib.mlab import window_hanning, detrend_none


class SFFT(object):
    def __init__(self, freq, Fs=None, allow_phaseshift=True):
        self.freq = freq
        self.rate = Fs
        self.s1 = 0
        self.s2 = 0
        self.n = 0
        self.allow_phaseshift = allow_phaseshift
        self.first = True

    def apply(self, data):
      if self.first:
          if not self.rate:
              if not hasattr(data, 'info') and 'rate' in data.info:
                  raise ValueError("sampling rate not specified")
              # try to use sampling rate specified in the data (if it's an InfoArray)
              self.rate = data.info['rate']
          self.nf = 2*_n.pi*self.freq/float(self.rate) # normalized frequency
          if self.allow_phaseshift \
             and (_n.fmod(self.nf, _n.pi) + _n.pi/4. < _n.pi/2.):
              # for nf outside (pi/4, 3*pi/4), a phase shift is supposed to
              # improve the numerical stability of the algorithm
              # see Newbery, Mathematics of Computation 27 p. 639 (1973)
              # with double precision, this seems to matter very little in practice
              self.phaseshifted = 1
              self.nf = _n.pi/2. + self.nf
          else:
              self.phaseshifted = 0
          self.cosnf = _n.cos(self.nf)
          self.sinnf = _n.sin(self.nf)
          self.coeff = 2*self.cosnf
          self.first = False

      datalen = int(len(data))
      phaseshifted = int(self.phaseshifted)
      coeff = float(self.coeff)
      xre = _n.array(data.real, dtype='d')
      xim = _n.array(data.imag, dtype='d')
      sre = _n.array([_n.real(self.s1), _n.real(self.s2)], dtype='d')
      sim = _n.array([_n.imag(self.s1), _n.imag(self.s2)], dtype='d')
      code = """
double sre0, sim0;
if (phaseshifted) {
    for (int n=0; n < datalen; n++) {
        switch (n % 4) {
            case 0:
                sre0 =  xre(n) + coeff*sre(0) - sre(1);
                sim0 = -xim(n) + coeff*sim(0) - sim(1);
                break;
            case 1:
                sre0 =  xim(n) + coeff*sre(0) - sre(1);
                sim0 =  xre(n) + coeff*sim(0) - sim(1);
                break;
            case 2:
                sre0 = -xre(n) + coeff*sre(0) - sre(1);
                sim0 =  xim(n) + coeff*sim(0) - sim(1);
                break;
            case 3:
                sre0 = -xim(n) + coeff*sre(0) - sre(1);
                sim0 = -xre(n) + coeff*sim(0) - sim(1);
                break;
        }
        sre(1) = sre(0);
        sim(1) = sim(0);
        sre(0) = sre0;
        sim(0) = sim0;
    }
}
else {
    for (int n=0; n < datalen; n++) {
        sre0 = xre(n) + coeff*sre(0) - sre(1);
        sim0 = xim(n) + coeff*sim(0) - sim(1);
        sre(1) = sre(0);
        sim(1) = sim(0);
        sre(0) = sre0;
        sim(0) = sim0;
    }
}
"""

      if True:
          _weave.inline(code, ['datalen', 'phaseshifted', 'coeff', 'xre', 'xim',
                               'sre', 'sim'],
                        type_converters=_weave.converters.blitz)
          self.s1 = sre[0] + 1j*sim[0]
          self.s2 = sre[1] + 1j*sim[1]

      if False:
          for n, x in enumerate(data.flat):
              if self.phaseshift:
                  if n % 4 == 0:
                      x =  _n.real(x) - 1j*_n.imag(x)
                  elif n % 4 == 1:
                      x =  _n.imag(x) + 1j*_n.real(x)
                  elif n % 4 == 2:
                      x = -_n.real(x) + 1j*_n.imag(x)
                  elif n % 4 == 3:
                      x = -_n.imag(x) - 1j*_n.real(x)
              s0 = x + self.coeff*self.s1 - self.s2
              self.s2 = self.s1
              self.s1 = s0

      self.n += len(data)
      re = self.s1 - self.s2*self.cosnf
      im = self.s2 * self.sinnf
      return (re + 1j*im)*_n.exp(-1j*self.nf*(self.n-1))*2/float(self.n)


def sfft(data, freq, Fs=None, allow_phaseshift=True):
    return SFFT(freq, Fs=Fs, allow_phaseshift=allow_phaseshift).apply(data)


def sfpsd(x, freq, NFFT=256, res=None, Fs=None, detrend=detrend_none,
          window=window_hanning, noverlap=0, overlap=None, norm=True):
    """Single frequency power spectral density estimate.

    Returns ``(Pxx, freq)`` as a tuple.

    See `matplotlib.mlab.psd` for more details.

    :Parameters:
    norm : bool
      If ``True``, the result is normalized in the same way that DTT
      displays it (single-sided amplitude rms per rtHz).  Otherwise
      it's double-sided mean squared amplitude per bin.

    """
    if not Fs:
        if not hasattr(x, 'info') and 'rate' in x.info:
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        Fs = x.info['rate']
    if res is not None:
        NFFT = int(Fs/res)
    if overlap is not None:
        noverlap = int(NFFT*overlap)
    x = _n.asarray(x)

    if len(x) < NFFT:
        n = len(x)
        x = _n.resize(x, (NFFT,))
        x[n:] = 0

    if _cbook.iterable(window):
        assert(len(window) == NFFT)
        windowVals = window
    else:
        windowVals = window(_n.ones((NFFT,), x.dtype))
    step = NFFT - noverlap
    ind = list(range(0, len(x)-NFFT+1, step))
    n = len(ind)
    Pxx = _n.zeros(n, _n.float_)
    for i in range(n):
        thisx = x[ind[i]:ind[i]+NFFT]
        thisx = windowVals * detrend(thisx)
        # NFFT/2.: convert back to double-sided mean squared amplitude per bin,
        # undoing the conversion to raw amplitude in SFFT
        fx = _n.absolute(sfft(thisx, freq, Fs=Fs)*NFFT/2.)**2
        Pxx[i] = fx
  
    if n > 1:
        Pxx = Pxx.mean()

    Pxx /= (_n.abs(windowVals)**2).sum()

    if norm:
        return _n.sqrt(2*Pxx/Fs), freq
    else:
        return Pxx, freq


def sfcsd(x, y, freq, NFFT=256, res=None, Fs=None, detrend=detrend_none,
          window=window_hanning, noverlap=0, overlap=None, norm=True):
    """Single frequency cross spectral density estimate.

    Returns ``(Pxy, freq)`` as a tuple.

    See `matplotlib.mlab.csd` for more details.

    :Parameters:
    norm : bool
      If ``True``, the result is normalized in the same way that DTT
      displays it (single-sided mean squared amplitude per Hz).
      Otherwise it's double-sided mean squared amplitude per bin.

    """
    if not Fs:
        if (not hasattr(x, 'info') and 'rate' in x.info) \
           or (not hasattr(y, 'info') and 'rate' in y.info):
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        if x.info['rate'] != y.info['rate']:
            raise ValueError("sampling rates differ")
        Fs = x.info['rate']
    if res is not None:
        NFFT = int(Fs/res)
    if overlap is not None:
        noverlap = int(NFFT*overlap)
    x = _n.asarray(x)
    y = _n.asarray(y)

    if len(x) < NFFT:
        n = len(x)
        x = _n.resize(x, (NFFT,))
        x[n:] = 0
    if len(y) < NFFT:
        n = len(y)
        y = _n.resize(y, (NFFT,))
        y[n:] = 0

    if _cbook.iterable(window):
        assert(len(window) == NFFT)
        windowVals = window
    else:
        windowVals = window(_n.ones((NFFT,), x.dtype))
    step = NFFT - noverlap
    ind = list(range(0, len(x)-NFFT+1, step))
    n = len(ind)
    Pxy = _n.zeros(n, _n.complex_)

    for i in range(n):
        thisx = x[ind[i]:ind[i]+NFFT]
        thisx = windowVals*detrend(thisx)
        thisy = y[ind[i]:ind[i]+NFFT]
        thisy = windowVals*detrend(thisy)
        # NFFT/2.: convert back to double-sided mean squared amplitude per bin,
        # undoing the conversion to raw amplitude in SFFT
        fx = sfft(thisx, freq, Fs=Fs)*NFFT/2.
        fy = sfft(thisy, freq, Fs=Fs)*NFFT/2.
        Pxy[i] = _n.conjugate(fx)*fy

    if n > 1:
        Pxy = Pxy.mean()

    Pxy /= (_n.abs(windowVals)**2).sum()
    if norm:
        return 2*Pxy/Fs, freq
    else:
        return Pxy, freq


def sftfe(x, y, freq, NFFT=256, res=None, Fs=None, detrend=detrend_none,
          window=window_hanning, noverlap=0, overlap=None):
    """Single frequency transfer function estimate.

    Returns ``(Pxy/Pxx, freq)`` as a tuple.

    """
    if not Fs:
        if (not hasattr(x, 'info') and 'rate' in x.info) \
           or (not hasattr(y, 'info') and 'rate' in y.info):
            raise ValueError("sampling rate not specified")
        # try to use sampling rate specified in the data (if it's an InfoArray)
        if x.info['rate'] != y.info['rate']:
            raise ValueError("sampling rates differ")
        Fs = x.info['rate']
    if res is not None:
        NFFT = int(Fs/res)
    if overlap is not None:
        noverlap = int(NFFT*overlap)
    Pxy, freq = sfcsd(x, y, freq, NFFT=NFFT, Fs=Fs, detrend=detrend,
                      window=window, noverlap=noverlap, norm=False)
    Pxx, freq = sfpsd(x, freq, NFFT=NFFT, Fs=Fs, detrend=detrend,
                      window=window, noverlap=noverlap, norm=False)
    return _n.divide(Pxy, Pxx), freq


_coh_error = """Coherence is calculated by averaging over NFFT
length segments.  Your signal is too short for your choice of NFFT.
"""
def sfcohere(x, y, freq, NFFT=256, res=None, Fs=None, detrend=detrend_none,
             window=window_hanning, noverlap=0, overlap=None):
    """Coherence function (normalized cross spectral density estimate).

    Returns ``(Cxy, freq)`` as a tuple.

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
    if res is not None:
        NFFT = int(Fs/res)
    if overlap is not None:
        noverlap = int(NFFT*overlap)
    if len(x) < 2*NFFT:
        raise ValueError(_coh_error)
    Pxx, freq = sfpsd(x, freq, NFFT=NFFT, Fs=Fs, detrend=detrend,
                      window=window, noverlap=noverlap, norm=False)
    Pyy, freq = sfpsd(y, freq, NFFT=NFFT, Fs=Fs, detrend=detrend,
                      window=window, noverlap=noverlap, norm=False)
    Pxy, freq = sfcsd(x, y, freq, NFFT=NFFT, Fs=Fs, detrend=detrend,
                      window=window, noverlap=noverlap, norm=False)
    Cxy = _n.divide(_n.absolute(Pxy)**2, Pxx*Pyy)
    return Cxy, freq
