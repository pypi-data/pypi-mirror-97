import numpy as np

from gnuradio import gr
import pmt

class pulse_integrator(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Perform coherent or non-coherent integration of N pulses
    
    coherent: If True, perform coherent integration, otherwise non-coherent
    num_pulses: The number of pulses over which to integrate
    samples_per_pulse: Number of samples recorded for each pulse
    normalize_output: Scale the output so that the signal level is approximately unchanged
    """

    def __init__(self, coherent: bool, num_pulses: int, samples_per_pulse: int,
                normalize_output: bool = True):
        gr.sync_block.__init__(
            self,
            name='Pulse Integrator',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        
        self.num_pulses = num_pulses
        self.samples_per_pulse = samples_per_pulse
        self.coherent = coherent

        if normalize_output:
            self.scale_factor = 1/num_pulses
        else:
            self.scale_factor = 1

        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

    def start(self):        
        self.buffer = np.zeros((self.num_pulses, self.samples_per_pulse), np.complex64)
        self.pulse_index = 0

    def work(self, input_items, output_items):
        "Process one pulse's worth of samples"
        assert(len(output_items[0] >= self.samples_per_pulse))
        samples_to_read = self.samples_per_pulse

        # read into the next buffer
        self.buffer[self.pulse_index, :] = input_items[0][0:samples_to_read]

        # integrate and normalize the buffer values to get the output
        if self.coherent:
            output_items[0][:samples_to_read] = np.sum(self.buffer, axis=0)*self.scale_factor
        else:
            output_items[0][:samples_to_read] = np.sqrt(np.sum(np.abs(self.buffer)**2, axis=0)*self.scale_factor)

        self.pulse_index += 1
        if self.pulse_index == self.num_pulses:
            self.pulse_index = 0

        return samples_to_read

