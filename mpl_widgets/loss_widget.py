import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class MyData:
    '''Attributes:
    self.Loss       - Loss to calc Loss.val         [class]
    self.regSliders - Sliders for each region       [list of classes]
    self.regColors  - colors for each region        [list of np.arrays]
    self.regNames   - names for each region         [list of strings]
    self.regLines   - Lines in Axes for each region [list of classes]
    self.idxRegs    - indexes for each region       [list of np.arrays]
    self.ax         - main Axes for plotting        [class]
    self.line       - main Line in Axes             [class]
    '''
    def __init__(self, yval, fmin, fmax, n_points,
                 xReg_min, xReg_max, nRegions,
                 lossPower, lossThreshold):
        self.nRegs = nRegions
        self.xReg_min, self.xReg_max = xReg_min, xReg_max
        self.init_ox_oy(yval, fmin, fmax, n_points)
        self.init_regions()

        self.Loss = Loss(self, power=lossPower, threshold = lossThreshold)

        self.init_plot()
        self.init_sliders()


    def init_ox_oy(self, yval, fmin, fmax, n_points,):

        self.ox = np.linspace(fmin, fmax, n_points,)
        rng = np.random.default_rng(20654)
        self.oy = np.full((len(self.ox)), yval) + \
            rng.normal(scale=0.5, size=len(self.ox))


    def init_regions(self):

        # ==== Get list of edges ====
        dr = (self.xReg_max - self.xReg_min)/self.nRegs
        # xEdge1 = self.xReg_min + dr
        xEdges = [self.xReg_min + dr*i for i in range(self.nRegs)]
        xEdges.append(self.xReg_max)

        # ==== Get list of region indexes ====
        self.idxRegs = [np.where((self.ox >= xEdges[i]) & \
                                    (self.ox < xEdges[i+1]))
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
        self.regColors = plt.cm.viridis_r(np.linspace(0.15, 0.85, self.nRegs))
        # ====// Main Plot \\ ====
        fig, self.ax = plt.subplots(figsize=(10, 7))
        self.line, = self.ax.plot(self.ox, self.oy, color='r')

        self.regLines = []
        for idx, c in zip(self.idxRegs, self.regColors):
            line, = self.ax.plot(self.ox[idx], self.oy[idx], mfc=c, color=c)
            self.regLines.append(line)

        # lossStr = lossFunc1(self.ox, self.oy, self.xReg_min, self.xReg_max,
        #           T=threshold, power=power)
        self.Loss.calc()
        self.text = self.ax.text(0.25, 0.85, 'Loss = %1.2f' % self.Loss.val)
        # self.ax.set_title('Name')
        self.ax.set_xlabel('Frequency (GHz)')
        self.ax.set_ylabel('S$_{11}$ (dB)')
        self.ax.set_ylim(-15, 0)


    def init_sliders(self):
        sliderW = 0.05
        sliderX = 0.95 - sliderW*len(self.regNames)
        sliderY = 0.1
        sliderL = 0.8

        hSpace = 0.10
        plt.subplots_adjust(right=1 - hSpace - sliderW*len(self.regNames))
        vmin = 0
        vmax = 10
        vinit = 0
        vstep = 0.5
        self.regSliders = []
        for i, (idxReg, rname, c) in enumerate(
                zip(self.idxRegs, self.regNames, self.regColors)):

            mySlider = self.create_Slider(
                sliderX+sliderW*i,sliderY, sliderW, sliderL,
                vmin=vmin, vmax=vmax, vinit=vinit, vstep=vstep,
                name=rname, orient='vertical', color=c)
            mySlider.__dict__['name'] = rname
            mySlider.__dict__['prev_val'] = 0
            mySlider.__dict__['new_val'] = 0
            updateFun = self.create_updateFunc(mySlider, idxReg)

            mySlider.on_changed(updateFun)
            self.regSliders.append(mySlider)


    def create_Slider(self, sliderX, sliderY, sliderW, sliderL,
                    name, orient='vertical', color='C0',
                    vmin=0, vmax=7, vinit=0, vstep=0.5):
        # init slider axis
        ax = plt.axes([sliderX, sliderY, sliderW, sliderL])
        # create slider class
        return Slider(ax, name, orientation=orient, color=color,
                    valmin=vmin, valmax=vmax, valinit=vinit,
                    valstep=vstep)

    def create_updateFunc(self, mySlider, idxReg):
        def updateFunc(val):
            print(mySlider.name)
            # === //remeber prev slider value: choose add or subtract
            mySlider.new_val = val
            if mySlider.new_val > mySlider.prev_val:
                add = -(val-mySlider.prev_val)
            else:
                add = (mySlider.prev_val-val)
            mySlider.prev_val = val

            # === //recalc self.oy
            self.recalc_oy(idxReg, add)
            self.Loss.calc()

            # === //update plot
            self.line.set_ydata(self.oy)
            for line, idx in zip(self.regLines, self.idxRegs):
                line.set_ydata(self.oy[idx])
            self.text.set_text('Loss = %1.2f' % self.Loss.val)
        return updateFunc

    def recalc_oy(self, idxReg, add):
        # zeros = create zero array size of oy
        regZeros = np.zeros(np.shape(self.oy))
        # fill zeros with valls at indexes
        np.put(regZeros, [idxReg], add)
        # add to original array
        self.oy = self.oy + regZeros


class Loss:
    def __init__(self, Data, power, threshold):
        self.Data = Data
        self.p = power
        self.T = threshold
        print('power =', self.p, '   threshold = ', self.T)
    def calc(self):
        """T - threshold
        above T = sum[max[(Y-T),0]^power]
        below T = sum[min[(Y-T),0]/3]
        """
        idx = np.where((self.Data.ox >= self.Data.xReg_min) \
                        & (self.Data.ox <= self.Data.xReg_max))
        aboveT = np.sum(np.maximum((self.Data.oy[idx] - self.T), 0)**self.p)
        belowT = np.sum(np.minimum((self.Data.oy[idx] - self.T), 0))/3

        self.val = aboveT + belowT
        print('Loss =', self.val)



# ==== Freq range ====
yval = -2
fmin = 20
fmax = 190
n_points = 30
# ==== Define regions ====
nRegions = 3
xReg_min = 50
xReg_max = 110

# ==== Loss func params ====
threshold = - 8
lossPower = 2.5

Data = MyData(yval, fmin, fmax, n_points,
              xReg_min, xReg_max, nRegions,
              lossPower=lossPower, lossThreshold=threshold)

Data.regSliders[0].val = 5
print(Data.regSliders[0].val)
Data.ax.figure.savefig('test.png', bbox_inches='tight')
print(Data.__doc__)
plt.show()

