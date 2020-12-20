#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection='3d')

zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)

myMean = xline.mean()
ax.plot3D(xline, yline, zline, 'gray')

ax.set_title('MyFirstTitle')


plt.show()
plt.legend()
