#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os, sys
import glob
import shutil
import random

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def get_stru(lines, stru, name, length, lattice,
               keyword, atomlist, type_file, upfpath, orbpath, 
               drppath, upflist, orblist, descriptor):
    write_stru = open(stru, 'w')
    write_stru.write("ATOMIC_SPECIES" + '\n')
    for i in range(len(atomlist)):
        write_stru.write('%s 1.00 %s\n' %(atomlist[i],os.path.join(upfpath,upflist[i])))
    write_stru.write('\n\n')
    write_stru.write('LATTICE_CONSTANT\n')
    write_stru.write('%s\n\n' %lattice)
    write_stru.write('LATTICE_VECTORS\n')
    write_stru.write("%12.6f%12.6f%12.6f\n"  %(length[0],length[1],length[2]))
    write_stru.write("%12.6f%12.6f%12.6f\n"  %(length[3],length[4],length[5]))
    write_stru.write("%12.6f%12.6f%12.6f\n\n"%(length[6],length[7],length[8]))
    write_stru.write('ATOMIC_POSITIONS\n')
    write_stru.write('%s\n\n' %keyword)

    atomdict = {}
    for k in range(len(atomlist)): 
        atom_index = 0
        for i in range(len(type_file)):   
            if int(type_file[i]) == k:
                atom_index += 1
        atomdict[atomlist[k]] = atom_index  
    
    for k in range(len(atomlist)): 
        write_stru.write('%s\n' %atomlist[k])
        write_stru.write('0.0\n')
        write_stru.write('%d\n' %atomdict[atomlist[k]])
        for i in range(len(type_file)):   
            if int(type_file[i]) == k:
                write_stru.write("%12.6f%12.6f%12.6f%6d%2d%2d\n"%(lines[0+i*3],lines[1+i*3],
                                                                  lines[2+i*3],0,0,0))
    write_stru.write('\nNUMERICAL_ORBITAL\n')
    for i in range(len(atomlist)):
        write_stru.write('%s\n' %os.path.join(orbpath,orblist[i]))
    write_stru.write('\nNUMERICAL_DESCRIPTOR\n') 
    write_stru.write('%s\n' %os.path.join(drppath,descriptor))
    write_stru.close()

root_path = "/data/HOME_BACKUP/pengchao/deepmd2/lmp_dp/slab/lmp/DatasetWaterionSCAN/03/1000w_water_ion_slab0.005/npt_pure_water_dataset/npt_pure_water"
data_path = []
for file in os.listdir(root_path):
    data_path.append(file)

lattice  = '1.8897259886' #angstrom2bohr
keyword  = 'Cartesian'
atomlist = ['H','O'] # 0 1
upfpath  = '/data/HOME_BACKUP/pengchao/glycine/deepks/water_ion/pbe/iter'
orbpath  = '/data/HOME_BACKUP/pengchao/glycine/deepks/water_ion/pbe/iter'
drppath  = '/data/HOME_BACKUP/pengchao/glycine/deepks/water_ion/pbe/iter'
savpath  = '/data/HOME_BACKUP/pengchao/glycine/deepks/water_ion/pbe/test'
upflist  =['H_ONCV_PBE-1.0.upf',
           'O_ONCV_PBE-1.0.upf']
orblist  =['H_gga_6au_100Ry_2s1p.orb',
           'O_gga_7au_100Ry_2s2p1d.orb']
descriptor = 'jle.orb'

for i in data_path:
#for i in ['data.029']:
    npy_path = os.path.join(root_path,i,'set.000')
    crd_file = np.load(os.path.join(npy_path,'coord.npy'))
    box_file = np.load(os.path.join(npy_path,'box.npy'))
    #type_map_file = np.loadtxt(os.path.join(root_path,i,'type_map.raw'),usecols=0) # H O
    type_file = np.loadtxt(os.path.join(root_path,i,'type.raw'),usecols=0)  # 0 1
    frame_num = box_file.shape[0]
    atoms_num = type_file.shape[0]
    idx = 0
    for j in range(0,frame_num,1):
        idx += 1
        name = str(10000+idx)
        mkpath = os.path.join(savpath, str(int(i.split('.')[1])+100), name)
        mkdir(mkpath)
        stru = os.path.join(mkpath, 'STRU') 
        get_stru(crd_file[j], stru, name, box_file[j], lattice,
                   keyword, atomlist, type_file, upfpath, orbpath, 
                   drppath, upflist,  orblist,   descriptor)  
