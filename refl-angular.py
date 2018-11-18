# This scrip is a function, def main(args), which is called by a bash script with arguments (args).
# The bash script is refl-angular.sh

import meep as mp
import argparse
import math

def main(args):

    resolution = args.res #res is the resolution argument that can be passed to main(args) in the bash script.

    dpml = 1.0              # PML thickness.
    sz = 10                 # size of computational cell (without PMLs).
    sz = 10 + 2*dpml # size of computational cell (with PMLs).
    cell_size = mp.Vector3(0,0,sz) #1-D computational space, along z.
    pml_layers = [mp.PML(dpml)] #put the PMLs around the comp. cell boundaries.

    wvl_min = 0.4           # min wavelength.
    wvl_max = 0.8           # max wavelength.
    fmin = 1/wvl_max        # min frequency.
    fmax = 1/wvl_min        # max frequency.
    fcen = 0.5*(fmin+fmax)  # center frequency.
    df = fmax-fmin          # frequency width.
    nfreq = 50              # number of frequency bins.

    # rotation angle (in degrees) of source: CCW around y axis, 0 degrees along +z axis
    theta_r = math.radians(args.theta) #converts degrees to radians; theta is an argument passed to main(args) by a bash script.

    # plane of incidence is xz
    k = mp.Vector3(math.sin(theta_r),0,math.cos(theta_r)).scale(fmin) #determines k vector in x-z plane.

    # if normal incidence, force number of dimensions to be 1
    if theta_r == 0:
        dimensions = 1
    else:
        dimensions = 3

    sources = [mp.Source(mp.GaussianSource(fcen,fwidth=df), component=mp.Ex, center=mp.Vector3(0,0,-0.5*sz+dpml))]
    #pulsed source placed on z-axis just at the left-had pml boundary.

    #attributes of the simulation object
    sim = mp.Simulation(cell_size=cell_size,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k, #when k_point is not zero, the fields are complex.
                        dimensions=dimensions,
                        resolution=resolution)

    refl_fr = mp.FluxRegion(center=mp.Vector3(0,0,-0.25*sz)) #location of the reflection flux monitor (flux region)
    refl = sim.add_flux(fcen, df, nfreq, refl_fr) #flux (Poynting vector normal component) collected by refl_fr

    #being "empty" run with no reflecting object.
    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(0,0,-0.5*sz+dpml), 1e-9))
    # Continues to run until intensity of Ex=1e-9 of max. value...checks for this condition every 50 time steps at source position.

    empty_flux = mp.get_fluxes(refl) #put the reflected flux in empty_flux
    empty_data = sim.get_flux_data(refl) #put the E(ω),H(ω) fields (from which flux is calculated, S(ω)=E(ω)xH(ω), in empty_data

    #reset the fields to zero.  End of "empty" run with no reflecting object.
    sim.reset_meep()
    #begin "reflection" run...add a block with n=3.5 for the air-dielectric interface

    geometry = [mp.Block(mp.Vector3(mp.inf,mp.inf,0.5*sz), center=mp.Vector3(0,0,0.25*sz), material=mp.Medium(index=3.5))]

    sim = mp.Simulation(cell_size=cell_size,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=k, #when k_point is not zero, the fields are complex, not real (the default)
                        dimensions=dimensions,
                        resolution=resolution)

    refl = sim.add_flux(fcen, df, nfreq, refl_fr) #refl is the object to which flux detected at refl_fr will be added.
    sim.load_minus_flux_data(refl, empty_data) #load the negative of the E,H field data from the "empty" run to refl.

    sim.run(until_after_sources=mp.stop_when_fields_decayed(50, mp.Ex, mp.Vector3(0,0,-0.5*sz+dpml), 1e-9))
    #run the FDTD programme again (this time with the reflecting slab in place).

    refl_flux = mp.get_fluxes(refl)
    #net reflected flux, calculated from the sum of the negative fields of the "empty run" and the fields from the "reflection" run
    freqs = mp.get_flux_freqs(refl)

    for i in range(nfreq):
        print("refl:, {}, {}, {}, {}".format(k.x,1/freqs[i],math.degrees(math.asin(k.x/freqs[i])),-refl_flux[i]/empty_flux[i]))#NB print(str.format)
        #print to the screen kx, wavelength, angle(deg), normalized reflected flux.  This line is the last one of the subroutine.

if __name__ == '__main__':  #begin parsing the arguments in the function call to "main".
    parser = argparse.ArgumentParser() #create the parer object.
    parser.add_argument('-res', type=int, default=200, help='resolution (default: 200 pixels/um)') #resolution argument
    parser.add_argument('-theta', type=float, default=0, help='angle of incident planewave (default: 0 degrees)') #theta argument
    args = parser.parse_args()  #put the arguments created by the parser in args
    main(args) #put args in  "main".
