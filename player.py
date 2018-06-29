import tkinter as tk
import numpy as np
import time
import matplotlib as mpl
from PIL import Image, ImageTk
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

class MoviePlayer(tk.Frame):
    def __init__(self, data, Ts=1):
        

        # image setup
        self.data = data # source of images
        self.n, self.h, self.w = self.data.shape
        self.imshape = (self.w, self.h)
        self.Ts = Ts

        # tkinter setup
        self.root = tk.Tk()
        self.master = self.root
        window_size = [self.w, self.h]
        tk.Frame.__init__(self, master=self.master, 
                width=window_size[0], height=window_size[1])
        self.canvas = tk.Canvas(self, width=self.w, height=self.h)
        # Populate frame
        self.canvas.place(relx=0,rely=0,x=0,y=0)
        self.pack()

        # tk bindings
        self.bind("<Destroy>", self.end)
        self.root.bind('f', self.faster)
        self.root.bind('s', self.slower)

        # messing with mpl
        fig = mpl.figure.Figure(figsize=(2, 1))
        ax = fig.add_axes([0, 0, 1, 1])
        self.line, = ax.plot(np.arange(1000), np.random.random(1000))
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().place(relx=.5, rely=.5)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack()

        # runtime variables
        self._recall = None # stores `after' event
        self.ended = False

	# run
        self.after(0, self.step)

    def faster(self, *args):
        self.Ts /= 1.5

    def slower(self, *args):
        self.Ts *= 1.5

    def step(self):

        if self.ended:
            return
        
        # acquire image
        self.im = Image.fromarray(self.data.get())
        
        # convert image for display
        self.photo = ImageTk.PhotoImage(image=self.im) # 1-3 msec
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW) # 1-5 msec

        # call next step
        self.recall = self.after(int(self.Ts*1000), self.step)

    def end(self, *args):
        self.ended = True
        self.root.quit()






class Data():
    def __init__(self):
        self.shape = [3000,512,512]
    def get(self):
        frame = np.random.random([512,512])
        minn,maxx = frame.min(),frame.max()
        frame = (255*((frame-minn)/(maxx-minn))).astype(np.uint8)
        return frame
