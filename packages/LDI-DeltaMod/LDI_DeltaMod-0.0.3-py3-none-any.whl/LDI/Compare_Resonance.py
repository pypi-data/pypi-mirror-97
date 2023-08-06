# -*- coding: utf-8 -*-
"""
Lumerical Data Handling
Created on Fri Feb  7 12:14:09 2020
@author: Vidar Flodgren
Github: https://github.com/DeltaMod
"""

#use this to set current directory without running code: os.chdir(os.path.dirname(sys.argv[0]))
import os
import sys
import time
import h5py
import hdf5storage
import matplotlib
import tkinter as tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d #If you want to be able to use projection="3D", then you need this:
import scipy
import numpy as np
from scipy import integrate
from scipy import interpolate
import json
from collections import Counter
import natsort
from scipy.constants import e


from LDI import (Get_FileList,MatLoader,CUV,jsonhandler,cprint,PathSet,AbsPowIntegrator,Rel_Checker,DataDir,Init_LDI,Prog_Dict_Importer,ezplot,MergeList)

## for Palatino and other serif fonts use:
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["CMU"],
    "font.size": 14,
    "axes.grid.which":'both', 
    "grid.linestyle":'dashed',
    "grid.linewidth":0.6,
    "xtick.minor.visible":True,
    "ytick.minor.visible":True,
    "figure.figsize":[16/2,9/1.5],
    
})

plt.rcParams['figure.dpi']         = 100
plt.rcParams['axes.grid']          = True
plt.rcParams['axes.axisbelow']     = True
plt.rcParams['figure.autolayout']  = True 


        
    
    
#Load user settings from a file using CUV
UV = CUV(act = 'init')
UV['txt_import'] = True
#%%
#We get a list of all files in dicts matching the number of extensions we are searching for.
DIR,DIRPT = Rel_Checker(DataDir(act='load')['9'])
#DIR1 = 'C:\\Users\\vidar\\Desktop\\MD2_Contacts-24-08-2020'; DIRPT = 'abs'
#DIR1 = "Z:\\HDD-PC\\Work\\University Work\\Physics\\PhD Local Storage\\Data\\MD2_NoContacts-24-08-2020"; DIRPT = 'abs'

DList,NList = Get_FileList(DIR,pathtype=DIRPT, ext = (('mat','txt')),sorting='numeric')

#%%
#We probably only want to only load one matfile at a time, because otherwise we're going to quickly run out of memory!
# Dproc = {'AbsPow':[],'enw_x':[],'enw_y':[],'enw_z':[],'s_d':[],'enw_rot':[],'rel_rot':[],'current':[],'roundingradius dir':[],'GCx_span':[]}
P_out = 8.4e-15

"""
0.1 nA    1 nA     10 nA
0.02 fW     8.4 fW     0.5 pW
"""

"""
New method of importing data that does not require manual assignment of the keys in Dproc!
"""
#Scattering Peak Dictionary
SPD  = {'Abs':[],'Scat':[],'xdim':[],'ydim':[],'zdim':[]}


