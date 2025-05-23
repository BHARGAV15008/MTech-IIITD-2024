# -*- coding: utf-8 -*-
"""ML_project_N_body_simulation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12JU24lUqGqljprFSB2PLQdTw6Hk6RM5w
"""

import numpy as np
import pandas as pd
from multiprocessing import process,Pool
from functools import partial

def find_force_1on2(m1,r1,m2,r2):
  G=6.65*10**-11
  epsilon=10**-10 # to avoid infinite
  r=np.array(r1)-np.array(r2)
  f=G*m1*m2/((np.linalg.norm(r)+epsilon)**3)
  f=f*r
  # print(f"f:{f}")
  return f


def total_force(m_index,mass,position):
  # print(f"mass.shape:{mass.shape}")
  # print(f"position.shape:{position.shape}")
  # print(f"position[0].shape:{position[:][0].shape}")
  # print(f"position[0]:{position[0]}")
  # print(f"mass[0].shape:{mass[0].shape}")
  with Pool(processes=len(mass)) as pool:
    complete=[i for i in range(len(mass))]; complete.remove(m_index)
    f_partial=partial(find_force_1on2,mass[m_index],position[m_index])
    # force=pool.map(f_partial,[(mass[i],position[i]) for i in complete])
    #force=pool.starmap(f_partial,zip([mass[i] for i in complete],[position[i] for i in complete]))
    
    #force=pool.starmap(f_partial,[(mass[i],position[i]) for i in complete])
    force=[pool.starmap_async(f_partial,[(mass[i],position[i]) for i in complete])]
    all_forces=np.array([force_handle.get() for force_handle in force][0])
    pool.close()
    pool.terminate()
    pool.join()
    #force=pool.map(find_force_1on2,mass[m_index],position[m_index],[mass[i] for i in complete],[position[i] for i in complete])
  # force=np.array([find_force_1on2(mass[m_index],mass[i],position[m_index],position[i]) for i in range(len(mass)) if i!=m_index])
  #total_force=np.sum(force,axis=0)
  total_force=np.sum(all_forces,axis=0)
  # print(f"total_force:{total_force}")
  return total_force

def get_new_pos(index,mass,total_force,r,u,dt):
  a=total_force/mass
  v=u+a*dt
  s=u*dt+(0.5*a*dt**2)
  r=r+s
  # print(f"r:{r},s:{s}")
  #print(f"a:{a}")
  #print(f"dt:{dt}")
  #print(f"a*dt:{a*dt}")
  #print(f"u:{u},v:{v}")
  return (index,r,v)


def get_new_pos_v2(index,all_mass,all_position,all_u,dt):
  def total_force(m_index,mass,position):
    # print(f"mass.shape:{mass.shape}")
    # print(f"position.shape:{position.shape}")
    # print(f"position[0].shape:{position[:][0].shape}")
    # print(f"position[0]:{position[0]}")
    # print(f"mass[0].shape:{mass[0].shape}")
    with Pool(processes=len(mass)) as pool:
      complete=[i for i in range(len(mass))]; complete.remove(m_index)
      f_partial=partial(find_force_1on2,mass[m_index],position[m_index])
      # force=pool.map(f_partial,[(mass[i],position[i]) for i in complete])
      #force=pool.starmap(f_partial,zip([mass[i] for i in complete],[position[i] for i in complete]))
    
      #force=pool.starmap(f_partial,[(mass[i],position[i]) for i in complete])
      force=[pool.starmap_async(f_partial,[(mass[i],position[i]) for i in complete])]
      all_forces=np.array([force_handle.get() for force_handle in force][0])
      pool.close()
      pool.terminate()
      pool.join()
      #force=pool.map(find_force_1on2,mass[m_index],position[m_index],[mass[i] for i in complete],[position[i] for i in complete])
    # force=np.array([find_force_1on2(mass[m_index],mass[i],position[m_index],position[i]) for i in range(len(mass)) if i!=m_index])
    #total_force=np.sum(force,axis=0)
    total_force=np.sum(all_forces,axis=0)
    # print(f"total_force:{total_force}")
    return total_force
	
  def find_force_1on2(m1,r1,m2,r2):
    G=6.65*10**-11
    epsilon=10**-10 # to avoid infinite
    r=np.array(r1)-np.array(r2)
    f=G*m1*m2/((np.linalg.norm(r)+epsilon)**3)
    f=f*r
    # print(f"f:{f}")
    return f
  #new_pos=pool.starmap(get_new_pos,[(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])
  net_force=total_force(index,all_mass,all_position)
  a=net_force/all_mass[index]
  v=all_u[index]+a*dt
  s=all_u[index]*dt+(0.5*a*dt**2)
  r=r+s
  return (index,r,v)

