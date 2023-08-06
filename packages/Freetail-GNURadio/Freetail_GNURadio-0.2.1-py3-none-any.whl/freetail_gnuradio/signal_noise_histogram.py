import numpy as np
from scipy import stats

from gnuradio import gr
import pmt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtWidgets

class signal_noise_histogram(gr.sync_block, FigureCanvasQTAgg):  # other base classes are basic_block, decim_block, interp_block
    """Calculate histograms for signal and noise
    """

    def __init__(self, target_time: float, noise_time: float, samples_per_pulse: int, samp_rate: float, num_pulses: int):
        gr.sync_block.__init__(
            self,
            name='Signal and Noise Histrograms',
            in_sig=[np.float32],
            out_sig=[np.float32],
        )

        self.target_index = int(np.round(target_time*samp_rate))
        self.noise_index = int(np.round(noise_time*samp_rate))
        self.samp_rate = samp_rate

        self.samples_per_pulse = samples_per_pulse
        self.set_output_multiple(samples_per_pulse) # ensure that requested output size is at least one entire buffer

        self.num_bins = 25
        self.num_fit_points = 200

        fig = Figure()
        self.axes = fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, fig)
        fig.set_tight_layout(True)
        self.target_plot = self.axes.bar(np.arange(self.num_bins), np.zeros(self.num_bins), align='edge', label='Target Measured', color='Coral')
        self.noise_plot = self.axes.bar(np.arange(self.num_bins), np.zeros(self.num_bins), align='edge', label='Noise Measure', color='DarkSeaGreen')
        self.plot_text = self.axes.text(0.5, 0.5, "Press button to start collecting data", horizontalalignment='center', 
                                        verticalalignment='center', transform=self.axes.transAxes)

        self.axes.set_xlabel('Signal level (linear)')
        self.axes.set_ylabel('Estimated PDF')
        
        self.target_fit_plot, = self.axes.plot(np.arange(self.num_fit_points), np.zeros(self.num_fit_points), label='Target Fitted', color='Crimson')
        self.noise_fit_plot, = self.axes.plot(np.arange(self.num_fit_points), np.zeros(self.num_fit_points), label='Noise Fitted', color='DarkGreen')

        self.message_port_register_in(pmt.intern("update"))
        self.set_msg_handler(pmt.intern("update"), self.toggle_update)

        self.target_fit_plot.set_visible(False)
        self.noise_fit_plot.set_visible(False)

        self.num_pulses = num_pulses

    def set_num_pulses(self, num_pulses):
        self.num_pulses = num_pulses

    def set_target_time(self, target_time):
        self.target_index = int(np.round(target_time*self.samp_rate))

    def set_noise_time(self, noise_time):
        self.noise_index = int(np.round(noise_time*self.samp_rate))

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

            for patch in self.noise_plot.patches:
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
        from Freetail module
        """

        self.target_values = np.array(self.target_values)
        self.noise_values = np.array(self.noise_values)

        heights, bins = np.histogram(self.target_values, bins=self.num_bins, density=True)

        for count, patch in enumerate(self.target_plot.patches):
            patch.set_height(heights[count])
            patch.set_x(bins[count])
            patch.set_width(bins[count+1]-bins[count])

        dist_target = stats.rice(*stats.rice.fit(self.target_values, floc=0))
        x = np.linspace(dist_target.mean()-4*dist_target.std(), dist_target.mean()+4*dist_target.std(), self.num_fit_points)
        y = dist_target.pdf(x,)

        self.target_fit_plot.set_xdata(x)
        self.target_fit_plot.set_ydata(y)
        self.target_fit_plot.set_visible(True)

        heights, bins = np.histogram(self.noise_values, bins=self.num_bins, density=True)

        for count, patch in enumerate(self.noise_plot.patches):
            patch.set_height(heights[count])
            patch.set_x(bins[count])
            patch.set_width(bins[count+1]-bins[count])

        dist_noise = stats.rayleigh(*stats.rayleigh.fit(self.noise_values, floc=0))
        x = np.linspace(0, dist_noise.mean()+4*dist_noise.std(), self.num_fit_points)
        y = dist_noise.pdf(x)

        self.noise_fit_plot.set_xdata(x)
        self.noise_fit_plot.set_ydata(y)
        self.noise_fit_plot.set_visible(True)

        self.plot_text.set_text("")

        self.axes.legend()
        self.axes.relim()
        self.axes.autoscale_view()
        self.draw()


    def work(self, input_items, output_items):

        if self.pulse_collection_count > 0 and self.updating:
            self.target_values.append(np.abs(input_items[0][self.target_index]))
            self.noise_values.append(np.abs(input_items[0][self.noise_index]))

            self.pulse_collection_count -= 1

            if self.pulse_collection_count == 0:
                # we just collected the last pulse, so plot the data
                self.update_plot()
                self.updating = False

        output_items[0][:self.samples_per_pulse] = input_items[0][:self.samples_per_pulse]

        self.add_item_tag(0, self.nitems_written(0)+self.target_index, pmt.intern("range"), pmt.intern("target"))
        self.add_item_tag(0, self.nitems_written(0)+self.noise_index, pmt.intern("range"), pmt.intern("noise"))

        return self.samples_per_pulse

