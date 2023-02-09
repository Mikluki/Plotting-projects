import pandas as pd
import numpy as np
from numpy.random import normal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


plt.rcParams.update(
    {'font.size': 14, 'lines.markersize': 15, 'lines.linewidth': 4,\
     'lines.marker': '.', 'lines.markerfacecolor': 'orange', 'lines.color':'C0',
     'axes.grid': True, 'axes.autolimit_mode': 'round_numbers'})
    # 'axes.prop_cycle': plt.cycler(color=colors), 'figure.max_open_warning': 0})
# ==== Freq range ====
yval = -2
fmin = 20
fmax = 190
Np = 30
# ==== Abs window ====
Nwindows = 3
fW_min = 50
fW_max = 100

ox = np.linspace(fmin, fmax, Np,)
oy = np.full((len(ox),), yval) + normal(scale=0.5, size=len(ox))
# print(oy)
idxW1 = np.where((ox >= fW_min) & (ox <= fW_max))
idxL = np.where((ox < fW_min))
idxR = np.where((ox > fW_max))

fig, ax = plt.subplots(figsize=(10, 7))

ax.plot(ox, oy)
ax.plot(ox[idxW1], oy[idxW1], markerfacecolor='red')


# ax.set_title('Name')
ax.set_xlabel('Frequency (GHz)')
ax.set_ylabel('S$_{11}$ (dB)')
ax.set_ylim(-15, 0)

plt.subplots_adjust(right=0.75)
sliderX = 0.8
sliderY = 0.1
sliderW = 0.05
sliderL = 0.8
Wcolors = plt.cm.rainbow(np.linspace(0, 1, Nwindows))


def create_slder_ax(sliderX, sliderY, sliderW, sliderL):
    return plt.axes([sliderX, sliderY, sliderW, sliderL])


def create_slder(ax, name='val', orient='vertical',\
                vmin=0, vmax=7, vinit=0, vstep=0.5):
    return Slider(ax, name, orientation=orient,\
                  valmin=vmin, valmax=vmax, valinit=vinit,\
                  valstep=vstep)

sl_axes = [create_slder_ax(sliderX+sliderW*i, sliderY,\
                           sliderW, sliderL)\
                           for i, c in enumerate(Wcolors)]
sl_axes
# ax_slider1 = plt.axes([sliderX, 0.1, sliderW, 0.8], facecolor='teal')
# ax_slider2 = plt.axes([sliderX+sliderW, 0.1, sliderW, 0.8], facecolor='teal')
# ax_slider3 = plt.axes([sliderX+sliderW*2, 0.1, sliderW, 0.8], facecolor='teal')

# slider1 = Slider(ax_slider1, 'yval', orientation='vertical',\
#                 valmin=0, valmax=7, valinit=0, valstep=0.5)
# slider2 = Slider(ax_slider2, 'yval', orientation='vertical',
#                 valmin=0, valmax=7, valinit=0, valstep=0.5)
# slider3 = Slider(ax_slider3, 'yval', orientation='vertical',
#                 valmin=0, valmax=7, valinit=0, valstep=0.5)


def update_w1(yval):
    ax.clear()
    ax.plot(ox[idxL], oy[idxL], 'C0')
    ax.plot(ox[idxW1], oy[idxW1] - yval, 'C1')
    ax.plot(ox[idxR], oy[idxR], 'C0')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('S$_{11}$ (dB)')
    ax.set_ylim(-15, 0)

    plt.draw()



slider1.on_changed(update_w1)
# slider2.on_changed(update_w1)
# slider3.on_changed(update_w1)

plt.show()
