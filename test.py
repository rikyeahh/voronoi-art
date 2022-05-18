import tkinter as tk
from tkinter import Frame, Menu, Tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from voronoi import generate_voronoi


class Example(Frame):

    def __init__(self, master):
        super().__init__(master)
        self._init_image_gui()
        self._set_default_params()
        self._update_img()

    def _init_image_gui(self):
        # Create an object of tkinter ImageTk
        self.img = Image.open("jap.jpg").resize((300,300))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a Label Widget to display the text or Image
        self.img_label = tk.Label(image=self.img)
        self.img_label.grid(column=0, row=3, columnspan=4)

    def _update_img(self):
        # produce image
        voronoi_img = np.random.randint(255, size=(2000, 2000, 3), dtype=np.uint8)
        voronoi_img = generate_voronoi(self.input_path, self.output_path, self.n_regions, self.padding_amount, self.pad_color, self.rounding_amount)
        voronoi_img = voronoi_img.astype(np.uint8)
        voronoi_img = cv2.cvtColor(voronoi_img, cv2.COLOR_BGR2RGB)
        new_img = Image.fromarray(voronoi_img).resize((200, 200))
        new_img = ImageTk.PhotoImage(new_img)
        # update the UI to show it
        self.img_label.configure(image=new_img)
        self.img = new_img

    def _set_default_params(self):
        self.input_path = "jap.jpg"
        self.output_path = "jap_out.jpg"
        self.n_regions = 100
        self.padding_amount = 10
        self.pad_color = "#000000"
        self.rounding_amount = 10


def main():
    root = Tk()
    root.geometry("500x500")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
