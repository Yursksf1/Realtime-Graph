#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from plotcat import plotter
import sys
import serial
import time
import _thread as thread 

#ser = serial.Serial('/dev/ttyACM0', 115200)
filne = "Datos.txt"
ser = open(filne, 'r+')
#print(ser)

root = tk.Tk()
p = plotter(number_of_samples=[1500, 1500, 1500, 1500], total_plots=4, rows=4, cols=1, names=["ECG","EMG","SPO2","GSR"],y_low_lim=0,y_high_lim=1000)

data1 = [0 for i in range(0,1500)]
data2 = [0 for i in range(0,1500)]
data3 = [0 for i in range(0,1500)]
data4 = [0 for i in range(0,1500)]


##data.append([0 for i in range(1500)])
##data.append([0 for i in range(1500)])
##data.append([0 for i in range(1500)])





def read_from_serial():

    while True:

        try:

            temp = ser.readline()
            t1 = temp.split(";")
            ##print eval(t1[2])
            try:

                data1.append(eval(t1[0]))
                data2.append(eval(t1[1]))
                data3.append(eval(t1[2]))
                data4.append(eval(t1[3]))
                

                ##[data[i].append(int(temp)/(i+1)) for i in range(4)]
                ##[data[i].pop(0) for i in range(3)]
                data1.pop(0)
                data2.pop(0)
                data3.pop(0)
                data4.pop(0)
                time.sleep(0.005)

            except ValueError as Ve:
                #print(Ve)
                pass

        except AttributeError as Ae:
            #print(Ae)
            pass

        except TypeError as Te:
            #print(Te)
            pass

        except Exception as e:
            #print(e)
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
    #plotter.show()

    plotcanvas = FigureCanvasTkAgg(p.fig, root)
    
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    #plotcanvas.show()
    root.mainloop()
    
