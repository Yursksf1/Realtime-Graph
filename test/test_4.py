from tkinter import Tk, Button

root = Tk()
button = Button(root, text="Click Me!")
button.pack()

def callback(event):
    print ("Hello World!")

button.bind("<Button-1>", callback)
root.mainloop()