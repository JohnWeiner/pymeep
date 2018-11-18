import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import argparse
from meep.materials import Ag,Graph

def main(args):
    sx=3.0 #spatial extent along x including pmls (μm)
    sy=3.0
    sz=3.0
    dpml=1.0

    cell = mp.Vector3(sx,sy,sy)
    pml_layers=[mp.PML(dpml)]
    geometry=[mp.Cylinder(center=mp.Vector3(0,0,0),
                          height=mp.inf,
                          radius=0.505,
                          axis=mp.Vector3(0,0,1),
                          material=Graph),
        mp.Cylinder(center=mp.Vector3(0,0,0),
                          height=mp.inf,
                          radius=0.5,
                          axis=mp.Vector3(0,0,1),
                          material=mp.Medium(epsilon=3.9))]     
    resolution=args.res
    wvlmax=40
    fmin=1/40
    wvlmin=20
    fmax=1/20
    wvl=args.wvl
    fcen=1/wvl
    df=fmax-fmin
    nfreq=1
    print("wavelength =", wvl,"μm")
    print("center frequency =", fcen, "1/μm")

    source=[mp.Source(mp.GaussianSource(fcen,df,nfreq),
                 component=mp.Ey,
                 center=mp.Vector3(0,0.510,0))]

    symmetries=[mp.Mirror(mp.X),mp.Mirror(mp.Z)]

    sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers)

    pt=mp.Vector3(0,0.510,0)
       
    sim.run(mp.dft_ldos(fcen,df,nfreq),until_after_sources=mp.stop_when_fields_decayed(20,mp.Ey,pt,1e-3))

    eps_data=sim.get_array(center=mp.Vector3(),size=cell, component=mp.Dielectric)

    #plot eps_data

    plt.figure(dpi=160)
    plt.imshow(eps.data.transpose(), interpolation='spline36',cmap='binary')
    plt.axis('off')
    plt.show

#end of def main(args)

if __name__ == '__main__':  #begin parsing the arguments in the function call to "main".
    parser = argparse.ArgumentParser() #create the parer object.
    parser.add_argument('-res', type=int, default=50, help='resolution (default: 50 pixels/100 nm)') #resolution argument
    parser.add_argument('-wvl', type=float, default=500, help='wavelength corresponding to frequency of point dipole(default: 500 nm )') #wavelength argument
    args = parser.parse_args()  #put the arguments created by the parser in args
    main(args) #put args into function "main".


                  
                 



