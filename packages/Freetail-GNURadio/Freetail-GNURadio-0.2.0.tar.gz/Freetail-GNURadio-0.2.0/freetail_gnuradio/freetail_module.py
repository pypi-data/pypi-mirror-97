import numpy as np

from gnuradio import gr
import pmt

import serial
import serial.tools.list_ports

header = [b'\x7A', b'\x7A']
usb_id_regex = ".*16C0:0483.*" # Regex containing USB VID:PID of Teensy in Serial mode

def open_freetail_module(firmware_version):
    "Find the serial port with the Freetail module and open it"

    correct_serial = None

    for port in serial.tools.list_ports.grep(usb_id_regex):
        ser = serial.Serial(port.device, timeout=1)
        ser.write(b'I')
    
        if ser.readline().decode().strip() != 'Freetail':
            ser.close()
            continue

        if ser.readline().decode().strip() == firmware_version:
            # found correct version
            correct_serial = ser
            break
        else:
            ser.close()
            raise ValueError(f"Freetail module has the wrong firmware version. Please upload version {firmware_version}")

    if correct_serial is None:
        raise ValueError("Freetail module not found")
    
    return ser

def write_waveform(ser, tx_waveform):
    "Write the waveform to the Freetail module"
    ser.write(b'W')
    ser.write(len(tx_waveform).to_bytes(2, 'little'))
    ser.write(tx_waveform.tobytes())
    if ser.readline().strip() != b"OK":
        raise ValueError("Could not write transmit waveform")

maximum_value: int = 2048
bias_value: int = 2048
DAC_max = 4095.0

class freetail_module(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Freetail Module
    
    Configure the transmit waveform of the Freetail module, and read the
    received waveform.
    """

    def __init__(self, waveform, 
                f_0: float, samp_rate: float, samples_per_pulse: int, duplexer_time: float):
        """
        waveform: The sampled baseband waveform that the module will use to modulate its transmission
        f_0: Centre frequency, should match the physical hardware
        samp_rate: Sample rate, should match that used by the module
        samples_per_pulse: How many samples between each pulse. This determintes the PRF
        duplexer_time: The received signal up to this time will be zeroed out, to simulate
        the operation of a duplexer, to prevent receiving the transmitted waveform.
        """
        gr.sync_block.__init__(
            self,
            name='Freetail module',
            in_sig=None,
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.maximum_value = maximum_value
        self.bias_value = bias_value

        t = np.arange(len(waveform))/samp_rate
        modulated_waveform = (waveform*np.exp(2j*np.pi*f_0*t)).real

        # pad out the waveform with zeros to the required length
        padding_samples = samples_per_pulse-len(waveform)
        assert(padding_samples > 0)
        padded_waveform = np.pad(modulated_waveform+1, (0, padding_samples)) # pad to full PRI length
        self.waveform =  np.array(padded_waveform.real*(DAC_max)/2, dtype=np.uint16) # store corresponding integer waveform

        self.blank_samples = int(duplexer_time*samp_rate)

        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

    def start(self):
        "Open serial port, set waveform, start receiving values"
        self.ser = open_freetail_module("v3")
        write_waveform(self.ser, self.waveform)
        self.ser.write(b'B')

        self.data_rf = None
        
    def work(self, input_items, output_items):
        "Get data from serial port"

        # Reading header. TODO: Timeout if header not found
        while (self.ser.read() != header[0]):
            pass
        while (self.ser.read() != header[1]):
            pass

        read_size = int.from_bytes(self.ser.read(2), 'little')
        buffer = self.ser.read(read_size*2)

        if read_size != len(self.waveform):
            # This is old data, with different waveform settings. Discard it
            return 0

        assert(read_size <= len(output_items[0]))

        # Convert to float, remove bias and scale to range -1.0 to +1.0
        output_items[0][:read_size] = (np.array(np.frombuffer(buffer, dtype='uint16'), dtype=np.float32)-self.bias_value)/self.maximum_value

        # tag the point in data stream corresponding to the start of transmission
        self.add_item_tag(0, self.nitems_written(0), pmt.intern("tx_start"), pmt.to_pmt(0))
        #self.add_item_tag(0, self.nitems_written(0)+self.blank_samples, pmt.intern("rx_start"), pmt.to_pmt(0))

        # Blank the data to simulate duplexer
        output_items[0][:self.blank_samples] = 0.0

        return read_size
        
    def stop(self):
        "Close serial port at end of sim"
        self.ser.close()
