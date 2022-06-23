import tkinter as tk
from tkinter import Frame, Menu, Tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from voronoi import generate_voronoi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Example(Tk):

    def __init__(self):
        plt.Figure()
        #plt.close()
        
        super().__init__()
        self._init_menubar()


    def _init_menubar(self):
        self.title("Simple menu")

        menubar = Menu(self)
        # File
        fileMenu = Menu(self)
        fileMenu.add_command(label="Exit")
        fileMenu.add_command(label="Save as")
        menubar.add_cascade(label="File", menu=fileMenu)
        # Help
        menubar.add_cascade(label="Help")
        self.config(menu=menubar)


def main():
    root = Example()
    root.geometry("500x500")
    #app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
