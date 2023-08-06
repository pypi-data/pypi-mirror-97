#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import mechanica as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
# import time
import csv
from scipy.interpolate import griddata
from sympy import S, symbols, printing

# python poiseuille_plot.py

# universe parameters
dt = 0.1 # time step
x_dim = 15
y_dim = 12
z_dim = 10
dim = [x_dim, y_dim, z_dim] # universe dimensions
cutoff = 0.5 # cutoff radius 

# lattice parameters
a = 0.15 # lattice spacing
latDim = 30 # lattice dimensions

# initialize simulation
m.Simulator(dt=dt, dim=dim, cutoff=cutoff,
            bc={'x':'periodic',
                'y':'periodic',
                'z':'no_slip'})

# create fluid particles
class Fluid (m.Particle):
    radius = 0.2
    style={"color":"white"}
    dynamics = m.Newtonian
    mass=1

# fluid interaction potential
alpha = 0.5
gamma = 2.0
sigma = 1.0
rc = 1.0
dpd = m.Potential.dpd(alpha=alpha, gamma=gamma,sigma=sigma,cutoff=rc)
m.bind(dpd, Fluid, Fluid)

# boundary condition potential
bdpd = m.Potential.dpd(alpha=0.01, gamma=0.05,sigma=0.01,cutoff=1.0)
m.bind(bdpd, Fluid, m.Universe.boundary_conditions.top)
m.bind(bdpd, Fluid, m.Universe.boundary_conditions.bottom)

# driving pressure
g = 0.01 # magnitude
pressure = m.forces.ConstantForce([g, 0.0, 0.0])
m.bind(pressure, Fluid)

# lattice
uc = m.lattice.sc(a, Fluid) # lattice unit cell
parts = m.lattice.create_lattice(uc, [latDim, latDim, latDim]) # make lattice

# =============================================================================
# 
# plotting stuff
# 
# =============================================================================

particles = Fluid.items()
def plot(e):
    # get position and velocity coordinates (for quiver plot, haven't changed to grid)
    ps = range(len(particles))
    posXZ = np.asarray([[particles[p].position[0],particles[p].position[2]] for p in ps])
    velXZ = np.asarray([[particles[p].velocity[0],particles[p].velocity[2]] for p in ps])
    # print('pos: ',posXZ)
    # print('vel: ',velXZ)
    
    # compute velocity profile
    x_poly,y_poly,curve = velProfile(posXZ,velXZ)
    
    # compute viscosity
    eta = viscosity(posXZ,profile=curve)
    
    # make plots
    
    time = m.Universe.time # get time
    
    plt.figure(100,figsize=(4,3)) # flow field plot
    
    colormap,norm,colors,mappable = colorPlot(velXZ) # color arrows by magnitude
    
    # quiver plot
    plt.quiver(posXZ.T[0],posXZ.T[1],velXZ.T[0],velXZ.T[1],
                color=colormap(norm(colors)),
                scale_units='xy')
    plt.colorbar(mappable).set_label('velocity',labelpad=-25, y=1.07, rotation=0)
    plt.suptitle('Poiseuille Velocity (time: {:.2f})'.format(time))
    plt.title(r'$\alpha = {}, \gamma = {}, \sigma = {}, r = {}$'.format(alpha,gamma,sigma,rc),fontsize='small')
    plt.xlabel('x-direction')
    plt.ylabel('z-direction')
    # stream plot (without grid)
    # x,y,u,v,vel_mag = interpolate(posXZ.T[0],posXZ.T[1],velXZ.T[0],velXZ.T[1])
    # plt.streamplot(x[::5],y[::5],u[::5],v[::5],linewidth=0.5)
    
    # stream plot (with grid)
    vel_x,vel_z = streams()
    #pos_x,pos_z = np.meshgrid(np.arange(x_dim),np.arange(z_dim))

    #plt.streamplot(pos_x,pos_z,vel_x,vel_z)
    
    #plt.show(block=False)
    #plt.pause(0.01)
    #plt.clf()
    
    #plt.figure(101,figsize=(4,3)) # velocity profile plot
    
    #plt.scatter(posXZ.T[1],np.sqrt(velXZ.T[0]**2)) # velocity vs height
    #plt.xlabel('z-direction')
    #plt.ylabel('velocity')
    
    # plot polyfit velocity profile
    #plt.plot(x_poly,y_poly,
    #      color='red',
    #      label='velocity profile: ${:.2f}z^2 + {:.2f}z + {:.2f}$'.format(curve[0],curve[1],curve[2])
    #      + '\n viscosity: {:.2f}'.format(eta))
    # plt.ylim(0,3)
    #plt.suptitle('velocity profile (time: {:.2f})'.format(time))
    #plt.title(r'$\alpha = {}, \gamma = {}, \sigma = {}, r = {}$'.format(alpha,gamma,sigma,rc),fontsize='small')
    #plt.legend(fontsize='small')
    
    #plt.show(block=False)
    #plt.pause(0.01)
    #plt.clf()
    
    #plt.figure(102,figsize=(4,3)) # density plot
    
    slice_density,total_density = densityProfile()
    #plt.scatter(np.arange(z_dim),np.asarray(slice_density))
    #plt.suptitle(r'Density as a function of height $(\rho = {:.2f})$'.format(total_density))
    #plt.title(r'$\alpha = {}, \gamma = {}, \sigma = {}, r = {}$'.format(alpha,gamma,sigma,rc),fontsize='small')
    #plt.xlabel('z-direction')
    #plt.ylabel('density')
    
    #plt.show(block=False)
    #plt.pause(0.01)
    #plt.clf()

