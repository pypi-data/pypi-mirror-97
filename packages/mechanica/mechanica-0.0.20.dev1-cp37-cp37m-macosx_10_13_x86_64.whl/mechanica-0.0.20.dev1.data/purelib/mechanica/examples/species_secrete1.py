import mechanica as m
import numpy as n

m.Simulator()

class A(m.Particle):

    radius = 1

    species = ['S1', 'S2', 'S3']

    style = {"colormap" : {"species" : "S1", "map" : "rainbow", "range" : "auto"}}


a = A(m.Universe.center - [0, 1, 0])

b = A(m.Universe.center + [0, 1, 0])

a.species.S1 = 1

s.species.S1.secrete(0.5, b)

m.show()
