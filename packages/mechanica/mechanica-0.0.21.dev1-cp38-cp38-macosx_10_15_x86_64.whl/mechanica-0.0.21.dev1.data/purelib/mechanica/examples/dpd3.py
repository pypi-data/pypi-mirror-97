import mechanica as m
import numpy as np

m.Simulator(dt=0.1, dim=[15, 12, 10],
            bc={'x':'no_slip',
                'y':'periodic',
                'bottom':'no_slip',
                'top':{'velocity':[-0.1, 0, 0]}},
            perfcounter_period=100)

# lattice spacing
a = 2.5

m.universe.boundary_conditions.left.restore = 0.5

class A (m.Particle):
    radius = 2
    style={"color":"seagreen"}
    dynamics = m.Newtonian
    mass=10

dpd = m.Potential.dpd(alpha=0.5, gamma=1, sigma=0.1, cutoff=2)

m.bind(dpd, A, A)
m.bind(dpd, A, m.Universe.boundary_conditions.left)


uc = m.lattice.sc(a, A)

parts = m.lattice.create_lattice(uc, [5, 5, 5])

print(m.universe.boundary_conditions)

m.show()
