import numpy as np

"Define waveforms that can be used by transmitter and matched filter"

def rectangular_pulse(samp_rate: float, tau: float):
    """pulse_waveform: Create a rectangular pulse

    samp_rate: Sample rate of waveform
    tau: length of pulse (ideally should be a multiple of 1/f_0)
    """

    num_samples = int(np.round(tau*samp_rate))
    x = np.ones(num_samples)

    return np.array(x, dtype=np.float32)

def chirped_pulse(samp_rate: float, T_un: float, delta_f: float):
    """Generate complex frequency modulated pulse
    
    samp_rate: Sample rate of the waveform
    T_un: Uncompressed pulse width
    delta_f: Frequency range of the chirp
    """

    num_points = int(np.round(T_un*samp_rate))

    chirp_rate = 2*np.pi*delta_f/T_un
    t = np.arange(num_points)/samp_rate

    # The phase of the linear chirp;
    phase_t = chirp_rate*(t-0.5*T_un)**2/2

    return np.exp(1j*phase_t)

def matched_filter_taps(waveform):
    """Find match filter taps corresponding to a waveform
    by reversing its order, and normalize maximum gain to 1"""
    
    return np.flip(waveform.conj())/(np.sum(abs(waveform)))

