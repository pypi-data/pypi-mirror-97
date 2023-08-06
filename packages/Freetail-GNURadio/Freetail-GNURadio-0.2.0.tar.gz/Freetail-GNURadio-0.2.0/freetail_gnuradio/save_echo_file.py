import numpy as np

from gnuradio import gr
import pmt

class save_echo_file(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    "Save one echo's worth of data to a file"

    def __init__(self, samp_rate: int, samples_per_pulse: int, filename: str, header: str):
        gr.sync_block.__init__(
            self,
            name='Save echo to file',
            in_sig=[np.float32],
            out_sig=None
        )

        self.set_filename(filename)
        self.samples_per_pulse = samples_per_pulse

        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

        self.message_port_register_in(pmt.intern("write_data"))
        self.set_msg_handler(pmt.intern("write_data"), self.write_data)

        self.time_data = np.arange(samples_per_pulse)/samp_rate
        self.header = header


    def start(self):
        self.write_requested = False

    def write_data(self, msg):
        self.write_requested = True

    def set_filename(self, filename):
        self.filename = filename

    def work(self, input_items, output_items):

        if self.write_requested:
            
            np.savetxt(self.filename, np.stack((self.time_data, input_items[0][:self.samples_per_pulse]), axis=1),
            delimiter=', ', header=self.header, comments='')

            self.write_requested = False

        return self.samples_per_pulse

