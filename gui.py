from tkinter import Tk, Frame, Menu
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

from utils import fix_missing_params2
from voronoi import generate_voronoi
import numpy as np
import cv2


class Example(Frame):

    def __init__(self, master):
        super().__init__(master)
        self._init_ui()
        self._set_default_params()
        self._update_img()

    def _init_menubar(self):
        self.master.title("Simple menu")

        menubar = Menu(self.master)
        # File
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self._onExit)
        fileMenu.add_command(label="Save as", command=self._save_as)
        menubar.add_cascade(label="File", menu=fileMenu)
        # Help
        menubar.add_cascade(label="Help", command=lambda: self._help_popup)
        self.master.config(menu=menubar)

    def _init_n_regions_gui(self):
        window = self.master
        # label for number of regions
        self.n_regions_lbl = tk.Label(window, text="# Voronoi regions")
        self.n_regions_lbl.grid(column=0, row=0)
        # textbox for number of regions
        self.n_regions_textbox = tk.Text(window, height=1, width=5)
        self.n_regions_textbox.grid(column=0, row=1)
        # slider for number of regions
        self.n_regions_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.n_regions_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.n_regions_slider.grid(column=0, row=2)

    def _init_padding_gui(self):
        window = self.master
        # label for padding amount
        self.padding_lbl = tk.Label(window, text="Padding amount")
        self.padding_lbl.grid(column=1, row=0)
        # textbox for padding amount
        self.padding_textbox = tk.Text(window, height=1, width=5)
        self.padding_textbox.grid(column=1, row=1)
        # slider for padding amount
        self.padding_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.padding_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.padding_slider.grid(column=1, row=2)

    def _init_rounding_gui(self):
        window = self.master
        # label for rounding amount
        self.rounding_lbl = tk.Label(window, text="Rounding amount")
        self.rounding_lbl.grid(column=2, row=0)
        # textbox for rounding amount
        self.rounding_textbox = tk.Text(window, height=1, width=5)
        self.rounding_textbox.grid(column=2, row=1)
        # slider for rounding amount
        self.rounding_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.rounding_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.rounding_slider.grid(column=2, row=2)
    
    def _init_pad_color_gui(self):
        window = self.master
        # label background color
        self.pad_color_lbl = tk.Label(window, text="BG color")
        self.pad_color_lbl.grid(column=3, row=0)
        # showcase label for showing active bg color
        self.pad_color_canvas = tk.Label()
        self.pad_color_canvas.config(bg='#FA6744', text='        ')
        self.pad_color_canvas.grid(column=3, row=1)
        # button to open colorpicker
        self.pad_color_btn = tk.Button(text="Choose color", command=lambda: self._choose_color())
        self.pad_color_btn.grid(column=3, row=2)

    def _init_image_gui(self):
        # Create an object of tkinter ImageTk
        self.img = Image.open("jap.jpg").resize((300,300))
        self.img = ImageTk.PhotoImage(self.img)

        # Create a Label Widget to display the text or Image
        self.img_label = tk.Label(image=self.img)
        self.img_label.grid(column=0, row=3, columnspan=4)

    def _init_ui(self):
        self._init_menubar()
        self._init_n_regions_gui()
        self._init_padding_gui()
        self._init_rounding_gui()
        self._init_pad_color_gui()
        self._init_image_gui()

        self.debug_label = tk.Label(self.master, text="WELCOME")
        self.debug_label.grid(column=0, row=4)

    def _update_img(self):
        # TODO
        plt.figure()
        voronoi = np.random.randint(255, size=(1108, 1674, 3), dtype=np.uint8)
        #voronoi2 = generate_voronoi(self.input_path, self.output_path, self.n_regions, self.padding_amount, self.pad_color, self.rounding_amount)
        
        voronoi = voronoi.astype(np.uint8)
        voronoi = cv2.cvtColor(voronoi, cv2.COLOR_BGR2RGB)
        print(np.mean(voronoi))
        new_img = Image.fromarray(voronoi).resize((300, 300))
        new_img = ImageTk.PhotoImage(new_img)
        self.img_label.configure(image=new_img)
        self.img = new_img
    
    def get_voronoi_params(self):
        return [self.input_path, self.output_path, self.n_regions, self.padding_amount, self.pad_color, self.rounding_amount]
    
    def _update_debug_label(self):
        info = ", ".join(map(str, self.get_voronoi_params()))
        self.debug_label.config(text=info)

    def _set_default_params(self):
        self.input_path = "jap.jpg"
        params = fix_missing_params2(self.input_path, None, None, None, None, None)
        self.output_path = params[1]
        self.n_regions = params[2]
        self.padding_amount = params[3]
        self.pad_color = params[4]
        self.rounding_amount = params[5]

    def _onExit(self):
        self.quit()

    def _help_popup(self):
        top = tk.Toplevel(self.master)
        top.geometry("750x250")
        top.title("Child Window")
        tk.Label(top, text="Hello World!").place(x=150, y=80)

    def _save_as(self):
        files = [('All Files', '*.*'), 
                ('PNGs', '*.png'),
                ('JPGs', '*.jpg')]
        file = asksaveasfile(filetypes=files, defaultextension=files)

    def _update_GUI_after_slider(self):
        # get values from sliders
        self.n_regions = self.n_regions_slider.get()
        self.padding_amount = self.padding_slider.get()
        self.rounding_amount = self.rounding_slider.get()
        # update textbox 
        self.n_regions_textbox.delete(1.0, tk.END)
        self.n_regions_textbox.insert(tk.END, self.n_regions)

        self.padding_textbox.delete(1.0, tk.END)
        self.padding_textbox.insert(tk.END, self.padding_amount)

        self.rounding_textbox.delete(1.0, tk.END)
        self.rounding_textbox.insert(tk.END, self.rounding_amount)

        self._update_debug_label()
        self._update_img()


    def _update_GUI_after_textbox(self):
        # get values from textboxes
        self.n_regions = self.n_regions_textbox.get("1.0", 'end-1c')
        self.padding_amount = self.padding_textbox.get("1.0", 'end-1c')
        self.rounding_amount = self.rounding_textbox.get("1.0", 'end-1c')
        # TODO update sliders with new values, capped to slider max
        self._update_debug_label()
        self._update_img()


    def _choose_color(self):
        self.pad_color = askcolor()[1] or '#000000'
        self.pad_color_canvas.config(bg=self.pad_color, text='        ')
        self._update_debug_label()
        self._update_img()


def main():
    root = Tk()
    root.geometry("500x500")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()