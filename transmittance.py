import meep as mp

resolution = 10 # pixels/micron

sx=16
sy=32
cell=mp.Vector3(sx,sy,0)

dpml=1.0
pml_layers=[mp.PML(dpml)]
pad=4
w=1
wvg_xcen= 0.5*(sx-w-2*pad) #x center for vertical wave guide
wvg_ycen=-0.5*(sy-w-2*pad) #y center for horizontal wave guide

geometry = [mp.Block(size=mp.Vector3(mp.inf,w,mp.inf),
                     center=mp.Vector3(0,wvg_ycen,0),
                     material=mp.Medium(epsilon=12))]
#straight waveguide for normalisation

fcen=0.15  #pulse center frequency
df = 0.1      #pulse width

sources=[mp.Source(mp.GaussianSource(fcen, fwidth=df),
        component=mp.Ez,
        center=mp.Vector3(-0.5*sx+1,wvg_ycen,0),
                  size=mp.Vector3(0,w,0))]

sim=mp.Simulation(cell_size=cell,
                  boundary_layers=pml_layers,
                  geometry=geometry,
                  sources=sources,
                  resolution=resolution)
nfreq = 100 #number of frequencies at which to compute flux

# reflected flux region...refl_fr
refl_fr=mp.FluxRegion(center=mp.Vector3(-0.5*sx+dpml+0.5,wvg_ycen,0),
                      size=mp.Vector3(0, 2*w, 0)) #reflected flux region location
refl = sim.add_flux(fcen, df, nfreq, refl_fr) #reflected flux capture...in norm. run, this serves as the incident flux
                      
# transmitted flux region...tran_fr
tran_fr=mp.FluxRegion(center=mp.Vector3(0.5*sx-dpml-0.5 ,wvg_ycen, 0),
                      size=mp.Vector3(0, 2*w, 0)) #transmitted flux region location
tran=sim.add_flux(fcen,df,nfreq,tran_fr) #transmitted flux capture

pt=mp.Vector3(0.5*sx-dpml-0.5,wvg_ycen) #point for monitoring the field intensity of Gaussian source
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3)) #run the simulation

straight_refl_data=sim.get_flux_data(refl) #for the normalisation run, save the E(w)xH(w) fields data at the reflection plane. These fields are actually the incident fields for the subsequent reflextion and transmission calculation of bent wave guide.

straight_tran_flux=mp.get_fluxes(tran) #used for computing reflectance and transmittance.

# end of straight_wg normalisation run

sim.reset_meep() #resets the fields to zero.

# begin bent_wg scattering run

geometry=[mp.Block(mp.Vector3(sx-pad, w, mp.inf),
                   center=mp.Vector3(-0.5*pad,wvg_ycen),
                   material=mp.Medium(epsilon=12)), #horizontal wave guide.
          mp.Block(mp.Vector3(w, sy-pad, mp.inf),
                   center=mp.Vector3(wvg_xcen, 0.5*pad),
                   material=mp.Medium(epsilon=12))] #vertical wave guide.

sim=mp.Simulation(cell_size=cell,
              boundary_layers=pml_layers,
              geometry=geometry,
              sources=sources,
              resolution=resolution)

# reflected flux
refl=sim.add_flux(fcen,df,nfreq,refl_fr)
# new transmitted flux region
tran_fr=mp.FluxRegion(center=mp.Vector3(wvg_xcen,0.5*sy-dpml-0.5,0),
                      size=mp.Vector3(2*w,0,0))
tran=sim.add_flux(fcen, df, nfreq, tran_fr)

#now load negated E,H fields from normalisation run to subtract incident from reflected fields
sim.load_minus_flux_data(refl, straight_refl_data)

pt=mp.Vector3(wvg_xcen,0.5*sy-dpml-0.5) #at position of new tran_fr on vertical wave guide.

sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))

bend_refl_flux=mp.get_fluxes(refl)
bend_tran_flux=mp.get_fluxes(tran)

flux_freqs=mp.get_flux_freqs(refl)

# plot results

import numpy as np
import matplotlib.pyplot as plt

wl = []
Rs = []
Ts = []

for i in range(nfreq):
    wl = np.append(wl, 1/flux_freqs[i])
    Rs = np.append(Rs,-bend_refl_flux[i]/straight_tran_flux[i])
    Ts = np.append(Ts, bend_tran_flux[i]/straight_tran_flux[i])

plt.plot(wl,Rs,'bo-',label='reflectance')
plt.plot(wl,Ts,'ro-',label='transmittance')
plt.plot(wl,1-Rs-Ts,'go-',label='loss')
plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.show()
    
 
