import pandas as pd
import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def create_slder_ax(sliderX, sliderY, sliderW, sliderL):
    return plt.axes([sliderX, sliderY, sliderW, sliderL])


def create_slder(ax, name='val', orient='vertical', color='C0',
                 vmin=0, vmax=7, vinit=0, vstep=0.5):
    return Slider(ax, name, orientation=orient, color=color,
                  valmin=vmin, valmax=vmax, valinit=vinit,
                  valstep=vstep)


def update_region(val):
    ax.clear()

    ax.plot(ox[idxL], oy[idxL], 'C0')
    ax.plot(ox[idxR], oy[idxR], 'C0')
    ax.plot(ox[idxR1], oy[idxR1]-val, 'C1')

    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('S$_{11}$ (dB)')
    ax.set_ylim(-15, 0)

    plt.draw()


plt.rcParams.update(
    {'font.size': 14, 'lines.markersize': 15, 'lines.marker': '.',\
     'lines.linewidth': 4, 'lines.markerfacecolor': 'orange', 'lines.color': 'C0',
     'axes.grid': True, 'axes.autolimit_mode': 'round_numbers'})
    # 'axes.prop_cycle': plt.cycler(color=colors), 'figure.max_open_warning': 0})
# ==== Freq range ====
yval = -2
fmin = 20
fmax = 190
Np = 30
# ==== Define regions ====
nRegions = 3
xReg_min = 50
xReg_max = 105

ox = np.linspace(fmin, fmax, Np,)
oy = np.full((len(ox),), yval) + normal(scale=0.5, size=len(ox))
# ==== Get region indexes ====
# mainRegL = xReg_max - xReg_min
dr = (xReg_max - xReg_min)/nRegions
xEdges = [xReg_min + dr*i for i in range(nRegions)]
xEdges.append(xReg_max)
# fEdge1 = xReg_min + dr
# fEdge2 = xReg_min + dr*2
# print(xEdges)
idxR_all = [np.where((ox >= xEdges[i]) & (ox <= xEdges[i+1]))\
            for i in range(nRegions)]
# print(idxR_all)
idxR1 = np.where((ox >= xReg_min) & (ox <= xReg_max))
idxL = np.where((ox < xReg_min))
idxR = np.where((ox > xReg_max))


# regColors = plt.cm.plasma_r(np.linspace(0.2, 0.8, nRegions))
regColors = plt.cm.viridis_r(np.linspace(0.15, 0.85, nRegions))
sliderX = 0.8
sliderY = 0.1
sliderW = 0.05
sliderL = 0.8


# ====// Main Plot \\ ====
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot(ox, oy)
# ax.plot(ox[idxR1], oy[idxR1], markerfacecolor='red')
for idx in idxR_all:
    ax.plot(ox[idx], oy[idx])
# ax.set_title('Name')
ax.set_xlabel('Frequency (GHz)')
ax.set_ylabel('S$_{11}$ (dB)')
ax.set_ylim(-15, 0)

plt.subplots_adjust(right=0.75)
sl_axes = [create_slder_ax(sliderX+sliderW*i, sliderY, sliderW, sliderL)
           for i in range(nRegions)]
sliders = [create_slder(ax=ax, color=c) for ax, c in zip(sl_axes, regColors)]

sliders[0].on_changed(update_region)
# slider2.on_changed(update_w1)
# slider3.on_changed(update_w1)

plt.show()
