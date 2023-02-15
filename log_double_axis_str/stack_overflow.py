import matplotlib
from matplotlib import pyplot as plt
fig1, ax1 = plt.subplots()
ax1.plot([10, 100, 1000], [1,2,3])

ax1.set_xscale('log')

ax1.set_xticks([20, 200, 1000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_xticklabels(['a', 'b' ,'c'])
plt.show()
