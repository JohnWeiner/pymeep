import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy.matlib
import math
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

majorLocator = MultipleLocator(20)
majorFormatter = FormatStrFormatter('%d')
minorLocator = MultipleLocator(5)

f=np.genfromtxt("ldos_200_shell.dat", delimiter=",")
for j in range(205,1005,5):
    tmp=np.genfromtxt("ldos_"+str(j)+"_shell.dat",delimiter=",")
    f=np.vstack((f,tmp))

frq=f[:,[0]]
wvl=(1/frq)*1000.0
ldos=f[:,[1]]

print(wvl,ldos)

plt.figure(dpi=160)
ax = plt.gca()
plt.plot(wvl,ldos,"bo-",markersize=3)
ax.xaxis.set_minor_locator(minorLocator)
plt.annotate('Ex point dipole 5nm above sphere surface: 2D',xy=(400,100), xytext=(400,100))
plt.ylabel("ldos (not normalised)")
plt.xlabel("wavelength(nm)")
plt.title("LDOS vs Wavelength-2D")
plt.savefig("LDOS vs Wavelength_Dipole_Ex_2D")
plt.grid()
plt.show()