def simulate_galaxy_v2(r,v,mass,dt,total_time):
  f_p="n_body/object_"
  r_old=r;v_old=v;r_new=np.empty(r_old.shape);v_new=np.empty(v_old.shape)
  file_var=[None]*len(mass)
  for i in range(len(mass)):
    file_var[i]=open(f_p+str(i)+".csv",'w')
    file_var[i].writelines('mass,x,y,z,vx,vy,vz');file_var[i].writelines('\n')
  for epoch in range(int(total_time/dt)):
    with Pool(processes=len(mass)) as pool:
      #r_new,v_new=pool.starmap(get_new_pos,zip([mass[i] for i in range(len(mass))],[total_force(i,mass,r_old) for i in range(len(mass))],[r_old[i] for i in range(len(mass))],[v_old[i] for i in range(len(mass))],[dt for i in range(len(mass))]))
     # (r_new,v_new)=pool.starmap(get_new_pos,[(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])
      
      new_pos=pool.starmap(get_new_pos,[(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])
    for i in range(len(mass)):
      file_var[i].writelines(str(mass[i])+','+','.join(map(str,list(np.concatenate((new_pos[i][0],new_pos[i][1]),axis=0)))))
      file_var[i].writelines("\n")
      r_old[i]=new_pos[i][0];v_old[i]=new_pos[i][1]  


def simulate_galaxy(r,v,mass,dt,total_time):
  f_p="n_body/object_"
  r_old=r;v_old=v;r_new=np.empty(r_old.shape);v_new=np.empty(v_old.shape)
  file_var=[None]*len(mass)
  for i in range(len(mass)):
    file_var[i]=open(f_p+str(i)+".csv",'w')
    file_var[i].writelines('mass,x,y,z,vx,vy,vz');file_var[i].writelines('\n')
  for epoch in range(int(total_time/dt)):
    print(f"Inside epoch:{epoch}")
    with Pool(processes=len(mass)) as pool:
      #r_new,v_new=pool.starmap(get_new_pos,zip([mass[i] for i in range(len(mass))],[total_force(i,mass,r_old) for i in range(len(mass))],[r_old[i] for i in range(len(mass))],[v_old[i] for i in range(len(mass))],[dt for i in range(len(mass))]))
     # (r_new,v_new)=pool.starmap(get_new_pos,[(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])
      
      #new_pos=pool.starmap(get_new_pos,[(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])
      
      new_pos_list=[pool.starmap_async(get_new_pos,[(i,mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt) for i in range(len(mass))])]
      #new_pos_list=[pool.starmap_async(get_new_pos_v2,[(i,mass,r_old,v_old,dt) for i in range(len(mass))])]
      new_pos=[position_handle.get() for position_handle in new_pos_list][0]
      #pool.close()
      #pool.terminate()
      #pool.join()
      #print(f"new_pos:{new_pos}")
      #print(f"new_pos[0][0]:{new_pos[0][0]}")
      #print(f"new_pos[0][1]:{new_pos[0][1]}")
      #print(f"new_pos[0][2]:{new_pos[0][2]}")
      #for i in range(len(mass)):
      for j in range(len(mass)):
        '''
        print(f"i:{i}")
        print(f"new_pos[{i}]:{new_pos[i]}")
        print(f"new_pos[{i}][0]:{new_pos[i][0]}")
        print(f"new_pos[{i}][1]:{new_pos[i][1]}")
        print(f"type(new_pos[{i}][0]):{type(new_pos[i][0])}")
        print(f"type(new_pos[{i}][1]):{type(new_pos[i][1])}")
        print(f"{np.concatenate((new_pos[i][0],new_pos[i][1]),axis=0)}")
        '''
        #file_var[i].writelines(str(list(np.concatenate((new_pos[i][0],new_pos[i][1]),axis=0))))
        #file_var[i].writelines(','.join(map(str,list(np.concatenate((new_pos[i][0],new_pos[i][1]),axis=0)))))
      
        #file_var[i].writelines(str(mass[i])+','+','.join(map(str,list(np.concatenate((new_pos[i][0],new_pos[i][1]),axis=0)))))
        i=new_pos[j][0]
        #print(f"i:{i},j:{j}")
        file_var[i].writelines(str(mass[i])+','+','.join(map(str,list(np.concatenate((new_pos[i][1],new_pos[i][2]),axis=0)))))
        file_var[i].writelines("\n")
        #print(f"new_pos.shape:{new_pos.shape}")
        '''
        print(f"new_pos[0][{i}]:{new_pos[0][i]}")
        print(f"r_old.shape:{r_old.shape}")
        '''
        #r_old[i]=new_pos[i][0];v_old[i]=new_pos[i][1]
        r_old[i]=new_pos[i][1];v_old[i]=new_pos[i][2]
        #print(f"new_pos[{i}]:{new_pos[i]}")
        #print(f"r_old[{i}]:{r_old[i]}")
    '''
    for i in range(len(mass)):
      r_new[i],v_new[i]=get_new_pos(mass[i],total_force(i,mass,r_old),r_old[i],v_old[i],dt)
    r_old=r_new;v_old=v_new
    '''
  #print(f"new_pos:{new_pos}")
  #print(f"r_new:{r_new}")

def main_v1():
	num_fragments = int(100)        # Number of fragments created after explosion
	total_mass = 1e30            # Total mass (in kg)
	min_mass = 1e23              # Minimum mass of individual fragments (in kg)
	max_mass = 1e26              # Maximum mass of individual fragments (in kg)
	max_velocity = 1e4           # Maximum velocity of fragments (in m/s)
	explosion_radius = 1e6       # Explosion radius (in meters)
	G = 6.67430e-11              # Gravitational constant (m^3 kg^-1 s^-2)
	G = 4.3009e-3			# parses(distance), kms-1(velocity), 
	k_B = 1.380649e-23           # Boltzmann constant (J/K)
	T = 1e5                       # Temperature (Kelvin) for Maxwell-Boltzmann distribution
	mass_decay_rate=0.001
	conic_section_split=5


	fragment_masses = np.random.uniform(min_mass, max_mass, num_fragments)
	theta = np.random.uniform(0, 2 * np.pi, num_fragments)  # Random azimuthal angle
	phi = np.random.uniform(0, np.pi, num_fragments)         # Random polar angle
	speed = np.random.normal(0, np.sqrt(k_B * T / fragment_masses), num_fragments)  # Maxwell-Boltzmann distribution

	# Calculate velocity components in 3D space (spherical to Cartesian conversion)
	vx = speed * np.sin(phi) * np.cos(theta)  # X velocity component
	vy = speed * np.sin(phi) * np.sin(theta)  # Y velocity component
	vz = speed * np.cos(phi)                 # Z velocity component

	# Generate random initial positions (within the explosion radius)
	r = np.random.uniform(0, explosion_radius, num_fragments)
	#r = np.random.uniform(explosion_radius/(1e2), explosion_radius, num_fragments)
	x_initial = r * np.sin(phi) * np.cos(theta)
	y_initial = r * np.sin(phi) * np.sin(theta)
	z_initial = r * np.cos(phi)

	# r_old=np.array([x_initial,y_initial,z_initial])
	r_old=np.transpose(np.vstack([x_initial,y_initial,z_initial]))
	# r_old=np.array([np.transpose(x_initial),np.transpose(y_initial),np.transpose(z_initial)])
	v_old=np.transpose(np.vstack([vx,vy,vz]))
	r_new=np.empty(r_old.shape);v_new=np.empty(v_old.shape)
	dt=int(86400/20000)  #in seconds
	total_time=dt*2 #in seconds

	r_new=simulate_galaxy(r_old,v_old,fragment_masses,dt=dt,total_time=total_time)

	# for epoch in range(int(total_time/dt)):
	#   for i in range(num_fragments):
	#     r_new[i],v_new[i]=get_new_pos(fragment_masses[i],total_force(i,fragment_masses,r_old),r_old[i],v_old[i],dt)
	#   r_old=r_new;v_old=v_new


	#print(f"r_new:\n{r_new}")
	# print(f"r_old[0]:\n{r_old[0]}")

if __name__=="__main__":
	main_v1()
