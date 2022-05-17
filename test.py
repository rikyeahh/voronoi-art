# Import required libraries
from tkinter import *
from PIL import ImageTk, Image

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
win.geometry("700x500")

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("jap.jpg"))

# Create a Label Widget to display the text or Image
label = Label(win, image = img)
label.grid(column=0, row=0)

win.mainloop()