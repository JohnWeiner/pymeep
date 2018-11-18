import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
minorLocator=MultipleLocator(20)
plt.figure(figsize=(12,6), dpi=100)
wvl=np.genfromtxt('wvl_slab.dat', delimiter='\n')
flux=np.genfromtxt('flux_slab.dat', delimiter='\n')
#plt.plot(wvl,flux, ls = '-', lw =3, color='blue', )
#plt.plot(wvl,flux, marker='o', markersize=5, color='blue' )
plt.scatter(1000*wvl,flux,s=30, marker='o',color='blue', edgecolors="red", linewidths=0.5 )
ax=plt.gca()
#for tick in ax.get_xticklabels():#one methond to alter the font size of the tick labels
#    tick.set_fontsize(11)
#for tick in ax.get_yticklabels():
#    tick.set_fontsize(11)
ax.tick_params(axis='both', which='major', labelsize= 11) #alternative (and simpler) way to alter font size of tick labels.
ax.tick_params(axis='x', which='major', top=True, direction='in', length=14)
ax.tick_params(axis='x', which='minor', top=True, direction='in', length=7)
ax.xaxis.set_minor_locator(minorLocator)
ax.set_xlabel('wavelength(nm)',fontsize=14)
ax.set_ylabel('fractional flux', fontsize=14)
ax.set_title('Net Fractional Flux through Subwavelength Slit', fontsize=16)
plt.grid()
plt.savefig('slit_flux_vs_wvl')
plt.show()
