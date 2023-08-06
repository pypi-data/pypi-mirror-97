import mechanica as m

p = m.Potential.overlapping_sphere(mu=10, max=20)

p.plot(s=2, force=True, potential=True, ymin=-10, ymax=8)
