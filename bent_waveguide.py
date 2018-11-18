import meep as mp
import numpy as np
import matplotlib.pyplot as plt


cell = mp.Vector3(16,16,0)
geometry=[mp.Block(mp.Vector3(12,1,1e20),
                   center=mp.Vector3(-2.5,-3.5),
                   material=mp.Medium(epsilon=12)),
          mp.Block(mp.Vector3(1,12,1e20),
                   center=mp.Vector3(3.5,2),
                   material=mp.Medium(epsilon=12))]
pml_layers=[mp.PML(1.0)]
resolution=10
sources = [mp.Source(mp.ContinuousSource(wavelength=2*(11**0.5), width=20),
                     component=mp.Ez,
                     center=mp.Vector3(-7,-3.5),
                     size=mp.Vector3(0,1))]
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
        until=200)



eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure(dpi=100)
#plt.imshow(eps_data, interpolation='spline36', cmap='binary') Here is the waveguide with no transpose or flipud
#plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')  From original tutorial
#plt.imshow(np.flipud(eps_data.transpose()), interpolation='spline36', cmap='binary' Using np.flipud() for waveguide orientation
plt.imshow((np.flipud(np.transpose(eps_data))), interpolation='spline36', cmap='binary',extent=(-80,80,-80,80))#Using np.flipud() and np.transpose() for waveguide orientation.  Note the use of extents to "relable" the axes
plt.axis('on')
#plt.axis([0,160,0,160])
plt.xticks(np.arange(-80,90,10))
plt.yticks(np.arange(-80,90,10))
plt.xlabel('x')
plt.ylabel('y')
plt.title('Bent Waveguide')
plt.grid(True)
plt.show()

vals = [] #initialize the array named vals.

def get_slice(sim):
    center = mp.Vector3(0, -3.5)
    size = mp.Vector3(16, 0)
    vals.append(sim.get_array(center=center, size=size, component=mp.Ez))

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_every(0.6, get_slice),
        until=200)

plt.figure(dpi=100)
plt.imshow(vals, interpolation='spline36', cmap='RdBu')
plt.axis('off')
plt.show()

