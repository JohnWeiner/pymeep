import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import math

theta_in = np.arange(0,85,5) #17-element row vector of angles(deg) from 0 to 80 by 5's.
kxs = np.empty((50,theta_in.size)) #Create empty matrix, 50 row 17 columns for the kx values
thetas = np.empty((50,theta_in.size)) #Create empty matrix for angles..same size and shape as kxs
Rmeep = np.empty((50,theta_in.size)) #Create empty matrix for meep reflection calculation...sames as thetas and kxs.

for j in range(theta_in.size): #theta_in.size = 17 in this example (j=0 to 80 by 5).
  f = np.genfromtxt("flux_t{}.dat".format(theta_in[j]), delimiter=",")
#f is an array consisting of 4 columns and 50 rows. For the jth loop pass, f takes its data from the jth "flux_t{j}.dat" file.
  kxs[:,j] = f[:,0] #kxs fills rows at each j column from the 0 column of f, consisting of 50 elements.
  thetas[:,j] = f[:,2] #thetas fills rows at each j column from the 2 column of f, consisting of 50 elements.
  Rmeep[:,j] = f[:,3] #Rmeep fills rows at each j column from the 3 column of f, consisting of 50 elements.

wvl = f[:,1]
#wvl is row vector from the 1 column of f, consisting of 50 wavelengths and corresponding to the 50 freqs of the source pulse.

wvls = np.matlib.repmat(np.reshape(wvl, (wvl.size,1)),1,theta_in.size)
# create wvls as a 2d matrix for each of the 50 wavelengths by repeating the column vector for each of the 17 angles.

n1=1
n2=3.5

# compute angle of refracted planewave in medium n2
# for incident planewave in medium n1 at angle theta_in...note that theta_out is a lambda function that takes theta_in as an arg.

theta_out = lambda theta_in: math.asin(n1*math.sin(theta_in)/n2)

# compute Fresnel reflectance for P-polarization (TM polarisation) in medium n2
# For incident planewave in medium n1 at angle theta_in, this is the Fresnel reflectance formula...note the lambda function.
#This is the square of the negative of the amplitude formula from Born and Wolf. math.fabs takes the absolute value.

Rfresnel = lambda theta_in: math.fabs((n1*math.cos(theta_out(theta_in))-n2*math.cos(theta_in))/(n1*math.cos(theta_out(theta_in))+n2*math.cos(theta_in)))**2

Ranalytic = np.empty((50, theta_in.size))# Ranalytic is a matrix of the same form as Rmeep.
for m in range(wvl.size):
    for n in range(theta_in.size):
        Ranalytic[m,n] = Rfresnel(math.radians(thetas[m,n]))

#start plotting
theta_45=thetas[: ,8]
Rmeep_45=Rmeep[: ,8]
Ranalytic_45=Ranalytic[:,8]
plt.figure(dpi=160)
plt.plot(theta_45,Rmeep_45,'bo-',label='R_meep')
plt.plot(theta_45,Ranalytic_45,'rs-',label='R_Fresnel')
plt.xlim(17.5,42.5)
plt.xticks(np.arange(17.5,42.5,2.5))
plt.yticks(np.arange(0.2,0.3,0.01))
plt.ylim(0.2,0.3)
plt.xlabel("angles corresponding to kx at incident angle of 45 deg")
plt.ylabel("Fresnel R")
plt.title("reflectance(meep and Fresnel)")
plt.legend()
plt.grid()
plt.show()

plt.figure(dpi=160)
plt.pcolormesh(kxs, wvls, Rmeep, cmap='seismic', shading='gouraud', vmin=0, vmax=Rmeep.max())
#x-axis is kxs column index and y-axis is wvls row index; Rmeep values are colored by cmap; "gouraud" is interpolated shading.
plt.axis([kxs[0,0], kxs[0,-1], wvl[-1], wvl[0]]) #The use of -1 in kxs[0,-1] infers the entire extent of the column index.
plt.yticks([t for t in np.arange(0.4,0.9,0.1)]) #yticks from 0.4, 0.5...0.8
plt.xlabel("Bloch-periodic wavevector ($k_x/2π$)")
plt.ylabel("wavelength (μm)")
plt.title("reflectance (meep)")
cbar = plt.colorbar()
cbar.set_ticks([t for t in np.arange(0,0.4,0.1)])
cbar.set_ticklabels(["{:.1f}".format(t) for t in np.arange(0,0.4,0.1)])
plt.show()
