import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import os
import MDAnalysis as mda

#set bigger font sizes
SMALL_SIZE = 18
MEDIUM_SIZE = 18
BIG_SIZE = 20
plt.rc('font', size=SMALL_SIZE)        # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)   # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE-3)  # legend fontsize
plt.rc('figure', titlesize=BIG_SIZE)   # fontsize of the figure title

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 

def get_distance(xyz1, xyz2):
    distance = 0
    for i in range(3):
        distance += np.square((xyz1[i]-xyz2[i]))
    return np.sqrt(distance)        

####################change below####################
geo_path    = "/data/HOME_BACKUP/pengchao/Oil/dpmd/oil_droplet/geo"
root_path   = "/data/HOME_BACKUP/pengchao/Oil/dpmd/oil_droplet/44c10h22_5050h2o/003/charge"
sav_path    = os.path.join(root_path,'surf_chg')
data_geo    = "droplet_44c10h22_5050h2o_atomic.data"
trj_name    = "xyz.lammpstrj"
droplet_center = np.array([0.,0.,0.])
trj_step    = 1
trj_skip    = 0
delta_r     = 2  # Angstrom
####################change above####################
mkdir(sav_path)
data_geo    = os.path.join(geo_path,data_geo)
trj_file    = os.path.join(root_path,trj_name)

u = mda.Universe(data_geo,trj_file, atom_style='id type x y z',format='LAMMPSDUMP')
atom_num = len(u.atoms)
traj_num = len(u.trajectory)
box_length  = [u.dimensions[0],u.dimensions[1],u.dimensions[2]] # Angstrom

choose_frames = range(trj_skip,traj_num,trj_step)

with open(trj_file, "r") as file:
    lines = file.readlines()
q_values = []
for i, line in enumerate(lines):
    if line.startswith("ITEM: NUMBER OF ATOMS"):
        q_values.extend([float(row.split()[5]) for row in lines[i+7:i+7+atom_num]])

q_array = np.array(q_values).reshape((len(choose_frames), atom_num))

edge_start  = 0
edge_end    = box_length[2]/2
bin_edges   = np.linspace(edge_start, edge_end, int((edge_end-edge_start)/delta_r)+1)
bin_centers = bin_edges[:-1] + delta_r/2

q_counts = np.full(bin_centers.size, fill_value=0.0)
q_counts_list = q_counts
for i in range(len(choose_frames)-1):
    q_counts_list = np.vstack((q_counts_list, q_counts))

for i in range(len(choose_frames)):
    u.trajectory[int(i*trj_step)]
    for k in range(atom_num):
        z_atom = u.atoms[k].position
        _d = get_distance(z_atom, droplet_center)
        hist, _ = np.histogram(_d, bins=bin_edges)           
        q_counts_list[i] += hist*q_array[i][k]

v_list = []
for i in bin_edges[1:]:
    v = 4/3*np.pi*(np.power(i,3)-np.power(i-delta_r,3))*1e-3 #nm^3
    v_list.append(v)    

q_density_avg = np.average(q_counts_list, axis=0)

q_density_vol = []
for i in range(len(q_density_avg)):
    d = q_density_avg[i]/v_list[i]
    q_density_vol.append(d)

Dfile = open(os.path.join(sav_path, "charge_step{0}_dr{1}.txt".format(trj_step,delta_r)), 'w+')
Dfile.write('# %16s%16s%16s\n' %('Distance(Angstrom)','Charge(e)','Charge(e/nm^3)'))
for i in range(len(bin_centers)):
    Dfile.write('%16.8f%16.8f%16.8f\n' %(bin_centers[i],q_density_avg[i],q_density_vol[i]))
Dfile.close()

fig = plt.figure(figsize=(15.5,6.5), dpi=150, facecolor='white')
ax1 = fig.add_subplot(1, 2, 1)
ax1.plot(bin_centers, q_density_avg, lw=2)
ax1.set_xlabel("Distance to center "+r"$\ \rm (\AA)$")
ax1.set_ylabel("Charge (e)")

ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(bin_centers, q_density_vol, lw=2)
ax2.set_xlabel("Distance to center "+r"$\ \rm (\AA)$")
ax2.set_ylabel("Charge (e/nm$^3$)")
fig.show()
fig.savefig(os.path.join(sav_path, "charge_step{0}_dr{1}.png".format(trj_step,delta_r)), dpi=200, bbox_inches='tight')
