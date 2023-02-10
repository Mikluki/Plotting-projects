import pandas as pd
import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class MyData:
    def __init__(self, yval, fmin, fmax, n_points,
                 xReg_min, xReg_max, nRegions):
        self.nRegs = nRegions
        self.init_ox_oy(yval, fmin, fmax, n_points,)
        self.init_regions(xReg_min, xReg_max)

        self.init_plot()
        self.init_sliders()


    def init_ox_oy(self, yval, fmin, fmax, n_points,):

        self.ox = np.linspace(fmin, fmax, n_points,)
        self.oy = np.full((len(self.ox)), yval) + \
            normal(scale=0.5, size=len(self.ox))

    def init_regions(self, xReg_min, xReg_max):

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
        self.regNames = [f'r{i}' for i in range(self.nRegs)]


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
        self.line, = self.ax.plot(self.ox, self.oy, color='r')

        for idx, c in zip(self.idxRegs, self.regColors):
            self.ax.plot(self.ox[idx], self.oy[idx], mfc=c, color=c)

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
        self.all_Sliders = []
        for i, (rname, c) in enumerate(zip(self.regNames, self.regColors)):

            mySlider = self.create_slider(
                sliderX+sliderW*i,sliderY, sliderW, sliderL,
                vmin=vmin, vmax=vmax, vinit=vinit, vstep=vstep,
                name=rname, orient='vertical', color=c)

            updateFun = self.init_updateFunc(mySlider)
            mySlider.on_changed(updateFun)
            self.all_Sliders.append(mySlider)


    def create_slider(self, sliderX, sliderY, sliderW, sliderL,
                    name, orient='vertical', color='C0',
                    vmin=0, vmax=7, vinit=0, vstep=0.5):

        ax = plt.axes([sliderX, sliderY, sliderW, sliderL])
        return Slider(ax, name, orientation=orient, color=color,
                    valmin=vmin, valmax=vmax, valinit=vinit,
                    valstep=vstep)

    def init_updateFunc(self, mySlider):
        def updateFun(val):
            print(mySlider.label)
            self.val = val
            print(self.val)
        return updateFun

    # def init_updateFuncs(self):
    #     self.updateFuncs = []
    #     for i, regName in enumerate(self.regNames):
    #         self.updateFuncs.append(self.factory(regName))
    # def factory(self, Slider):
    #     def f(val):
    #         print(funcname, val)
    #         self.val = self.val + val
    #         print(self.val)
    #     return f


    def update(self, val):
        [print(sl.label) for sl in self.all_Sliders]
        print('^---^')
        self.line.set_ydata(self.oy - val)

    def recalc_oy(self, val):
        self.oy = self.oy - val

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
n_points = 30
# ==== Define regions ====
nRegions = 3
xReg_min = 50
xReg_max = 105

Data = MyData(yval, fmin, fmax, n_points,
              xReg_min, xReg_max, nRegions)

plt.show()
