import numpy as np
from scipy import stats
import scipy.special
import itertools

from gnuradio import gr
import pmt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtWidgets

# Convert warnings to errors, in order to catch poor fit to Rice PDF
import warnings
warnings.filterwarnings("error")

class target_histogram(gr.sync_block, FigureCanvasQTAgg):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, target_time: float, samples_per_pulse: int, samp_rate: float, num_pulses: int, histogram_filename: str):
        """Calculate histograms for return from a target at chosen return time

        target_time: Return time for the target for which statistics are collected
        """
        gr.sync_block.__init__(
            self,
            name='Target Return Histrogram',
            in_sig=[np.float32],
            out_sig=[np.float32],
        )

        # Set parameters which are fixed
        self.num_bins = 25
        self.num_fit_points = 200
        self.samp_rate = samp_rate
        self.samples_per_pulse = samples_per_pulse
        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

        # Set parameters which can vary at run-time
        self.set_target_time(target_time)
        self.set_histogram_filename(histogram_filename)
        self.set_num_pulses(num_pulses)

        # Create Matplotlib figure, and generate dummy graphs to update later with data
        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        fig.set_tight_layout(True)
        self.target_plot = self.axes.bar(np.arange(self.num_bins), np.zeros(self.num_bins), align='edge', label='Target+Noise Measured', color='Coral')
        self.plot_text = self.axes.text(0.5, 0.5, "Press button to start collecting data", horizontalalignment='center', 
                                        verticalalignment='center', transform=self.axes.transAxes)

        self.axes.set_xlabel('Signal amplitude (linear)')
        self.axes.set_ylabel('Probability density')
        
        self.target_fit_plot, = self.axes.plot(np.arange(self.num_fit_points)*1e-6, np.zeros(self.num_fit_points), label='Target+Noise Fitted', color='Crimson')
        self.noise_fit_plot, = self.axes.plot(np.arange(self.num_fit_points)*1e-6, np.zeros(self.num_fit_points), label='Noise Estimated', color='DarkGreen')

        self.message_port_register_in(pmt.intern("update"))
        self.set_msg_handler(pmt.intern("update"), self.toggle_update)

        self.target_fit_plot.set_visible(False)
        self.noise_fit_plot.set_visible(False)

    def set_num_pulses(self, num_pulses: int):
        self.num_pulses = num_pulses

    def set_target_time(self, target_time: float):
        self.target_index = int(np.round(target_time*self.samp_rate))

    def set_histogram_filename(self, histogram_filename: str):
        self.histogram_filename = str(histogram_filename)

    def toggle_update(self, msg):

        if self.updating:
            # we are already updating, so stop
            self.updating = False
            self.update_plot()
        else:
            # we are about to start updating, so clear the data
            self.target_values = []
            self.noise_values = []
            self.plot_text.set_text(f"Collecting data from {self.num_pulses} pulses")
            for patch in self.target_plot.patches:
                patch.set_height(0)

            self.target_fit_plot.set_visible(False)
            self.noise_fit_plot.set_visible(False)

            self.draw()

            self.pulse_collection_count = self.num_pulses
            self.updating = True

    def start(self):
        self.target_values = []
        self.noise_values = []
        self.updating = False
        self.pulse_collection_count = 0

    def update_plot(self):
        """Update the plot after data collection
        
        Note, this is a long-running calculation which will likely corrupt data gathering
        from Freetail module. This is not a major problem, because corruption occurs
        after the data has been collected.
        """

        # Update measured target returns
        self.target_values = np.array(self.target_values)
        heights, bins = np.histogram(self.target_values, bins=self.num_bins, density=True)

        for count, patch in enumerate(self.target_plot.patches):
            patch.set_height(heights[count])
            patch.set_x(bins[count])
            patch.set_width(bins[count+1]-bins[count])

        # Fit distribution to target+noise
        try:
            # First attempt to fit a Rice distribution

            b, _, sigma = stats.rice.fit(self.target_values, floc=0) # shape (b), loc, scale
            dist_target = stats.rice(b, 0, sigma)
            dist_target.mean() # this will throw an error if the Rice fit is bad
            signal = (b*sigma)**2
            noise = 2*sigma**2

        except RuntimeWarning:
            # Rice fit failed
            # This usually occurs at high SNR where a Gaussian is a good approximation, so use that.

            signal_mag, sigma = stats.norm.fit(self.target_values) # loc, scale
            dist_target = stats.norm(signal_mag, sigma)
            signal = signal_mag**2
            noise = 2*sigma**2

        x_target = np.linspace(dist_target.mean()-4*dist_target.std(), dist_target.mean()+4*dist_target.std(), self.num_fit_points)
        y_target = dist_target.pdf(x_target)

        self.target_fit_plot.set_xdata(x_target)
        self.target_fit_plot.set_ydata(y_target)
        self.target_fit_plot.set_visible(True)

        self.plot_text.set_text(f"Estimated signal amplitude: {np.sqrt(signal):.3e} ({10*np.log10(signal):.1f} dB)\n"
                                f"Estimated noise amplitude: {np.sqrt(noise):.3e} ({10*np.log10(noise):.1f} dB)")

        # Create an estimated distribution of noise only
        dist_noise = stats.rayleigh(0, sigma)
        x_noise = np.linspace(0, dist_noise.mean()+4*dist_noise.std(), self.num_fit_points)
        y_noise = dist_noise.pdf(x_noise)

        self.noise_fit_plot.set_xdata(x_noise)
        self.noise_fit_plot.set_ydata(y_noise)
        self.noise_fit_plot.set_visible(True)

        self.axes.legend()
        self.axes.relim()
        self.axes.autoscale_view()
        self.draw()

        # Save histogram data to file if filename is given
        if len(self.histogram_filename.strip()) != 0:
            bin_centres = 0.5*(bins[1:]+bins[:-1])

            with open(self.histogram_filename, 'w') as outfile:
                outfile.write('Target Level,Target PDF,Noise Level,Noise PDF,Measured Target Level,Measured Target PDF\n')

                # Iterate over arrays of uneven length, replace missing values with empty string
                for fields in itertools.zip_longest(x_target, y_target, x_noise, y_noise, bin_centres, heights, fillvalue=''):
                    outfile.write('{},{},{},{},{},{}\n'.format(*fields))

    def work(self, input_items, output_items):
        "Collect pulses at given return time"

        if self.pulse_collection_count > 0 and self.updating:
            self.target_values.append(np.abs(input_items[0][self.target_index]))

            self.pulse_collection_count -= 1

            if self.pulse_collection_count == 0:
                # we just collected the last pulse, so plot the data
                self.update_plot()
                self.updating = False

        output_items[0][:self.samples_per_pulse] = input_items[0][:self.samples_per_pulse]
        self.add_item_tag(0, self.nitems_written(0)+self.target_index, pmt.intern("range"), pmt.intern("target"))
        return self.samples_per_pulse

