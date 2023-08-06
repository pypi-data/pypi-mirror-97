import numpy as np

from gnuradio import gr
import pmt


class split_gate_tracker(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Split gate Tracker

    Estimates the range to a target from the difference of signal
    strengths within the late and early gates.
    
    Tracking loop gain - controls the speed vs stability of tracking
    Gate width - width of early and late gates, usually set to the pulse width

    Sample rate - the sample rate of incoming data
    Samples per pulse - how many samples are collected per transmitted pulse
    Initial target return time - the initial estimate of the target location
    """

    def __init__(self, gain: float, samp_rate: float, gate_width: float, initial_time: float,
                samples_per_pulse: int):
        """Create a split-gate tracker"""
        gr.sync_block.__init__(
            self,
            name='Split gate Tracker',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )

        self.gain = gain
        self.gate_width = int(np.round(gate_width*samp_rate)) # gate width in samples
        self.range_estimate = int(np.round(initial_time*samp_rate)) # estimated target range in samples
        self.samples_per_pulse = samples_per_pulse

        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

    def work(self, input_items, output_items):
        "Process one pulse's worth of samples"
        assert(len(output_items[0] >= self.samples_per_pulse))

        # create a view to simplify algorithm
        buffer = input_items[0][:self.samples_per_pulse]

        # create early and late gates, ensuring they stay within this pulse
        early_gate = slice(max(0, self.range_estimate-self.gate_width), self.range_estimate)
        late_gate = slice(self.range_estimate, min(self.range_estimate+self.gate_width, self.samples_per_pulse))
        
        # integrate signal within early and late gates, and account for possible differences in gate sizes at ends of pulse
        try:
            late_integral = sum(abs(buffer[late_gate]))/(late_gate.stop-late_gate.start)
        except ZeroDivisionError:
            late_integral = 0

        try:
            early_integral = sum(abs(buffer[early_gate]))/(early_gate.stop-early_gate.start)
        except ZeroDivisionError:
            early_integral = 0

        # tracking error is normalized to amplitude of signal within the two gates
        tracker_error = (late_integral-early_integral)/(late_integral+early_integral)
        # TODO: decide if this normalization is appropriate or not. Probably yes, otherwise tracking performance
        # will depend on distance to target

        # update range estimate
        self.range_estimate = int(self.range_estimate + self.gain*tracker_error)

        # ensure it stays within this pulse
        self.range_estimate = max(self.range_estimate, 0)
        self.range_estimate = min(self.range_estimate, self.samples_per_pulse)

        # tag the output stream
        self.add_item_tag(0, self.nitems_written(0) + int(np.round(self.range_estimate)), pmt.intern("Target"), pmt.to_pmt(0))
        self.add_item_tag(0, self.nitems_written(0) + early_gate.start, pmt.intern("Early Gate"), pmt.to_pmt(0))
        self.add_item_tag(0, self.nitems_written(0) + late_gate.stop, pmt.intern("Late Gate"), pmt.to_pmt(0))

        # copy the output stream
        output_items[0][:self.samples_per_pulse] = buffer
        return self.samples_per_pulse
