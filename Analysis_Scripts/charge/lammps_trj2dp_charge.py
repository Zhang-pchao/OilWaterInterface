import numpy as np
import os, sys
import glob
import shutil
import MDAnalysis as mda

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 

def get_dos_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if '.ados.' in file:
                file_list.append(os.path.join(root, file))
    return file_list

def type_raw(u, typemap, type_path, map_path):
    u.trajectory[0]
    w_map = open(map_path, 'w')
    for i in typemap:
        w_map.write(i + '\n')
    w_map.close()
    
    w_type = open(type_path, 'w')
    for ii in range(len(u.atoms)): # dataset order = atom index != predict charge order = atom type 
        if int(u.atoms[ii].type) ==   3: # O lmp type
            w_type.write(str(1) + '\n') 
        elif int(u.atoms[ii].type) == 2: # C
            w_type.write(str(3) + '\n')                 
        elif int(u.atoms[ii].type) == 1: # H
            w_type.write(str(0) + '\n') 
    w_type.close()    

def write_trj_head(j,u,new_trj,Q_flag):
    u.trajectory[j]
    new_trj.write("ITEM: TIMESTEP\n")
    new_trj.write("%d\n"%j)
    new_trj.write("ITEM: NUMBER OF ATOMS\n")
    new_trj.write("%d\n"%(len(u.atoms)))
    new_trj.write("ITEM: BOX BOUNDS pp pp pp\n")
    for i in range(3):
        new_trj.write("%.6f%12.6f\n"%(0.,u.dimensions[i]))
    if Q_flag:
        new_trj.write("ITEM: ATOMS id type x y z q   \n")
    else:
        new_trj.write("ITEM: ATOMS id type x y z    \n")

def check_npy(loadData):
    print(type(loadData))
    print(loadData.dtype)
    print(loadData.ndim)
    print(loadData.shape)
    print(loadData.size)
    print(loadData)    

geo_path    = "/data/HOME_BACKUP/pengchao/Oil/dpmd/oil_droplet/geo"
root_path   = "../"
trj_path    = root_path
sav_path    = os.path.join(root_path,"charge")

typemap     = ["H","O","N","C"]
data_geo    = ["droplet_44c10h22_5050h2o_atomic.data"][0]
trj_name    = "oil_5b.lammpstrj"
frames      = 100  # split frames in each dataset
trj_step    = 1
trj_skip    = 200
Q_flag      = True # False for dataset; True for lmp

data_geo    = os.path.join(geo_path,data_geo)
trj_file    = os.path.join(trj_path,trj_name)
u = mda.Universe(data_geo,trj_file, atom_style='id type x y z',format='LAMMPSDUMP')
atom_num = len(u.atoms)
traj_num = len(u.trajectory)
choose_frames = range(trj_skip,traj_num,trj_step)

o_atoms = len(u.select_atoms('type %s'%3)) # lmp type
c_atoms = len(u.select_atoms('type %s'%2))
h_atoms = len(u.select_atoms('type %s'%1))

total_xyz,total_box,total_alq,total_chg  = [],[],[],[]
new_trj    = open(os.path.join(sav_path,"xyz.lammpstrj"), "w+")
if Q_flag:
    predict_chg_path = os.path.join(sav_path,'predict')
    q_files    = 0
        
#for j in choose_frames:
for j in range(trj_skip,int(int(len(choose_frames)/frames)*frames),trj_step):
    u.trajectory[j]
    if Q_flag:
        charge_tmp = np.loadtxt("%s/charge.ados.out.%d"%(predict_chg_path,q_files), usecols=1)
        charge= charge_tmp
        
        #charge= np.zeros(atom_num)
        #o_tmp = charge_tmp[h_atoms:h_atoms+o_atoms] # 2  charge model type
        #h_tmp = charge_tmp[:h_atoms]  # 1
        #c_tmp = charge_tmp[-c_atoms:] # 3
        #o_idx,h_idx,c_idx=0,0,0
        ## dataset order = atom index != predict charge order = atom type, let charge order = atom index
        #for ii in range(atom_num):
        #    if int(u.atoms[ii].type) ==   3: # O lmp type
        #        charge[ii] = o_tmp[o_idx]
        #        o_idx+=1
        #    elif int(u.atoms[ii].type) == 2: # C
        #        charge[ii] = c_tmp[c_idx]
        #        c_idx+=1                 
        #    elif int(u.atoms[ii].type) == 1: # H
        #        charge[ii] = h_tmp[h_idx]
        #        h_idx+=1 
                
    else:
        total_box.append([u.dimensions[0],0.,0.,
                          0.,u.dimensions[1],0.,
                          0.,0.,u.dimensions[2]])
        total_alq.append(0.)            
    
    write_trj_head(j,u,new_trj,Q_flag)
    for k in range(atom_num):     
        if Q_flag:
            new_trj.write("%6d %3d %10.4f%10.4f%10.4f%10.4f\n"%(float(u.atoms[k].index)+1,
                                     float(u.atoms[k].type),float(u.atoms[k].position[0]),
                              float(u.atoms[k].position[1]),float(u.atoms[k].position[2]),
                                                                    float(charge[k])))
        else:
            total_xyz.append(u.atoms[k].position)
            total_chg.append(0.)
            #new_trj.write("%6d %3d %10.4f%10.4f%10.4f\n"%(float(u.atoms[k].index)+1,
            #                    float(u.atoms[k].type),float(u.atoms[k].position[0]),
            #            float(u.atoms[k].position[1]),float(u.atoms[k].position[2])))
    if Q_flag:
        q_files+=1

new_trj.close()
if not Q_flag:
    total_xyz_np = np.asarray(total_xyz,dtype=float).reshape(len(choose_frames),atom_num*3)
    total_box_np = np.asarray(total_box,dtype=float).reshape(len(choose_frames),9)
    total_alq_np = np.asarray(total_alq,dtype=float).reshape(len(choose_frames),1)
    total_chg_np = np.asarray(total_chg,dtype=float).reshape(len(choose_frames),atom_num)
    
    for sp in range(int(len(choose_frames)/frames)):
        save_path1 = os.path.join(sav_path,   "chg_data_sp", "%d"%(10001+sp))
        save_path2 = os.path.join(save_path1, "set.000")
        mkdir(save_path2)
        type_path  = os.path.join(save_path1,  "type.raw")
        map_path   = os.path.join(save_path1,  "type_map.raw")
        box_path   = os.path.join(save_path2,  "box.npy")
        xyz_path   = os.path.join(save_path2,  "coord.npy")
        alq_path   = os.path.join(save_path2,  "dos.npy")
        chg_path   = os.path.join(save_path2,  "atom_dos.npy")
        
        type_raw(u, typemap, type_path, map_path)    
        np.save(xyz_path, total_xyz_np[sp*frames:(sp+1)*frames])    
        np.save(box_path, total_box_np[sp*frames:(sp+1)*frames])   
        np.save(alq_path, total_alq_np[sp*frames:(sp+1)*frames])    
        np.save(chg_path, total_chg_np[sp*frames:(sp+1)*frames])

if not Q_flag:
    check_npy(loadData = np.load(os.path.join(save_path2,'coord.npy')))
    check_npy(loadData = np.load(os.path.join(save_path2,'box.npy')))
    check_npy(loadData = np.load(os.path.join(save_path2,'dos.npy')))
    check_npy(loadData = np.load(os.path.join(save_path2,'atom_dos.npy')))
