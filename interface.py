import numpy as np
import matplotlib.pyplot as pl
from matplotlib import animation
from matplotlib.widgets import Slider, Button, RadioButtons
import matplotlib.gridspec as gridspec
import time

class Interface(animation.TimedAnimation):
    def __init__(self, mov, **kwargs):

        self.mov = mov

        # figure setup
        self.fig = pl.figure()
        self.ax_mov = self.fig.add_axes([.3,.3,.4,.5])
        self.ax_nav = self.fig.add_axes([.3,.2,.4,.1])
        self.ax_nav.set_xlim([0, len(self.mov)])
        self.ax_nav.axis('off')

        self.movdata = self.ax_mov.imshow(self.mov[0], vmin=0, vmax=1)
        self.movdata.set_animated(True)
        self.navdata, = self.ax_nav.plot([-2,-2],[-1,1], 'r-')

        self.fig.canvas.mpl_connect('button_press_event', self.evt_click)

        # runtime
        self._idx = -1
        self.t0 = time.clock()
        self.always_draw = [self.movdata, self.navdata]
        self.blit_clear_axes = [self.ax_mov, self.ax_nav]

        # parent init
        animation.TimedAnimation.__init__(self, self.fig, interval=40, blit=True, **kwargs)
    
    @property
    def frame_seq(self):
        self._idx += 1
        if self._idx == len(self.mov):
            self._idx = 0
        self.navdata.set_xdata([self._idx, self._idx])
        yield self.mov[self._idx]

    @frame_seq.setter
    def frame_seq(self, val):
        pass

    def new_frame_seq(self):
        return self.mov


    def _init_draw(self):
        self._draw_frame(self.mov[0])
        self._drawn_artists = self.always_draw

    def _draw_frame(self, d):
        self.t0 = time.clock()

        self.movdata.set_data(d)
        
        # blit
        self._drawn_artists = self.always_draw
        for da in self._drawn_artists:
            da.set_animated(True)
    
    def _blit_clear(self, artists, bg_cache):
        for ax in self.blit_clear_axes:
            if ax in bg_cache:
                self.fig.canvas.restore_region(bg_cache[ax])
    
    def evt_click(self, evt):
        if not evt.inaxes:
            return

        elif evt.inaxes in [self.ax_nav]:
            x = int(np.round(evt.xdata))
            self._idx = x
    

if __name__ == '__main__':
    # load data
    mov = np.array([np.clip(np.random.normal(i,.1,size=[512,512]),0,1) for i in np.linspace(0,1,100)])
    # run interface
    intfc = Interface(mov)
