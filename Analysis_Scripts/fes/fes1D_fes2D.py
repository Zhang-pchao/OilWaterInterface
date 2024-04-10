#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import sys
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects


# In[2]:


import os
import plumed
import argparse

#reuse same plumed kernel, to avoid multiple warnings
PLUMED_KERNEL=plumed.Plumed()
from functools import partial
plumed.read_as_pandas = partial(plumed.read_as_pandas, kernel=PLUMED_KERNEL)

#some other plotting functions
from matplotlib.pyplot import MultipleLocator
from matplotlib.patches import Ellipse
from matplotlib.collections import PatchCollection
from IPython.display import clear_output


# In[3]:


#set bigger font sizes
SMALL_SIZE = 18
MEDIUM_SIZE = 18
BIG_SIZE = 20
plt.rc('font', size=SMALL_SIZE)        # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)   # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE-4)  # legend fontsize
plt.rc('figure', titlesize=BIG_SIZE)   # fontsize of the figure title


# In[4]:


colors = [
#          (31,59,115),
          (34,75,121),
          (40,108,133), 
#          (46,141,146),
          (57,156,146),
          (70,168,143),
          (85,180,138),
          (118,194,116),         
          (184,216,81),
          (216,220,72),
          (250,223,63),          
          (255,207,69),
          (255,186,78),          
          (252,164,83),
          (237,133,74),          
#          (222,102,64),
          (214,87,59),
         (255,255,255),
          ]  # R -> G -> B 
          
colornum=15
colors=list(tuple(i/255 for i in color) for color in colors)
#colors.reverse()
cm = LinearSegmentedColormap.from_list('my_list', colors, N=colornum)


# In[5]:


path1='/data/HOME_BACKUP/pengchao/Oil/dpmd/slab_24c10h22_256h2o'
path4='/data/HOME_BACKUP/pengchao/Oil/dpmd/slab_24c10h22_256h2o/100_003_bulk/5-10ns_b75/fes_reweight'
path5='/data/HOME_BACKUP/pengchao/glycine/dpmd/franklin/opes/013_water/014_58H2O_logd_cc_scan/fes_reweight'
data1='fes-rew.dat'
data2=['c5','c100','d8','d100','c8','c10','logd']
save_path=os.path.join(path1,'final_figs')
kJ2kcal=0.239005736
barrier=19.09945818 #water autoionization free energy barrier


# In[6]:


folder_f     = os.path.join("/data/HOME_BACKUP/pengchao/Oil/dpmd/slab_24c10h22_256h2o/100_003_bulk/5-10ns_b75/fes2D_2/logd_cc_bin200_block3_s0.02_0.02/")
max_fes    = 30 #kcal/mol
cvnames    = ['logd','cc']
cvnames2   = ['dd','cc']
Temp       = 300.0


# In[7]:


x,y,z=np.loadtxt(os.path.join(folder_f+"fes-rew.dat"),unpack=True)[:3]
z=z*kJ2kcal
z=z-z.min()
z[z>max_fes]=max_fes
yi = np.linspace(min(y), max(y), 200)
xi = np.linspace(min(x), max(x), 200)
X,Y=np.meshgrid(xi,yi)
zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='nearest')


# In[8]:


c05x       =np.loadtxt(os.path.join(path4,data2[0],data1),unpack=True)[0:1].flatten()
c05y,c05e  =np.loadtxt(os.path.join(path4,data2[0],data1),unpack=True)[1:3]*kJ2kcal
d08x       =np.loadtxt(os.path.join(path4,data2[2],data1),unpack=True)[0:1].flatten()
d08y,d08e  =np.loadtxt(os.path.join(path4,data2[2],data1),unpack=True)[1:3]*kJ2kcal
ld08x        =np.loadtxt(os.path.join(path4,data2[-1],data1),unpack=True)[0:1].flatten()
ld08y,ld08e  =np.loadtxt(os.path.join(path4,data2[-1],data1),unpack=True)[1:3]*kJ2kcal


# In[9]:


sc05x        =np.loadtxt(os.path.join(path5,data2[0],data1),unpack=True)[0:1].flatten()
sc05y,sc05e  =np.loadtxt(os.path.join(path5,data2[0],data1),unpack=True)[1:3]*kJ2kcal
sd08x        =np.loadtxt(os.path.join(path5,data2[2],data1),unpack=True)[0:1].flatten()
sd08y,sd08e  =np.loadtxt(os.path.join(path5,data2[2],data1),unpack=True)[1:3]*kJ2kcal
lsd08x         =np.loadtxt(os.path.join(path5,data2[-1],data1),unpack=True)[0:1].flatten()
lsd08y,lsd08e  =np.loadtxt(os.path.join(path5,data2[-1],data1),unpack=True)[1:3]*kJ2kcal


# In[10]:


def get_xy_min_max(filename,cvs):
    with open(filename) as f: 
        lines = f.readlines()
        for line in lines:
            if "SET min_%s"%cvs[0] in line:
                minss = float(line.split()[3])
            if "SET max_%s"%cvs[0] in line:
                maxss = float(line.split()[3])    
            if "SET min_%s"%cvs[1] in line:
                mindd = float(line.split()[3])
            if "SET max_%s"%cvs[1] in line:
                maxdd = float(line.split()[3])
    return (minss,maxss,mindd,maxdd)


# In[11]:


