#import serial
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
#root.geometry('1200x700+200+100')
#root.title('This is my root window')
#root.state('zoomed')
#root.config(background='#fafafa')
filne = "Datos.txt"
ser = open(filne, 'r+')
#print(ser)
xar = []
yar = []

#style.use('ggplot')
fig = plt.figure(figsize=(10, 4.5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 1000)
ax1.set_xlim(0, 1000)
line, = ax1.plot(xar, yar, 'r')
#ser = serial.Serial('com3', 9600)

def animate(i):
    #ser.reset_input_buffer()
    #data = ser.readline().decode("utf-8")
    #data_array = data.split(',')
    #yvalue = float(data_array[1])

    temp = ser.readline()
    t1 = temp.split(";")
    yar.append(eval(t1[0]))
    xar.append(i)
    line.set_data(xar, yar)
    #ax1.set_xlim(0, i+1)


plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
#plotcanvas.show()

root.mainloop()