PlotParam = {'DFT Plot':True,'Cross Section':False,'Save Figure':False,'E_C Plot':True}
#Only use for small amounts of data!
E_C = []
figs = []
if UV['Debug'] == False:
    Dproc = {} # Create an empty dictionary to store your data in 
    for file in DList['.mat']:
        MDat,MFi = MatLoader(file,txt=UV['txt_import'])

        if 'lambda' not in MDat.keys():
            MDat['lambda'] = MatLoader("Z:\\HDD-PC\\Work\\University Work\\Physics\\PhD Local Storage\\Data\\Yagi-Uda\\DirectorResonance-18-02-2021\\WAVELENGTH.mat")[0]['lambda']
        
        """
        This was specific to plotting only from 1/3 monitors for the same data series
        if "_b." in MDat['matname']:    
            fig4 = ezplot(fid=4)
            fig4.DFT_Intensity_Plot(MDat['xgrid'],MDat['ygrid'],np.log10(MDat['Eabs_adj']),1e-6)
            colm = plt.cm.get_cmap("jet",1000)
            sm   = plt.cm.ScalarMappable(cmap=colm)
            plt.colorbar(sm,boundaries=np.linspace(0,1000,1000))
        """

        
        if PlotParam['DFT Plot'] == True:    
            try:
                MDat['Eabs_adj'] = MDat['Eabs']#/(np.min(MDat['Eabs'])+0.000000001) - 1
                E_C.append( {'Eabs':MDat['Eabs_adj'],'xgrid':MDat['xgrid'],'ygrid':MDat['ygrid'],'matfilepath':MDat['matfilepath'],'matname':MDat['matname']} )
                
                ## Old Filtering Options 
                #MDat['Eabs_adj'] = MDat['Eabs_adj']/np.max(MDat['Eabs_adj'])
                
                #for i in range(MDat['Eabs_adj'].shape[0]):
                #    for j in range(MDat['Eabs_adj'].shape[1]):
                #        if MDat['Eabs_adj'][i,j] >= 0.5*np.max(MDat['Eabs_adj']):
                #            MDat['Eabs_adj'][i,j] = 0.1*MDat['Eabs_adj'][i,j]
                
                if PlotParam['E_C Plot'] == False:
                    figs.append(ezplot())
                    fig = figs[-1]
                    
                    fig.DFT_Intensity_Plot(MDat['xgrid'],MDat['ygrid'],np.log10(MDat['Eabs_adj']),1e-6)
                    colm = plt.cm.get_cmap("jet",100000)
                    sm   = plt.cm.ScalarMappable(cmap=colm)
                    plt.colorbar(sm,boundaries=np.linspace(0,100000,100000))
                    
                    fig.ax[0].set_title("$\_$".join(MDat['matname'].split('_')),fontsize=11)
                    mxgrid = MatLoader(DList['.mat'][len(DList['.mat'])-3],txt=UV['txt_import'])[0]['xgrid']
                    mygrid = MatLoader(DList['.mat'][len(DList['.mat'])-3],txt=UV['txt_import'])[0]['ygrid']
                    fig.ax[0].set_xlim(min(mxgrid)*1e-6, max(mxgrid)*1e-6)
                    fig.ax[0].set_ylim(min(mygrid)*1e-6, max(mygrid)*1e-6)
                    if PlotParam['Save Figure'] == True:
                        fig.fig.savefig(MDat['matfilepath'].split('.')[0]+'_FI.png',dpi=250)
            except:
                None 
        if PlotParam['E_C Plot'] == False:
            if PlotParam['Cross Section'] == True:
                try:
                    SPD = Prog_Dict_Importer(SPD,{'Abs':np.max(MDat['Qabs']),'Scat':np.max(MDat['Qscat']),
                                                  'xdim':MDat['x_span_dir'],'ydim':MDat['y_span_dir'],'zdim':MDat['z_span_dir']})
                except:
                    None
                try:
    
                    fig5 = ezplot(fid=5)
                    fig5.ax[0].plot(MDat['lambda'],MDat['Qabs'],'b',label='absorption cs')
                    fig5.ax[0].plot(MDat['lambda'],MDat['Qscat'],'r',label='Scattering cs')
                    fig5.ax[0].set_xlabel('Wavelength [m]')
                    fig5.ax[0].set_ylabel('Mie Efficiency')
                    fig5.ax[0].set_title("$\_$".join(MDat['matname'].split('_')),fontsize=11)
                    fig5.ax[0].set_ylim(0,100)
                    fig5.ax[0].annotate(s='[dx,dy,dz] = \n'+'['+str(float('%.3g'%MDat['x_span_dir']))+','+str(float('%.3g'%MDat['y_span_dir']))+','+str(float('%.3g'%MDat['z_span_dir']))+']',xy=(0.125,0.85),xycoords='figure fraction')
                    fig5.ax[0].legend()
                    if PlotParam['Save Figure'] == True:
                        fig5.fig.savefig(MDat['matfilepath'].split('.')[0]+'_CS.png',dpi=250)
                except:
                    None        
                

        try:
            
            #First, add additional variables that need specific calculation manually into MDat (so Prog_Dict_Importer can grab them)
            if UV['txt_import'] == True:
                if "ENW_x" and "ENW_y" and "ENW_z" in MDat.keys():
                    anw_l = np.array([0,0,MDat['ENW_z']])
                    enw_l = np.array([MDat['ENW_x'],MDat['ENW_y'],MDat['ENW_z']])
                    squared_dist = np.sum((anw_l-enw_l)**2, axis=0)
                
                if "ENW_z_rot" in MDat.keys():
                    enw_rot = MDat['ENW_z_rot'] 
                
                
                    if MDat['ENW_y'] == 0:
                        atdeg =  0
                    else:
                        atdeg = np.degrees(np.arctan(abs(MDat['ENW_x']/MDat['ENW_y']))) 
                
                    rel_rot = enw_rot + atdeg
                    
                    if rel_rot>180:
                        rel_rot = atdeg - (180 - enw_rot)  
                    MDat['rel_rot'] = rel_rot
                    
                    MDat['s_d'] = np.sqrt(squared_dist)
            
            #Then do calculations on the longer data sets and store only the specific single data needed in MDat
            if 'Pabs' in MDat.keys():
                MDat['P_abs'] = np.reshape(MDat['Pabs'],[MDat['lambda'].shape[0],MDat['z'].shape[0],MDat['y'].shape[0],MDat['x'].shape[0]])
                cprint(['Now processing file: ',str(file)],mt='curio')
            if "Pabs_total" in MDat.keys():
                MDat['P_tot']  = AbsPowIntegrator(MDat['P_abs'],MDat['x'],MDat['y'],MDat['z'],MDat['lambda'])
                MDat['AbsPow'] = max(MDat['P_tot'])
        except:
            pass
        try:
            MDat['Pabs'] #this line is used to make sure that the transfer box results do not get placed into the same Dproc. In the future, Dproc will be set up to separate data based on what it thinks it is!
            #Use Prog_Dict_Importer to append remainder data that has a length smaller than ml=int *default 1 to Dproc
            Dproc = Prog_Dict_Importer(Dproc,MDat)
        
        except:
            pass
    