def get_mins(x,y,interface):
    y=list(y)
    min_value=min(y)
    min_index=y.index(min_value)
    return x[min_index]-interface,y[min_index]


# In[12]:


def energy_rank(x_values,data, marker_width=0.1, color='blue'):
    y_data = np.repeat(data, 2)
    x_data = [x_values[0]-(marker_width / 2),x_values[0]+(marker_width / 2),
                x_values[1]-(marker_width / 2),x_values[1]+(marker_width / 2),
                x_values[2]-(marker_width / 2),x_values[2]+(marker_width / 2),
               ]
    lines = []
    lines.append(plt.Line2D(x_data, y_data, lw=1, linestyle='dashed', color=color))
    for x in range(0, len(data) * 2, 2):
        lines.append(plt.Line2D(x_data[x:x+2], y_data[x:x+2], lw=5, linestyle='solid', color=color))
    return lines


# In[13]:


def draw_fig(x_values,data,errors,ax,colors):
    artists = energy_rank(x_values, data, color=colors)
    for artist in artists:
        ax.add_artist(artist)
    for x, y, error in zip(x_values, data, errors):
        error_bar = plt.Line2D([x, x], [y - error, y + error],linestyle='solid',alpha=0.8,color=colors,label='Expt.')
        ax.add_artist(error_bar)
        # Add data numbers above the data line
    ax.text(x_values[1], data[1] + error + 0.8, 'Expt. $\Delta F^{\ddag}$ = '+f'{data[1]:.1f}', ha='center',fontsize=15,color=colors)
    ax.text(x_values[2], data[2] + error - 1.9, 'Expt. $\Delta F{\degree}$ = '+f'{data[2]:.1f}', ha='center',fontsize=15,color=colors)


# In[14]:


fig = plt.figure(figsize=(14,7), dpi=150, facecolor='white')
grid = plt.GridSpec(25, 39, wspace=0.5, hspace=0.5)
ax0c  = fig.add_subplot(grid[0:1 ,  0:18])
ax0  = fig.add_subplot(grid[4:25 ,  0:18])
ax1  = fig.add_subplot(grid[0:25 , 21:39])

label1='$\mathregular{H_3}$'+'$\mathregular{O^+}$'
label2='$\mathregular{OH^-}$'

extent_opes = get_xy_min_max(os.path.join(folder_f+"fes-rew.dat"),cvnames)
ax0.set_xlim([extent_opes[0],extent_opes[1]])
ax0.set_ylim([extent_opes[2],extent_opes[3]])
ax0.contour(xi, yi, zi, colornum, colors='k', linewidths=0.5)
mlt=ax0.contourf(xi, yi, zi, colornum,cmap=cm)
ax0.set_xlabel(r"$s'_t$")
ax0.set_ylabel(r'$s_a$')
ax0.xaxis.set_major_locator(MultipleLocator(1))
ax0.xaxis.set_minor_locator(MultipleLocator(1/5))
ax0.yaxis.set_major_locator(MultipleLocator(0.4))
ax0.yaxis.set_minor_locator(MultipleLocator(0.4/4))
mycbar = fig.colorbar(mlt,cax=ax0c,orientation='horizontal',
                    ticks=[xx*2 for xx in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]],
                    label=r'$\Delta$'+r'$F$'+' (kcal/mol)')
mycbar.ax.set_xticklabels(["%d"%int(xx*2) for xx in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]]+['>30'])
ax0.text(-3, 1.88, 'M06-2X DPMD', color='black',fontsize=18)

ax1.plot(c05x, c05y, lw=2, c=colors[2],alpha=0.8,label='M06-2X DPMD')#+r"$ΔF$"+' = %2.1f kcal/mol'%deltaf[0])
ax1.fill_between(c05x, c05y-c05e, c05y+c05e,facecolor=colors[2],alpha = 0.4)
ax1.plot(sc05x, sc05y, lw=2, c=colors[-3],alpha=0.8,label='SCAN DPMD')#+r"$ΔF$"+' = %2.1f kcal/mol'%deltaf[1])
#ax1.fill_between(sc05x, sc05y-sc05e, sc05y+sc05e,facecolor=colors[-5],alpha = 0.4)
ax1.legend(loc='lower right',ncol=1,fontsize=16)
ax1.set_xlabel(r'$s_a$')
ax1.set_ylabel(r'$\Delta$'+r'$F$'+" (kcal/mol)")
ax1.set_ylim(-2.8,28)
ax1.set_xlim((-0.,2.0))
ax1.yaxis.set_major_locator(MultipleLocator(7))
ax1.yaxis.set_minor_locator(MultipleLocator(7/5))
ax1.xaxis.set_major_locator(MultipleLocator(0.4))
ax1.xaxis.set_minor_locator(MultipleLocator(0.4/4))

draw_fig([0.0,0.6,1.35],[0.0,23.8,21.4],[0,0,0],ax1,colors[0])

lax=[ax0,ax1]
lll=['a','b']
for i in range(2):
    if i == 0:
        lax[i].text(-0.11, 1.22, '%s'%lll[i], weight='bold', transform=lax[i].transAxes, fontsize=22,verticalalignment='top')
    else:
        lax[i].text(-0.14, 1.02, '%s'%lll[i], weight='bold', transform=lax[i].transAxes, fontsize=22,verticalalignment='top')

fig.savefig(os.path.join(save_path,"fes_autoionize_2.png"), dpi=300, bbox_inches='tight')


# In[ ]:




