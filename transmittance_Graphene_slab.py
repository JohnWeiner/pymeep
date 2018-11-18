import meep as mp
from meep.materials import Graph,Ag,BK7

resolution = 80 # pixels/micron

sx=8
sy=8
cell=mp.Vector3(sx,sy,0)

dpml=1.0
pml_layers=[mp.PML(dpml)]
w=1


geometry = [mp.Block(size=mp.Vector3(0.05*w,mp.inf),
                     center=mp.Vector3(0,0),
                     material=mp.air)]
wvlmax=40.0
wvlmin=10.0
wvlcen=25.0 #center wavelength = 15μm
fmin=1/wvlmax
fmax=1/wvlmin
fcen=1/wvlcen
df = fmax-fmin      #pulse width

sources=[mp.Source(mp.GaussianSource(fcen, fwidth=df),
        component=mp.Ey,
        center=mp.Vector3(-0.5*sx+1.5,0),
                  size=mp.Vector3(0,w))]

sim=mp.Simulation(cell_size=cell,
                  boundary_layers=pml_layers,
                  geometry=geometry,
                  sources=sources,
                  resolution=resolution)
nfreq = 100 #number of frequencies at which to compute flux

# reflected flux region...refl_fr
refl_fr=mp.FluxRegion(center=mp.Vector3(-0.1*w,0),
                      size=mp.Vector3(0, sy)) #reflected flux region location
refl = sim.add_flux(fcen, df, nfreq, refl_fr) #reflected flux capture...in reference run, this serves as the incident flux
                      
# transmitted flux region...tran_fr
tran_fr=mp.FluxRegion(center=mp.Vector3(0.1*w,0),
                      size=mp.Vector3(0, sy)) #transmitted flux region location
tran=sim.add_flux(fcen,df,nfreq,tran_fr) #transmitted flux capture

pt=mp.Vector3(-0.5*w,0) #point for monitoring the field intensity of Gaussian source
sim.run(until_after_sources=mp.stop_when_fields_decayed(10,mp.Ey,pt,1e-3)) #run the simulation

reference_refl_data=sim.get_flux_data(refl) #for the reference run, save the E(w)xH(w) fields data at the reflection plane. These fields are actually the incident fields for the subsequent reflextion and transmission calculation of bent wave guide.

reference_tran_flux=mp.get_fluxes(tran) #used for computing reflectance and transmittance.

# end of reference run

sim.reset_meep() #resets the fields to zero.

# begin measurement run

geometry=[mp.Block(mp.Vector3(0.05*w, mp.inf),
                  center=mp.Vector3(0,0),
                   material=Graph),
         mp.Block(mp.Vector3(0.05*w, 0.05*w),
                   center=mp.Vector3(0,0),
                   material=Graph)]

sim=mp.Simulation(cell_size=cell,
             boundary_layers=pml_layers,
            geometry=geometry,
             sources=sources,
            resolution=resolution)

#reflected flux
refl=sim.add_flux(fcen,df,nfreq,refl_fr)
 #new, measeurement-run transmitted flux region
tran_fr=mp.FluxRegion(center=mp.Vector3(0.5*sx-1.75,0),
                      size=mp.Vector3(0,sy))
tran=sim.add_flux(fcen, df, nfreq, tran_fr)

#now load negated E,H fields from reference run to subtract incident from reflected fields
sim.load_minus_flux_data(refl, reference_refl_data)

pt=mp.Vector3(-0.5*w,0) 

sim.run(until_after_sources=mp.stop_when_fields_decayed(10,mp.Ey,pt,1e-3))

meas_refl_flux=mp.get_fluxes(refl)
meas_tran_flux=mp.get_fluxes(tran)

flux_freqs=mp.get_flux_freqs(refl)

# plot results

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

wl = []
Rs = []
Ts = []

for i in range(nfreq):
    wl = np.append(wl, 1/flux_freqs[i])
    Rs = np.append(Rs,-meas_refl_flux[i]/reference_tran_flux[i])
    Ts = np.append(Ts, meas_tran_flux[i]/reference_tran_flux[i])

#plot results
plt.figure(dpi=160)
plt.plot(wl,Rs,'bo-',markersize=3,label='reflectance')
plt.plot(wl,Ts,'ro-',markersize=3,label='transmittance')
plt.plot(wl,1-Rs-Ts,'go-',markersize=3,label='loss')
ax=plt.gca()
#ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
#ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.05))
#ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))
#ax.xaxis.grid(b=True,which="both")
#ax.yaxis.grid(b=True,which="both")
plt.axis([9.5, 50, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.title("Graphene Film Reflectance and Transmittance")
plt.savefig("Graph_Refectance_Transmittance")
plt.grid()
plt.show()
