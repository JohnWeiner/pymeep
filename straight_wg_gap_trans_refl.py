#transmittance and reflectance for normalisation
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 10
sx=16
sy=32
cell=mp.Vector3(sx,sy,0)

dpml=1.0
pml_layers=[mp.PML(dpml)]

pad=4
w=1
wvg_xcen= 0.5*(sx-w-2*pad)
wvg_ycen=-0.5*(sy-w-2*pad)

geometry = [mp.Block(size=mp.Vector3(mp.inf,w,mp.inf),
                     center=mp.Vector3(0,wvg_ycen,0),
                     material=mp.Medium(epsilon=12)), #Geometry of straight waveguid for normalisation
            mp.Block(size=mp.Vector3(w,w,mp.inf),
                     center=mp.Vector3(0,wvg_ycen,0),
                     material=mp.Medium(epsilon=1))]  #Geometry of straight waveguide with an interruption in the middle

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
                      size=mp.Vector3(0,2*w,0))
refl = sim.add_flux(fcen, df, nfreq, refl_fr)
                      
# transmitted flux region...tran_fr
tran_fr=mp.FluxRegion(center=mp.Vector3(0.5*sx-dpml-0.5,wvg_ycen,0),
                      size=mp.Vector3(0,2*w,0))
tran=sim.add_flux(fcen,df,nfreq,tran_fr)

pt=mp.Vector3(0.5*sx-dpml-0.5,wvg_ycen)
sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))
straight_refl_data=sim.get_flux_data(refl)
straight_tran_data=sim.get_flux_data(tran)
# save incident power for transmission plane
straight_tran_flux=mp.get_fluxes(tran)
straight_refl_flux=mp.get_fluxes(refl)
flux_freqs=mp.get_flux_freqs(refl)

# end of normalisation run

#plot results

wl=[]
RNs=[]
TNs=[]

for i in range(nfreq):
    wl=np.append(wl, 1/flux_freqs[i])
    RNs=np.append(RNs,straight_refl_flux[i])
    TNs=np.append(TNs,straight_tran_flux[i])

plt.subplot(211)
plt.plot(wl,RNs,'bo-',label='reflectance')
plt.subplot(212)
plt.plot(wl,TNs,'ro-',label='transmittance')
plt.show()