# def calcPressure(curve,eta):
#     '''
#     calculate pressure by integrating velocity profile to get flow rate.
#     plug into hagen-poiseuille equation
#     '''
#     pi = np.pi
#     const = (8*pi*eta*x_dim)/(y_dim*z_dim)
#     p = np.poly1d(curve) # velocity profile
#     i = p.integ() # integrate velocity profile (indefinite integral)
#     result = i(z_dim)-i(0) # flow rate (evaluate integral at boundaries)
#     pressure = const*result
#     return pressure
    

def viscosity(pos,profile,height=dim[2],force=g):
    '''
    compute viscosity
        inputs:
                pos - position vector
                profile - polyfit velocity profile
    '''
    rho = len(pos)/(15*12) # number density in slice
    eta = -(rho*g)/(2*profile[0]) # viscosity
    return eta

def densityProfile():
    grid = m.Universe.grid(dim)
    area = x_dim*y_dim
    volume = x_dim*y_dim*z_dim
    slice_density = []
    total_density = 0
    for k in range(z_dim):
        slice_density_k = 0
        for i in range(x_dim):
            for j in range(y_dim):
                slice_density_k += len(grid[i][j][k].positions())/area
                total_density+=len(grid[i][j][k].positions())
        slice_density.append(slice_density_k)
        total_density/=volume
    return slice_density,total_density
    

def velProfile(pos,vel):
    '''
    generate velocity profile
        inputs:
                pos - position vector
                vel - velocity vector
    '''
    curve = np.polyfit(pos.T[1],vel.T[0],2)
    poly = np.poly1d(curve)
    x_poly = np.linspace(pos.T[1].min(),pos.T[1].max(),100)
    y_poly = poly(x_poly)
    return x_poly, y_poly, curve

def colorPlot(vel):
    '''
    create mappable to color arrows in quiver plot by magnitude
        inputs:
            vel - velocity vector
    '''
    colors = np.sqrt(vel.T[0]**2 + vel.T[1]**2)
    norm = Normalize()
    norm.autoscale(colors)
    
    colormap = cm.viridis
    mappable = cm.ScalarMappable(cmap=colormap, norm=norm)
    return colormap,norm,colors,mappable

def streams():
    grid = m.Universe.grid(dim)
    vel_x = []
    vel_z = []
    for k in range(z_dim):
        for i in range(x_dim):
            # avg velocity at each point in slice down middle in xz-plane
            avg_vels_ik = grid[i][int(y_dim/2)][k].velocities().mean(axis=0)
            vel_x.append(avg_vels_ik[0]) # add x component
            vel_z.append(avg_vels_ik[2]) # add z component
    # vel_x = np.meshgrid(vel_x,vel_x)
    # vel_z = np.meshgrid(vel_x,vel_z)
    vel_x = np.asarray(vel_x).reshape((z_dim,x_dim)) # arrays for meshgrid
    vel_z = np.asarray(vel_z).reshape((z_dim,x_dim))
    return vel_x,vel_z
        
            

def interpolate(xx,yy,u,v):
    '''
    old interpolation function used before grid
    '''
    x = np.linspace(xx.min(), xx.max(), 50)
    y = np.linspace(yy.min(), yy.max(), 50)
    
    # grid coords for streamplot
    xi, yi = np.meshgrid(x,y)
    # print('shape: ',np.shape((xi,yi)))
    
    # for inerpoloation
    # tempX = xx.flatten()
    # tempY = yy.flatten()
    # tempU = u.flatten()
    # tempV = v.flatten()
    
    # print('shape 2: ', np.shape(list(zip(tempX,tempY))))
    # print('shape 3: ', np.shape(zip(tempX,tempY)))
    # print('shape 4: ', np.shape((tempX,tempY)))
    # interpolate
    # U = griddata((tempX,tempY), tempU, (xi,yi),method='nearest')
    # V = griddata((tempX,tempY), tempV, (xi,yi),method='nearest')
    U = griddata((xx,yy),u,(xi,yi),method='nearest')
    V = griddata((xx,yy),v,(xi,yi),method='nearest')
    
    #tempUV = np.sqrt(U**2 + V**2)
    # UV = griddata((tempX,tempY),np.sqrt(tempU**2+tempV**2),(xi,yi))
    UV = griddata((xx,yy),np.sqrt(u**2+v**2),(xi,yi))
    
    return xi,yi,U,V,UV

# itt = 0
# while itt<1000:
#     itt+=1
#     print('itt: ',itt)
#     m.step()

# run the simulator interactive
m.on_time(plot, period=0.1)
m.Simulator.run()   