try:
    mxgrid = [np.min([min(E_C[i]['xgrid']) for i in range(len(E_C))]),np.max([max(E_C[i]['xgrid']) for i in range(len(E_C))])]
    mygrid = [np.min([min(E_C[i]['ygrid']) for i in range(len(E_C))]),np.max([max(E_C[i]['ygrid']) for i in range(len(E_C))])]
    plt.close('all')
    for i in range(len(E_C)):
        if PlotParam['DFT Plot'] == True and "DFT_b" in E_C[i]['matname']:    
                try:
                    
                    ## Old Filtering Options 
                    #MDat['Eabs_adj'] = MDat['Eabs_adj']/np.max(MDat['Eabs_adj'])
                    
                    #for i in range(MDat['Eabs_adj'].shape[0]):
                    #    for j in range(MDat['Eabs_adj'].shape[1]):
                    #        if MDat['Eabs_adj'][i,j] >= 0.5*np.max(MDat['Eabs_adj']):
                    #            MDat['Eabs_adj'][i,j] = 0.1*MDat['Eabs_adj'][i,j]
                    
                    
                    figs.append(ezplot())
                    fig = figs[-1]
                    
                    Eabs = np.log10(E_C[i]['Eabs'])
                    minmaxEabs = [np.log10(min([np.min(E_C[i]['Eabs']) for i in range(len(E_C))])),np.log10(max([np.max(E_C[i]['Eabs']) for i in range(len(E_C))]))]
                    #Eabs = E_C[i]['Eabs']
                    #minmaxEabs = [min([np.min(E_C[i]['Eabs'] for i in range(len(E_C))])),max([np.max(E_C[i]['Eabs'] for i in range(len(E_C))]))]
                    fig.DFT_Intensity_Plot(E_C[i]['xgrid'],E_C[i]['ygrid'],Eabs,1,vmin=minmaxEabs[0],vmax=minmaxEabs[1])
                    #colm = plt.cm.get_cmap("jet",maxEabs)
                    #sm   = plt.cm.ScalarMappable(cmap=colm)
                    #plt.colorbar(sm,boundaries=np.linspace(0,maxEabs,1000))
                    fig.fig.colorbar(fig.mappable[0], ax=fig.ax[0])
                    
                    fig.ax[0].set_title("$\_$".join(E_C[i]['matname'].split('_')),fontsize=11)
                    fig.ax[0].set_xlim(min(mxgrid), max(mxgrid))
                    fig.ax[0].set_ylim(min(mygrid), max(mygrid))
                    if PlotParam['Save Figure'] == True:
                        fig.fig.savefig(E_C[i]['matfilepath'].split('.')[0]+'_FI.png',dpi=250)
                except:
                    None 
            
        if PlotParam['Cross Section'] == True:
            try:
                SPD = Prog_Dict_Importer(SPD,{'Abs':np.max(MDat['Qabs']),'Scat':np.max(MDat['Qscat']),
                                              'xdim':MDat['x_span_dir'],'ydim':MDat['y_span_dir'],'zdim':MDat['z_span_dir']})
            except:
                None
            try:

                fig5 = ezplot(fid=5)
                fig5.ax[0].plot(MDat['lambda'],MDat['Qabs'],'b',label='absorption cs')
                fig5.ax[0].plot(MDat['lambda'],MDat['Qscat'],'r',label='Scattering cs')
                fig5.ax[0].set_xlabel('Wavelength [m]')
                fig5.ax[0].set_ylabel('Mie Efficiency')
                fig5.ax[0].set_title("$\_$".join(MDat['matname'].split('_')),fontsize=11)
                fig5.ax[0].set_ylim(0,100)
                fig5.ax[0].annotate(s='[dx,dy,dz] = \n'+'['+str(float('%.3g'%MDat['x_span_dir']))+','+str(float('%.3g'%MDat['y_span_dir']))+','+str(float('%.3g'%MDat['z_span_dir']))+']',xy=(0.125,0.85),xycoords='figure fraction')
                fig5.ax[0].legend()
                if PlotParam['Save Figure'] == True:
                    fig5.fig.savefig(MDat['matfilepath'].split('.')[0]+'_CS.png',dpi=250)
            except:
                None            
