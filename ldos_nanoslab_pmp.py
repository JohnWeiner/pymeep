import meep as mp
import numpy as np
import sys
import matplotlib.pyplot as plt
import argparse
from meep.materials import Ag,Graph

def main(args):
    sx=8.0 #spatial extent along x including pmls (μm)
    sy=4
    sz=0
    dpml=1.0
    cell = mp.Vector3(sx,sy,sz)
    pml_layers=[mp.PML(dpml)]     
    resolution=args.res
    wvl=args.wvl #source wavelength
    fcen=1/wvl #center frequency
    df=0 #frequency bandwidth
    nfreq=1 #number of frequencies
    dw=args.dw #  slab thickness increment(um)
    w_init=args.w_init # initial slab thickness(μm)
    n=args.n
    w=w_init + n*dw #next slab thickness
    s=0.030 #slit width
    print("wavelength =", wvl, "μm")
    print("slab size =",w,"μm")
    print("center frequency =", fcen, "1/μm")

    geometry=[mp.Block(mp.Vector3(mp.inf,w,mp.inf),
                       center=mp.Vector3(0, 0.5*w),
                       material=Ag)]
    source=[mp.Source(mp.GaussianSource(fcen,df,nfreq),
                 component=mp.Ex,
                 center=mp.Vector3(0, -0.5*(sy-2.1), 0),
                 size=mp.Vector3(sx-2.0, 0, 0))]
    symmetries=[mp.Mirror(mp.X),mp.Mirror(mp.Z)]
    sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers,
                  filename_prefix='slab_noslit')
    sim.use_output_directory()
    
    pt=mp.Vector3(0,-0.5*(sy-2.1),0)#point where field intensity is measured (usually at source position)
    
    slab_flux_in_region=mp.FluxRegion(center=mp.Vector3(0, -0.005, 0), size=mp.Vector3(sx, 0, 0)) #incident flux monitor 5nm above slab.
    slab_flux_in=sim.add_flux(fcen,df,nfreq,slab_flux_in_region)
    slab_flux_in_data=sim.get_flux_data(slab_flux_in) #data are the E and H fields used to calculate S=ExH
    slab_flux_out_region=mp.FluxRegion(center=mp.Vector3(0, w+0.005, 0), size = mp.Vector3(sx, 0, 0)) #trans flux monitor 5nm below slab.
    slab_flux_out=sim.add_flux(fcen,df,nfreq,slab_flux_out_region)
    slab_flux_out_data=sim.get_flux_data(slab_flux_out)
    
    sim.run(mp.dft_ldos(fcen,df,nfreq),
        mp.at_beginning(mp.output_epsilon),
        until_after_sources=mp.stop_when_fields_decayed(10, mp.Hz, pt,1e-5))

    slab_flux_input=mp.get_fluxes(slab_flux_in)
    slab_flux_output=mp.get_fluxes(slab_flux_out)
    
    print('incident flux slab =',slab_flux_input,' ',
          'transmitted flux slab =',slab_flux_output,' ',
          'normed transmitted flux=',np.divide(slab_flux_output, slab_flux_input))
    
    eps_data_slab=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx, sy, sz), component=mp.Dielectric)
    ex_data_slab=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx, sy, sz), component=mp.Ex)
    hz_data_slab=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx,sy,sz), component=mp.Hz)

    sim.reset_meep()
    
    geometry=[mp.Block(mp.Vector3(mp.inf, w, mp.inf),
                       center=mp.Vector3(0, 0.5*(w)),
                       material=Ag),
          mp.Block(mp.Vector3(s, w, 0),
                  center=mp.Vector3(0, 0.5*(w), 0),
                   material=mp.Medium(epsilon=1))]

    sim=mp.Simulation(cell_size=cell,
                  geometry=geometry,
                  sources=source,
                  resolution=resolution,
                  boundary_layers=pml_layers,
                  filename_prefix="slab_slit")
    sim.use_output_directory()
    
    slit_flux_in_region=mp.FluxRegion(center=mp.Vector3(0, -0.005, 0), size=mp.Vector3(sx, 0, 0)) #same as slab_flux_in_region
    slit_flux_in=sim.add_flux(fcen, df, nfreq, slit_flux_in_region)
    slit_flux_in_data=sim.get_flux_data(slit_flux_in)
    slit_flux_out_region=mp.FluxRegion(center=mp.Vector3(0, w+0.005, 0), size=mp.Vector3(sx, 0, 0))#same as slab_flux_out_region
    slit_flux_out=sim.add_flux(fcen, df, nfreq, slit_flux_out_region)
    slit_flux_out_data=sim.get_flux_data(slit_flux_out)
    
    sim.load_minus_flux_data(slit_flux_out,slab_flux_out_data)
    #subract  transmitted slab flux data (slab_flux_out_data) from slit_flux_out.  This is a correction so that flux only
    #from the slit is registered in slit_flux_out.
    
    sim.run(mp.dft_ldos(fcen,0,nfreq),mp.at_beginning(mp.output_epsilon),
        until_after_sources=mp.stop_when_fields_decayed(10, mp.Hz, pt,1e-4))

    slit_flux_input=mp.get_fluxes(slit_flux_in)
    slit_flux_output=mp.get_fluxes(slit_flux_out)
    print('slit flux net =',slit_flux_output,'  ', 'slit_flux_normed =',np.divide(slit_flux_output, slab_flux_input))
    eps_data_slit=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx, sy, sz), component=mp.Dielectric)
    ex_data_slit=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx, sy, sz), component=mp.Ex)
    hz_data_slit=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx,sy,sz), component=mp.Hz)
    
    slabFlux=[]
    slabFlux=np.append(slabFlux, slab_flux_input)
    slitFlux=[]
    slitFlux=np.append(slitFlux, slit_flux_output)
    fracFlux=np.divide(slitFlux,slabFlux)
    print('normalised slit flux,', end=" ") #suppress the print newline function with end=" "
    np.savetxt(sys.stdout,fracFlux,fmt='%7.5f') #print to stdout transmitted slit flux normalised to input flux.
    print('slab thickness,', end=" ")
    print(w)
    
    #-------------------------------- Next three lines ok for data file in mp meep, but writes data np times (np no. processors) in pmp.
    #f=open('fracFL.dat','ab') 
    #np.savetxt(f,fracFl,fmt='%6.5f')   
    #f.close()
    #----------------------------------------------------
    
    eps_data_slit=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx,sy,sz), component=mp.Dielectric)
    hz_data_slit=sim.get_array(center=mp.Vector3(0,0,0),size=mp.Vector3(sx,sy,sz), component=mp.Hz)
    hz_scat=hz_data_slit - hz_data_slab

if __name__ == '__main__':  #begin parsing the arguments in the function call to "main".
    parser = argparse.ArgumentParser() #create the parser object.
    parser.add_argument('-res', type=int, default=50, help='resolution (default: 50 pixels/100 nm)') #resolution argument
    parser.add_argument('-wvl', type=float, default=500, help='wavelength corresponding to frequency of point dipole(default: 500 nm )') #wavelength argument.
    parser.add_argument('-w_init', type=float, default =0.050, help='initial slab thickness: (default: 0.050 μm)') #initial slab thickness argument
    parser.add_argument('-dw',type=float, default=0.002, help='slab thickness increment: (default: 0.002μm') #slab thickness increment argument
    parser.add_argument('-n',type=int, default =1, help='multiple of thickness increment: (default: 1')
    args = parser.parse_args()  #put the arguments created by the parser in args
    main(args) #put args into function "main".
