import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import argparse
from meep.materials import Graph

def main(args):
    sx=4.0 #spatial extent along x including pmls (μm)
    sy=4.0
    sz=4.0
    dpml=1.0

    cell = mp.Vector3(sx,sy,sz)
    pml_layers=[mp.PML(dpml)]
    geometry=[mp.Sphere(radius=0.7,
          center=mp.Vector3(0,0,0),
                        material=Graph),
          mp.Sphere(radius=0.5,
                    center=mp.Vector3(0,0,0),
                    material=mp.Medium(epsilon=12.25))]                    
    resolution=args.res
    wvl=args.wvl/1000 #convert args.wvl from nm to μm
    fcen=1/wvl
    df=0.1*fcen
    nfreq=1
    print("wavelength =", wvl,"μm")
    print("center frequency =", fcen, "1/μm")

    source=[mp.Source(mp.GaussianSource(fcen,df,nfreq),
                 component=mp.Ex,
                 center=mp.Vector3(0,0.705,0))]

    symmetries=[mp.Mirror(mp.X),mp.Mirror(mp.Z)]

    sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers)

    pt=mp.Vector3(0,0.75,0)
       
    sim.run(mp.dft_ldos(fcen,df,nfreq),until_after_sources=mp.stop_when_fields_decayed(20,mp.Ex,pt,1e-9))
#sim.run(until_after_sources=mp.stop_when_fields_decayed(20, mp.Ex,pt,1e-9))
#end of def main(args)

if __name__ == '__main__':  #begin parsing the arguments in the function call to "main".
    parser = argparse.ArgumentParser() #create the parer object.
    parser.add_argument('-res', type=int, default=50, help='resolution (default: 50 pixels/100 nm)') #resolution argument
    parser.add_argument('-wvl', type=float, default=500, help='wavelength corresponding to frequency of point dipole(default: 500 nm )') #wavelength argument
    args = parser.parse_args()  #put the arguments created by the parser in args
    main(args) #put args into function "main".


                  
                 