except:
    None
    
CUV(act = 'session',data=UV) #Saves user settings after each complete run!
#%%
"""
comp = [
7e-07, 0.00377263,
6.89447e-07, 0.00414069,
6.79208e-07, 0.00454842,
6.69268e-07, 0.00500499,
6.59615e-07, 0.00552264,
6.50237e-07, 0.00611169,
6.41121e-07, 0.00677529,
6.32258e-07, 0.00750842,
6.23636e-07, 0.00830372,
6.15247e-07, 0.00916187,
6.0708e-07, 0.0101,
5.99127e-07, 0.0111512,
5.91379e-07, 0.0123539,
5.8383e-07, 0.0137344,
5.76471e-07, 0.0152941,
5.69295e-07, 0.0170086,
5.62295e-07, 0.0188412,
5.55466e-07, 0.0207647,
5.488e-07, 0.0227782,
5.42292e-07, 0.0249087,
5.35938e-07, 0.0271938,
5.2973e-07, 0.0296524,
5.23664e-07, 0.0322573,
5.17736e-07, 0.0349238,
5.1194e-07, 0.0375188,
5.06273e-07, 0.0398887,
5.0073e-07, 0.0418913,
4.95307e-07, 0.0434199,
4.9e-07, 0.0444096,
4.84806e-07, 0.0448272,
4.7972e-07, 0.0446535,
4.7474e-07, 0.0438686,
4.69863e-07, 0.0424506,
4.65085e-07, 0.0403883,
4.60403e-07, 0.0377021,
4.55814e-07, 0.0344635,
4.51316e-07, 0.0308022,
4.46906e-07, 0.0268972,
4.42581e-07, 0.0229533,
4.38339e-07, 0.0191696,
4.34177e-07, 0.0157105,
4.30094e-07, 0.0126855,
4.26087e-07, 0.0101426,
4.22154e-07, 0.0080744,
4.18293e-07, 0.00643309,
4.14502e-07, 0.00514865,
4.10778e-07, 0.00414585,
4.07122e-07, 0.00335692,
4.03529e-07, 0.00272837,
4e-07, 0.00222265]
lambda2 = [comp[2*m] for m in range(int(len(comp)/2))]
int2 = [comp[2*m+1] for m in range(int(len(comp)/2))]
plt.plot(lambda2,int2)
plt.legend(['python interpolation','lumerical integration'])
plt.xlabel(r'$\lambda$ [m]')
plt.ylabel(r'$\frac{P_abs}{P_tot}$')
plt.grid(True)
"""


