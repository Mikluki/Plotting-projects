import pandas as pd
import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class MyData:
    def __init__(self, yval, fmin, fmax, Np,
                 xReg_min, xReg_max, nRegions):
        self.nRegs = nRegions
        self.init_ox_oy(yval, fmin, fmax, Np,)
        self.cut_to_regions(xReg_min, xReg_max)

        self.init_plot()
        self.init_sliders()

    def init_ox_oy(self, yval, fmin, fmax, Np,):

        self.ox = np.linspace(fmin, fmax, Np,)
        self.oy = np.full((len(self.ox)), yval) + \
            normal(scale=0.5, size=len(self.ox))

    def cut_to_regions(self, xReg_min, xReg_max):

        # ==== Get list of edges ====
        dr = (xReg_max - xReg_min)/self.nRegs
        # xEdge1 = xReg_min + dr
        # xEdge2 = xReg_min + dr*2
        xEdges = [xReg_min + dr*i for i in range(self.nRegs)]
        xEdges.append(xReg_max)

        # ==== Get list of region indexes ====
        self.idxRegs = [np.where((self.ox >= xEdges[i]) & \
                                    (self.ox <= xEdges[i+1]))
                            for i in range(self.nRegs)]

    def init_plot(self):
        plt.rcParams.update(
            {'font.size': 14, 'lines.markersize': 15, 'lines.marker': '.',
             'lines.linewidth': 4, 'lines.markerfacecolor': 'orange',
             'lines.color': 'C0',
             'axes.grid': True, 'axes.autolimit_mode': 'round_numbers'})
        # ==== Get colors ====
        # self.regColors = plt.cm.plasma_r(np.linspace(0.15, 0.85, self.nRegs))
        self.regColors = plt.cm.viridis_r(np.linspace(0.15, 0.85, \
                                                        self.nRegs))
        # ====// Main Plot \\ ====
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.ax.plot(self.ox, self.oy, color='r')
        for idx, c in zip(self.idxRegs, self.regColors):
            self.line, = self.ax.plot(self.ox[idx], self.oy[idx], color=c)
        # ax.set_title('Name')
        self.ax.set_xlabel('Frequency (GHz)')
        self.ax.set_ylabel('S$_{11}$ (dB)')
        self.ax.set_ylim(-15, 0)

    def init_sliders(self):
        plt.subplots_adjust(right=0.75)
        sliderX = 0.8
        sliderY = 0.1
        sliderW = 0.05
        sliderL = 0.8
        vmin = 0
        vmax = 7
        vinit = 0
        vstep = 0.5
        self.Sliders = []
        for i, c in enumerate(self.regColors):
            slider = self.create_slder(
                sliderX+sliderW*i,sliderY, sliderW, sliderL,
                vmin=vmin, vmax=vmax, vinit=vinit, vstep=vstep,
                name=f'[{i}]', orient='vertical', color=c)

            slider.on_changed(self.update)
            self.Sliders.append(slider)


    def create_slder(self, sliderX, sliderY, sliderW, sliderL,
                    name='val', orient='vertical', color='C0',
                    vmin=0, vmax=7, vinit=0, vstep=0.5):

        ax = plt.axes([sliderX, sliderY, sliderW, sliderL])
        return Slider(ax, name, orientation=orient, color=color,
                    valmin=vmin, valmax=vmax, valinit=vinit,
                    valstep=vstep)

    def update(self, val):
        # self.ax.plot(self.ox, self.oy - val, color='r')
        print(np.shape(self.ox))
        print(np.shape(self.oy))
        self.line.set_ydata(self.oy)



# def update_region(yval):
#     ax.clear()

#     ax.set_xlabel('Frequency (GHz)')
#     ax.set_ylabel('S$_{11}$ (dB)')
#     ax.set_ylim(-15, 0)

#     plt.draw()




# sliders = [create_slder(ax=ax, color=c) for ax, c in zip(sl_axes, regColors)]

# sliders[0].on_changed(update_region)
# # slider2.on_changed(update_w1)
# # slider3.on_changed(update_w1)



# ==== Freq range ====
yval = -2
fmin = 20
fmax = 190
Np = 30
# ==== Define regions ====
nRegions = 3
xReg_min = 50
xReg_max = 105

Data = MyData(yval, fmin, fmax, Np,
              xReg_min, xReg_max, nRegions)

plt.show()
