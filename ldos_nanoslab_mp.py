import meep as mp
import numpy as np
import matplotlib.pyplot as plt
#import argparse
from meep.materials import Ag,Graph

#fdef main(args):
sx=8.0 #spatial extent along x including pmls (μm)
sy=4
sz=0
dpml=1.0

cell = mp.Vector3(sx,sy,sz)
pml_layers=[mp.PML(dpml)]
geometry=[mp.Block(mp.Vector3(mp.inf,0.050,0),
                       center=mp.Vector3(0,0.025,0),
                       material=Graph)]
#          mp.Block(mp.Vector3(0.030,0.050,0),
#                   center=mp.Vector3(0,0.025,0),
#                   material=mp.Medium(epsilon=1.0))]       
resolution=200
#wvlmax=1.0
#fmin=1/wvlmax
#wvlmin=0.100
#fmax=1/wvlmin
wvl=30.0
fcen=1/wvl
df=0
nfreq=1
print("wavelength =", wvl,"μm")
print("center frequency =", fcen, "1/μm")

#source=[mp.Source(mp.ContinuousSource(fcen,df,nfreq),
#                 component=mp.Ex,
#                 center=mp.Vector3(0,-0.90,0),
#                 size=mp.Vector3(sx-2.1,0,0))]

source=[mp.Source(mp.GaussianSource(fcen,df,nfreq),
                 component=mp.Ex,
                 center=mp.Vector3(0,-0.90,0),
                 size=mp.Vector3(sx-2.1,0,0))]
symmetries=[mp.Mirror(mp.X),mp.Mirror(mp.Z)]
sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers,
                  filename_prefix='ref_slab')
pt=mp.Vector3(0,-0.90,0)
sim.run(mp.dft_ldos(fcen,0,nfreq),
        mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ref_hz", mp.at_every(0.05, mp.output_hfield_z)),
        until_after_sources=mp.stop_when_fields_decayed(10,mp.Hz,pt,1e-3))
#sim.run(mp.dft_ldos(fcen,0,nfreq),mp.at_beginning(mp.output_epsilon),mp.at_end(mp.output_efield_x),until=50)
eps_data1=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx-2,sy-2,sz), component=mp.Dielectric)
ex_data1=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx-2,sy-2,sz), component=mp.Ex)
hz_data1=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx-2,sy-2,sz), component=mp.Hz)

plt.figure(dpi=160)
plt.imshow(eps_data1.transpose(),interpolation='spline36',cmap='binary')
plt.imshow(hz_data1.transpose(), interpolation='spline36', cmap='jet', vmin=0.5*hz_data1.min(),vmax=0.5*hz_data1.max(),alpha=0.9)
plt.axis('off')
plt.show()

sim.reset_meep()

geometry=[mp.Block(mp.Vector3(mp.inf,0.050,0),
                       center=mp.Vector3(0,0.025,0),
                       material=Graph),
          mp.Block(mp.Vector3(0.030,0.050,0),
                  center=mp.Vector3(0,0.025,0),
                   material=mp.Medium(epsilon=1))]

sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers,
                  filename_prefix="ref+scat")

sim.run(mp.dft_ldos(fcen,0,nfreq),mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ref+slit_hz", mp.at_every(0.05, mp.output_hfield_z)),
        until_after_sources=mp.stop_when_fields_decayed(10,mp.Hz,pt,1e-3))
#sim.run(mp.dft_ldos(fcen,0,nfreq),until=50)

eps_data2=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx-2,sy-2,sz), component=mp.Dielectric)
hz_data2=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx-2,sy-2,sz), component=mp.Hz)

hz_scat=hz_data2 - hz_data1
#np.savetxt('hz_scat.dat', hz_scat, delimiter=',')

plt.figure(dpi=160)
plt.imshow(eps_data2.transpose(),interpolation='spline36',cmap='binary')
plt.imshow(hz_scat.transpose(), interpolation='spline36', cmap='jet', vmin=0.1*hz_scat.min(), vmax=0.1*hz_scat.max(), alpha=0.9)
plt.axis('off')
plt.title("Hz Field, 50nm Graphene Slab, 30nm Slit: Source Ex (λ=30μm)")
plt.savefig("Hz_Graphene_Slab")
plt.show()
     
#end of def main(args)

#if __name__ == '__main__':  #begin parsing the arguments in the function call to "main".
 #   parser = argparse.ArgumentParser() #create the parser object.
 #   parser.add_argument('-res', type=int, default=50, help='resolution (default: 50 pixels/100 nm)') #resolution argument
 #   parser.add_argument('-wvl', type=float, default=500, help='wavelength corresponding to frequency of point dipole(default: 500 nm )') #wavelength argument
 #   args = parser.parse_args()  #put the arguments created by the parser in args
 #   main(args) #put args into function "main".
