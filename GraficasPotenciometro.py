#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotcat import plotter
import sys
import serial
import time
import _thread as thread


import matplotlib.pyplot as pylab
import random
##if sys.version_info[0] < 3:
##    import thread
##
##else:
##    import _thread as thread
class plotter:

    """plotter initiates a matplotlib plot. This plot is used to plot the
    serial input."""

    def __init__(self, number_of_samples=100, total_plots=1, rows=1,
                 cols=1, y_low_lim=0, y_high_lim=1024,
                 plot_lines=1, names='serial-graph', time_interval=10, figure=1):

        """initializes the figure with the specified number of subplots
           (arg: total_plots)
        """
        
        self.fig = pylab.figure(figure)
        self.currentAxis = []
        
        self.plots = []
        self.lines = []
        if (type(number_of_samples) == int):
            NOS_val = number_of_samples
            number_of_samples = [NOS_val for i in range(total_plots)]

        elif type(number_of_samples) == list and not len(number_of_samples) == total_plots:
            raise ValueError("lenght of list number_of_samples must be equal to total number of plots")

        else:
            pass

        if type(names) == str:
            name_val = names
            names = [name_val for i in range(total_plots)]

        elif type(names) == list and  not len(names) == total_plots:
            raise ValueError("lenght of list of names must be equal to total number of plots")

        else:
            pass

        if (type(y_low_lim) == int):
            y_low_lim_val = y_low_lim
            y_low_lim = [y_low_lim_val for i in range(total_plots)]

        elif type(y_low_lim) == list and not len(y_low_lim) == total_plots:
            raise ValueError("lenght of list y_low_lim must be equal to total number of plots")

        else:
            pass

        if (type(y_high_lim) == int):
            y_high_lim_val = y_high_lim
            y_high_lim = [y_high_lim_val for i in range(total_plots)]

        elif type(y_high_lim) == list and not len(y_high_lim) == total_plots:
            raise ValueError("lenght of list y_high_lim must be equal to total number of plots")

        else:
            pass

        if (type(plot_lines) == int):
            plot_lines_val = plot_lines
            plot_lines = [plot_lines_val for i in range(total_plots)]

        elif type(plot_lines) == list and not len(plot_lines) == total_plots:
            raise ValueError("lenght of list y_high_lim must be equal to total number of plots")

        else:
            pass


        for i in range(total_plots):
            self.currentAxis.append(range(0, number_of_samples[i]))

        
        count = 1
        for i in range(rows):
            for j in range(cols):

                new_plot = self.fig.add_subplot(((rows * 100) + (cols * 10)
                                                 + count))
                for k in range(plot_lines[count-1]):

                    samples = number_of_samples[count -1]
                    new_line = new_plot.plot(self.currentAxis[count-1],
                                         [random.randint(y_low_lim[count-1],
                                                         y_high_lim[count-1])
                                          for i in
                                          range(0, samples)])
                    self.lines.append(new_line)


                #new_plot.axis('off')
                
                new_plot.set_yticklabels([])
                new_plot.set_xticklabels([])
                new_plot.set_ylabel(names[count-1])
                #pylab.title(names[count-1], loc='left', y=1)
                self.plots.append(new_plot) 
                if count == total_plots:
                    break
                count += 1
        #pylab.annotate("some", (1,1))
        self.manager = pylab.get_current_fig_manager()
        self.timer = self.fig.canvas.new_timer(interval=time_interval)

    def set_call_back(self, func):

        """sets callback function for updating the plot.
        in the callback function implement the logic of reading of serial input
        also the further processing of the signal if necessary has to be done
        in this
        callbak function."""

        self.timer.add_callback(func)
        self.timer.start()

    def plot_self(self, func):

        """define your callback function with the decorator @plotter.plot_self.
        in the callback function set the data of lines
        in the plot using self.lines[i][j].set_data(your data)"""

        def func_wrapper():

            func()

            try:

                self.manager.canvas.draw()

            except ValueError as ve:
                print(ve)
                pass

            except RuntimeError as RtE:
                print(RtE)
                pass

            except Exception as e:
                print(e)
                pass

        return func_wrapper

    @staticmethod
    def show():
        pylab.show()


ser = serial.Serial('/dev/ttyUSB0', 9600)
p = plotter(number_of_samples=[300, 300, 300, 300], 
            total_plots=4, 
            rows=4, 
            cols=1, 
            time_interval=5, 
            names=["ECG","EMG","SPO2","GSR"],
            y_low_lim=[0,0,0,0],
            y_high_lim=[1024,1024,1024,1024])


data1 = [0 for i in range(0,300)]
data2 = [0 for i in range(0,300)]
data3 = [0 for i in range(0,300)]
data4 = [0 for i in range(0,300)]


def read_from_serial():
    cont = 0

    while True:

        try:

            temp = ser.readline()
            try:
                cont = cont + 1
                data1.append(int(temp))
                data2.append(int(temp))
                data3.append(int(temp))

                if cont == 50:
                    data4.append(int(temp))                    
                    data4.pop(0)
                    cont = 0
                

                ##[data[i].append(int(temp)/(i+1)) for i in range(4)]
                ##[data[i].pop(0) for i in range(3)]
                data1.pop(0)
                data2.pop(0)
                data3.pop(0)
                time.sleep(0.000001)

                #data.append(int(temp))
                #data.pop(0)
                #time.sleep(0.000001)

            except ValueError:
                pass

        except AttributeError as Ae:
            pass

        except TypeError:
            pass

        except:
            pass


@p.plot_self
def setval():

    p.lines[0][0].set_data(p.currentAxis[0], data1)
    p.lines[1][0].set_data(p.currentAxis[1], data2)
    p.lines[2][0].set_data(p.currentAxis[2], data3)
    p.lines[3][0].set_data(p.currentAxis[3], data4)
    
                           

if __name__ == '__main__':

    thread.start_new_thread(read_from_serial, ())
    p.set_call_back(setval)
    p.fig.set_size_inches(10, 10, forward=True)
    p.fig.subplots_adjust(left=0.02, bottom=0.02, right=0.99, top=0.99, wspace=None, hspace=0)
    p.show()
