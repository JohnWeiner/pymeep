import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import argparse
from meep.materials import Ag,BK7

sx=4.0 #spatial extent along x including pmls (μm)
sy=4.0
sz=0.0
dpml=1.0

cell = mp.Vector3(sx,sy,sz)
pml_layers=[mp.PML(dpml)]
geometry=[mp.Sphere(radius=0.7,
          center=mp.Vector3(0,0,0),
                        material=Ag),
          mp.Sphere(radius=0.5,
                    center=mp.Vector3(0,0,0),
                    material=mp.Medium(epsilon=12.25))]                    
resolution=200
wvl=825/1000 #convert args.wvl from nm to μm
fcen=1/wvl
df=0
nfreq=1
print("wavelength =", wvl,"μm")
print("center frequency =", fcen, "1/μm")

source=[mp.Source(mp.GaussianSource(fcen,df,nfreq),
                 component=mp.Ey,
                 center=mp.Vector3(0,-0.705,0))]

symmetries=[mp.Mirror(mp.X),mp.Mirror(mp.Z)]

sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers)

pt=mp.Vector3(0,-0.705,0)
       
sim.run(mp.dft_ldos(fcen,0,nfreq),until_after_sources=mp.stop_when_fields_decayed(20,mp.Ey,pt,1e-3))
eps_data=sim.get_array(center=mp.Vector3(),size=cell, component=mp.Dielectric)
ey_data=sim.get_array(center=mp.Vector3(),size=cell, component=mp.Ey)

    #plot eps_data
    
#    from mayavi import mlab
#    s = mlab.contour3d(eps_data, colormap="YlGnBu")
#    mlab.show()

plt.figure(dpi=160)

plt.imshow(eps_data.transpose(),interpolation='spline36',cmap='binary')
plt.imshow(ey_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()



                  
                 



