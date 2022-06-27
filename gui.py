from tkinter import Tk, Frame, Menu
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.colorchooser import askcolor
from typing import Tuple
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import cv2

from utils import fix_missing_params2
from voronoi import generate_voronoi

class GUI(Frame):

    def __init__(self, master : Tk) -> None:

        super().__init__(master)
        self._init_ui()
        self._set_default_params()
        self._update_img()


    def _init_menubar(self) -> None:
        '''Builds top menu bar in the GUI'''

        menubar = Menu(self.master)
        # Save
        menubar.add_cascade(label="Save", command=lambda: self._save_as())
        # Open
        menubar.add_cascade(label="Open", command=lambda: self._choose_filepath())
        # Help
        menubar.add_cascade(label="Help", command=lambda: self._help_popup())
        
        self.master.configure(menu=menubar)

    def _init_n_regions_gui(self) -> None:
        '''Builds n regions input part in the GUI'''

        window = self.master
        # label for number of regions
        self.n_regions_lbl = tk.Label(window, text="# Voronoi regions")
        self.n_regions_lbl.grid(column=0, row=0)
        # textbox for number of regions
        self.n_regions_stringvar = tk.StringVar()
        self.n_regions_stringvar.trace("w", lambda name, index, mode, var=self.n_regions_stringvar: self._update_GUI_after_textbox())
        self.n_regions_entry = tk.Entry(window, textvariable=self.n_regions_stringvar)
        self.n_regions_entry.grid(column=0, row=1)
        # slider for number of regions
        self.n_regions_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.n_regions_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.n_regions_slider.grid(column=0, row=2)

    def _init_padding_gui(self) -> None:
        '''Builds padding input part in the GUI'''

        window = self.master
        # label for padding amount
        self.padding_lbl = tk.Label(window, text="Padding amount")
        self.padding_lbl.grid(column=1, row=0)
        # textbox for padding amount
        self.padding_stringvar = tk.StringVar()
        self.padding_stringvar.trace("w", lambda name, index, mode, var=self.padding_stringvar: self._update_GUI_after_textbox())
        self.padding_entry = tk.Entry(window, textvariable=self.padding_stringvar)
        self.padding_entry.grid(column=1, row=1)
        # slider for padding amount
        self.padding_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.padding_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.padding_slider.grid(column=1, row=2)

    def _init_rounding_gui(self) -> None:
        '''Builds rounding input part in the GUI'''

        window = self.master
        # label for rounding amount
        self.rounding_lbl = tk.Label(window, text="Rounding amount")
        self.rounding_lbl.grid(column=2, row=0)
        # textbox for rounding amount
        self.rounding_stringvar = tk.StringVar()
        self.rounding_stringvar.trace("w", lambda name, index, mode, var=self.rounding_stringvar: self._update_GUI_after_textbox())
        self.rounding_entry = tk.Entry(window, textvariable=self.rounding_stringvar)
        self.rounding_entry.grid(column=2, row=1)
        # slider for rounding amount
        self.rounding_slider = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL)
        self.rounding_slider.bind("<ButtonRelease-1>", lambda _: self._update_GUI_after_slider())
        self.rounding_slider.grid(column=2, row=2)
    
    def _init_pad_color_gui(self) -> None:
        '''Builds background color input part in the GUI'''

        window = self.master
        # label background color
        self.pad_color_lbl = tk.Label(window, text="BG color")
        self.pad_color_lbl.grid(column=3, row=0)
        # showcase label for showing active bg color
        self.pad_color_canvas = tk.Label()
        self.pad_color_canvas.config(bg='#000000', text='        ')
        self.pad_color_canvas.grid(column=3, row=1)
        # button to open colorpicker
        self.pad_color_btn = tk.Button(text="Choose color", command=lambda: self._choose_color())
        self.pad_color_btn.grid(column=3, row=2)

    def _init_image_gui(self) -> None:
        '''Builds image canvas in the GUI'''

        # Create an object of tkinter ImageTk
        self.img = Image.open("jap.jpg").resize((300,300))
        self.img = ImageTk.PhotoImage(self.img)

        # Create a Label Widget to display the text or Image
        self.img_label = tk.Label(image=self.img)
        self.img_label.grid(column=0, row=3, columnspan=4)

    def _init_ui(self) -> None:
        '''Builds the GUI'''

        # flag to prevent voronoi generation when .set is called on textboxes
        # from the _update_GUI_after_slider method
        self._inhibit_voronoi_generation = False

        # init all GUI parts
        self._init_menubar()
        self._init_n_regions_gui()
        self._init_padding_gui()
        self._init_rounding_gui()
        self._init_pad_color_gui()
        self._init_image_gui()

    def _update_img(self) -> None:
        '''Generates a new voronoi image and shows it'''

        # flag to prevent voronoi generation when .set is called on textboxes
        # from the _update_GUI_after_slider method
        if self._inhibit_voronoi_generation:
            return
        voronoi = generate_voronoi(self.input_path, self.n_regions, self.padding_amount, self.pad_color, self.rounding_amount)
    
        # convert and resize image
        voronoi = voronoi.astype(np.uint8)
        self.img_as_numpy = voronoi # this will be the output when saved
        voronoi = cv2.cvtColor(voronoi, cv2.COLOR_BGR2RGB)
        new_img = Image.fromarray(voronoi).resize((300, 300))
        # update image in the GUI
        new_img = ImageTk.PhotoImage(new_img)
        self.img_label.configure(image=new_img)
        self.img = new_img
        
    
    def _get_voronoi_params(self) -> Tuple[str, str, int, int, str, int]:
        '''Get all parameters for the image generation, mainly for debug'''

        return self.input_path, self.output_path, self.n_regions, self.padding_amount, self.pad_color, self.rounding_amount
    

    def _set_default_params(self, input_path="jap.jpg") -> None:
        '''Determines default parameters for the specified image'''

        self.input_path = input_path
        params = fix_missing_params2(self.input_path, None, None, None, None, None)
        self.output_path = params[1]
        self.n_regions = params[2]
        self.padding_amount = int(params[3])
        self.pad_color = params[4]
        self.rounding_amount = int(params[5])

    def _help_popup(self) -> None:
        '''Pops up a window for help'''

        top = tk.Toplevel(self.master)
        top.geometry("750x250")
        top.title("Help and info")
        txt = '''
        Project by Riccardo Rorato.
        For bugs or improvements, submit a PR or contact me at riccardororato99@gmail.com
        '''
        tk.Label(top, text=txt).place(x=150, y=80)

    def _save_as(self) -> None:
        '''Pops up window to choose save location and name, and saves the result'''

        files = [('All Files', '*.*'), 
                ('PNGs', '*.png'),
                ('JPGs', '*.jpg')]
        file = asksaveasfile(filetypes=files, defaultextension=".png")
        if file is not None:
            print(type(self.img_as_numpy))
            print(self.img_as_numpy)
            # TODO FIX NOT OPENABLE IMG
            cv2.imwrite(file.name, self.img_as_numpy)
        

    def _update_GUI_after_slider(self) -> None:
        '''Sliders listener, update GUI with new values'''

        # get values from sliders
        n_regions = self.n_regions_slider.get()
        padding_amount = self.padding_slider.get()
        rounding_amount = self.rounding_slider.get()
        # update textboxes
        # flag to prevent voronoi generation when .set is called on textboxes
        self._inhibit_voronoi_generation = True
        self.n_regions_stringvar.set(str(n_regions))
        self.padding_stringvar.set(str(padding_amount))
        self.rounding_stringvar.set(str(rounding_amount))
        self._inhibit_voronoi_generation = False
        # set instance fields after .set because it assigns self.var....
        self.n_regions = int(n_regions)
        self.padding_amount = int(padding_amount)
        self.rounding_amount = int(rounding_amount)

        self._update_img()

    def _validate_textbox_value(self, text : str) -> int:
        '''Validates input from the textboxes, popup if invalid'''

        if text.strip() == '':
            return 0
        try:
            value = int(text)
        except ValueError as ex:
            error_text = f"{text} is not a valid parameter: enter an integer please"
            self._invalid_input_popup(error_text)
            return 0
        return value

    def _invalid_input_popup(self, text : str) -> None:
        '''Pops up error window with given text'''

        top = tk.Toplevel(self.master)
        top.geometry("750x250")
        top.title("Error")
        tk.Label(top, text=text).place(x=150, y=80)


    def _update_GUI_after_textbox(self) -> None:
        '''Textbox listener, update GUI with new values'''

        # get values from textboxes
        self.n_regions = self._validate_textbox_value(self.n_regions_entry.get())
        self.padding_amount = self._validate_textbox_value(self.padding_entry.get())
        self.rounding_amount = self._validate_textbox_value(self.rounding_entry.get())
        
        # update sliders with new values
        self.n_regions_slider.set(self.n_regions)
        self.padding_slider.set(self.padding_amount)
        self.rounding_slider.set(self.rounding_amount)

        self._update_img()


    def _choose_color(self) -> None:
        '''Opens a popup to let the user choose a background color'''

        self.pad_color = askcolor()[1] or '#000000'
        self.pad_color_canvas.config(bg=self.pad_color, text='        ')

        self._update_img()
    
    def _choose_filepath(self) -> None:
        '''Opens a popup to let the user choose an input file'''

        self.input_path = filedialog.askopenfilename()
        self._set_default_params(self.input_path)
        self._update_gui_from_internal_params()

        self._update_img()

    def _update_gui_from_internal_params(self) -> None:
        '''Updates all the GUI with internal voronoi params'''

        self.n_regions_slider.set(self.n_regions)
        self.padding_slider.set(self.padding_amount)
        self.rounding_slider.set(self.rounding_amount)
        n_regions = self.n_regions
        padding_amount = self.padding_amount
        rounding_amount = self.rounding_amount
        self._inhibit_voronoi_generation = True
        self.n_regions_stringvar.set(str(n_regions))
        self.padding_stringvar.set(str(padding_amount))
        self.rounding_stringvar.set(str(rounding_amount))
        self._inhibit_voronoi_generation = False

def main() -> None:
    root = Tk()
    root.title("Voronoi art Generator")
    root.geometry("500x500")
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()