#%%
"""
The commented text here is old code - I'm actively working on renewing it to be more self-expandable.'

Mat = []
for i in DList['.mat']:
    Matfile = hdf5storage.loadmat(i)
    Matfile['name'] = i.split("\\")[-1]
    Mat.append(Matfile)
    
fid = 1    
Xdim,Ydim = Mat[fid]['Ex'][:,:,0,0].shape
def MatLoader(fid,MATF):
    x  = MATF[fid]['x'] #xaxis
    y  = MATF[fid]['y'] #yaxis
    z  = MATF[fid]['z'] #zaxis
    f  = MATF[fid]['f'] #frequency of the light probed
    if 'Px' in MATF[fid].keys():
        Px = MATF[fid]['Px']
        Py = MATF[fid]['Py']
        Pz = MATF[fid]['Pz']
        fn = 0
        mod = 1e-08
    
        Pv = {'x':[],'y':[],'z':[],'xc':[],'yc':[],'zc':[],'Px':[],'Py':[],'Pz':[],'L':[],'norm':[],'f':[]}
        Pv['x'] = x
        Pv['y'] = y
        Pv['z'] = z
        Pv['f'] = f
        for xn in range(len(x)):
            for yn in range(len(y)):
                for zn in range(len(z)):
                    Pv['Px'].append(np.real(MATF[fid]['Px'][xn,yn,zn,fn]))
                    Pv['Py'].append(np.real(MATF[fid]['Py'][xn,yn,zn,fn]))
                    Pv['Pz'].append(np.real(MATF[fid]['Pz'][xn,yn,zn,fn]))
                    Pv['xc'].append(x[xn])
                    Pv['yc'].append(y[yn])
                    Pv['zc'].append(y[zn])
                    Pv['L'].append( np.sqrt(Pv['Px'][-1]**2+Pv['Py'][-1]**2+Pv['Pz'][-1]**2))
                    Pv['norm'].append(mod/(Pv['L'][-1]))
        Pv['pPx'] = Px
        Pv['pPy'] = Py
        Pv['pPz'] = Pz
    return(Pv)

P_in  = MatLoader(4,Mat)
P_out = MatLoader(5,Mat)

def QuivPlot(figID,Pwr,ADD,SubSmple):
    fig = plt.figure(figID)
    if ADD == False:
        fig.clf()           # This clears the old figure
        ax = fig.add_subplot(projection='3d',proj_type='persp') # Makes a graph that covers a 2x2 size and has 3D projection
        
    cmap = plt.get_cmap('jet')
    #3D plot
    for name in Pwr.keys():
        Pwr[name] = np.asarray(Pwr[name])
    for n in range(0,len(Pwr['xc']),SubSmple):
        ax.quiver(Pwr['xc'][n],Pwr['yc'][n],Pwr['zc'][n],Pwr['norm'][n]*Pwr['Px'][n],Pwr['norm'][n]*Pwr['Py'][n],Pwr['norm'][n]*Pwr['Pz'][n],color=cmap(Pwr['L'][n]/np.max(Pwr['L'])))
    
QuivPlot(1,P_in,False,1)
QuivPlot(2,P_out,False,1)







def TotalPow(self):
    self['P_xp'] = [np.sum(np.real(self['pPx'][x,:,:,:])) for x in range(len(self['x'])) ]
  
    self['P_yp'] = [np.sum(np.real(self['pPy'][:,y,:,:])) for y in range(len(self['y'])) ]

    self['P_zp'] = [np.sum(np.real(self['pPz'][:,:,z,:])) for z in range(len(self['z'])) ]
TotalPow(P_in)
TotalPow(P_out)

#Surface Plots
#%%
fig = plt.figure(4)
fig.clf()           # This clears the old figure
ax = fig.add_subplot(projection='3d') # Makes a graph that covers a 2x2 size and has 3D projection
plt.ion()

Pow_l = []

for lambd in range(len(P_out['f'])):
    tempsum = 0
    for x in [0,-1]:
        A = sum(sum(np.real(P_out['pPx'][x,:,:,lambd])))
        B = sum(sum(np.real(P_out['pPy'][:,x,:,lambd])))
        C = sum(sum(np.real(P_out['pPz'][:,:,x,lambd])))
        tempsum = tempsum + abs(A)+abs(B)+abs(C)  
    Pow_l.append(tempsum)
# for x in [0,-1]:
#     for lambd in range(len(P_out['f'])):
        
        # Z,Y = np.meshgrid(P_out['z'],P_out['y'])
        # Pxsurf = P_out['pPx'][x,:,:,lambd]
        # ax.plot_surface(Y,Z,np.real(Pxsurf))

"""
 
"""
The data format used for all monitors has the following principle:
    Mat[file ID]['key'][xaxis,yaxis,zaxis,lambda]
If you want to slice through the x axis, showing the real valued intensity plotted in y/z, then you use:
for fn in range(len(Mat[fid]['f'])):
    for xn in range(len(x)):
        

im = plt.imshow(np.real(Mat[fid]['Py'][:,0,:,0]),cmap='jet')
for fn in range(len(Mat[fid]['f'])):
    for zn in range(len(z)):
        im.set_data(np.real(Mat[fid]['Pz'][:,:,zn,fn]))
        plt.draw()
        plt.pause(0.2)
        



""" 
    


