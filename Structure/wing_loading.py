import numpy as np
import sys
sys.path.insert(0, '../Airframe/')
from masses_cg_positions import x_positions, z_positions, w_components
from mass_calculation import mass_iteration
sys.path.insert(0, '../Aerodynamics/')
from aerodynamic_parameters import *
from aero import drag, Propellers
sys.path.insert(0, '../PowerElectrical/')
import power
import matplotlib.pyplot as plt

#DEFINE PARAMETERS
def wing_load(static= False,show=True,grph=False):
    MTOW, Wing_w = mass_iteration(1630)
    cruiseT = power.ThrustCalculator(MTOW,aero_vals().vinfcr,1500 , 400000/aero_vals().vinfcr)
    cruiseL = Propellers(cruiseT.thrust, cruiseT.velocity,
                              cruiseT.rho, cruiseT.aero_vals.cl_cr, 0)
    L =(MTOW * 9.81*3.5)/(wing_vals().b - 2.4)
    W_w = (Wing_w*9.81)/(wing_vals().b - 2.4)
    T_cp = cruiseL.thrustCP / cruiseL.numberCP
    T_hlp = cruiseL.thrustHLP / cruiseL.numberHLP
    W_hlp = 52 *9.81 #LINK THESE LATER
    W_cp = 74 *9.81  #LINK THESE LATER
    c = 1.2 #link this
    D = ((drag(aero_vals().cd0,cruiseT.aero_vals.cl_cr,wing_vals().b,wing_vals().MAC,cruiseT.wing_vals.e,cruiseT.velocity,cruiseT.rho))/2)/(wing_vals().b/2)
    b = wing_vals().b - 2.4
    y = [0.3,0.9,1.5,2.1,3.2]
    if static:
        L = 0
        D = 0
        T_cp = 0
        T_hlp = 0
        
    #Z-upwards defined
    #X-forward defined
    #y-doesn't matter
    R_z = -(W_hlp *4 + W_cp + W_w*b/2 - L * b/2)
    R_x = -(T_hlp *4 + T_cp - D * b/2)
    R_y = 0.0
    
    M_x = -(W_hlp*y[0] + W_hlp * y[1] + W_hlp * y[2] + W_hlp * y[3] + W_cp * y[4] + W_w * b/2 * b/4 - L * b/2 * b/4 )
    M_z = -(T_hlp*y[0] + T_hlp * y[1] + T_hlp * y[2] + T_hlp * y[3] + T_cp * y[4] - D * b/2 * b/4)
    M_y = -((W_hlp*4 + W_cp) * c/2 - L*b/2 * (1/2 - 1/3)*c)
    
    if show:
        ys = np.linspace(0,3.2,num=3200)
        y_ind = []
        for i in range(len(y)):
            ind_lst = []
            for j in range(len(ys)):
                if ys[j]<y[i]:
                    ind = 0
                else:
                    ind = 1
                ind_lst.append(ind)
            y_ind.append(ind_lst)
        #x Moment Diagram
        mom_x = []
        for i in range(len(ys)):
            if i ==0:
                mom = (- W_hlp *max(0,ys[i]-y[0])) - W_hlp * max(0,ys[i]-y[1]) - R_z * ys[i] - W_hlp * max(0,ys[i] - y[2]) - W_hlp * max(0,ys[i]-y[3]) - L/2 *ys[i]**2 + W_w/2 * ys[i]**2
                mom_x.append(mom)
            else:
                mom = M_x -( W_hlp *max(0,ys[i]-y[0])) - W_hlp * max(0,ys[i]-y[1]) - R_z * ys[i] - W_hlp * max(0,ys[i] - y[2]) - W_hlp * max(0,ys[i]-y[3]) + L/2 *ys[i]**2 - W_w/2 * ys[i]**2
                mom_x.append(mom)
        #plt.subplot(421)
        #plt.title('Moment Diagram (y-z plane)')
        #plt.xlabel('y [m]')
        #plt.ylabel('Internal Moment [Nm]')
        #plt.plot(ys,mom_x)
        #Z Moment Diagram
        mom_z = []
        for i in range(len(ys)):
            if i == 0:
                mom = 0.0
                mom_z.append(mom)
            else:
                mom = M_z - T_hlp*max(0,ys[i]-y[0]) - T_hlp*max(0,ys[i]-y[1]) - T_hlp*max(0,ys[i]-y[2])-T_hlp*max(0,ys[i]-y[3]) - R_x * ys[i] + D/2 * ys[i]**2
                mom_z.append(mom)
        #plt.subplot(422)
        #plt.title('Moment Diagram (x-y plane)')
        #plt.xlabel('y [m]')
        #plt.ylabel('Internal Moment [Nm]')
        #plt.plot(ys,mom_z)
        
        #Z Shear Diagram
        shr_z = []
        for i in range(len(ys)):
            shr = - W_hlp * y_ind[0][i] - W_hlp * y_ind[1][i] - W_hlp * y_ind[2][i] - R_z + L * ys[i] - W_w * ys[i] 
            shr_z.append(shr)
        #plt.subplot(423)
        #plt.plot(ys,shr_z)
        #X Shear Diagram
        shr_x = []
        for i in range(len(ys)):
            shr =  - T_hlp*y_ind[0][i] - T_hlp * y_ind[1][i] - T_hlp * y_ind[2][i] - T_hlp * y_ind[3][i] - R_x + D * ys[i]
            shr_x.append(shr)
        shradd = shr_x[0] - R_x
        for i in range(len(shr_x)):
            shr_x[i] = shr_x[i]-shradd 
        #plt.subplot(424)
        #plt.plot(ys,shr_x)
        
        data =[ys,shr_z, shr_x , mom_x , mom_z]
        if grph:
             plt.subplot(421)
             plt.title('Moment Diagram (y-z plane)')
             plt.xlabel('y [m]')
             plt.ylabel('Internal Moment [Nm]')
             plt.plot(ys,mom_x)
             plt.subplot(422)
             plt.title('Moment Diagram (x-y plane)')
             plt.xlabel('y [m]')
             plt.ylabel('Internal Moment [Nm]')
             plt.plot(ys,mom_z)
             plt.subplot(423)
             plt.title('Shear Diagram (y-z plane)')
             plt.xlabel('y [m]')
             plt.ylabel('Internal Shear [N]')
             plt.plot(ys,shr_z)
             plt.subplot(424)
             plt.title('Shear Diagram (x-y plane)')
             plt.xlabel('y [m]')
             plt.ylabel('Internal Shear [N]')
             plt.plot(ys,shr_x)
             plt.show()
        return data , grph, R_x, M_z
    
    
def wing_deflec(data,grph,E,I_xx,I_zz):
    int_z_1=[]
    int_x_1=[]
    for i in range(len(data[3])-1):
        if i==0:
            sm_z = data[3][i] * (data[0][i+1]-data[0][i])
            sm_x = data[4][i] * (data[0][i+1]-data[0][i]) 
            int_z_1.append(sm_z)
            int_x_1.append(sm_x)
        else:
            sm_z = data[3][i] * (data[0][i+1]-data[0][i]) +int_z_1[-1]
            sm_x = data[4][i] * (data[0][i+1]-data[0][i]) +int_x_1[-1]
            int_z_1.append(sm_z)
            int_x_1.append(sm_x)
    int_z_1.append(int_z_1[-1])
    int_x_1.append(int_x_1[-1])
    #plt.subplot(425)
    #plt.plot(data[0],int_z_1)
    #plt.subplot(426)
    #plt.plot(data[0],int_x_1)
    int_z_2 = []
    int_x_2 = []
    for i in range(len(data[3])-1):
        if i==0:
            sm_z = int_z_1[i] * (data[0][i+1]-data[0][i])
            sm_x = int_x_1[i] * (data[0][i+1]-data[0][i]) 
            int_z_2.append(sm_z)
            int_x_2.append(sm_x)
        else:
            sm_z = int_z_1[i] * (data[0][i+1]-data[0][i]) +int_z_2[-1]
            sm_x = int_x_1[i] * (data[0][i+1]-data[0][i]) +int_x_2[-1]
            int_z_2.append(sm_z)
            int_x_2.append(sm_x)
            
    for i in range(len(int_z_2)):
        int_z_2[i] = int_z_2[i]/(E*I_zz)
        int_x_2[i] = -int_x_2[i]/(E*I_xx)
    int_z_2.append(int_z_2[-1])
    int_x_2.append(int_x_2[-1])
    #plt.subplot(427)
    #plt.plot(data[0],int_z_2)
    #plt.subplot(428)
    #plt.plot(data[0],int_x_2)
    if grph:
        plt.subplot(425)
        plt.plot(data[0],int_z_1)
        plt.subplot(426)
        plt.plot(data[0],int_x_1)
        plt.subplot(427)
        plt.plot(data[0],int_z_2)
        plt.subplot(428)
        plt.plot(data[0],int_x_2)
    v_z = max(int_z_2)
    v_x = max(int_x_2)
    return v_z , v_x    

a = wing_load(grph=True)
b = wing_deflec(a[0],a[1],71.7e9,1e-6,4.03e-5)

def inert_req(E,max_def,tol):
    a = wing_load()
    rnge = [0.0,1.0]
    err=99999
    while abs(err)>tol:
        mid = (rnge[0] + rnge[1] ) / 2
        defl = wing_deflec(a[0],a[1],E,6.5e-6,mid)
        err=defl[0]-max_def
        if err<0:
            rnge[1] = mid
        elif err>0:
            rnge[0] = mid
    return mid

moi = inert_req(71.7e9,0.04,1e-9)

#FINAL VALUE
b = wing_deflec(a[0],a[1],228e9,2.184e-4,6.739e-6)

print moi   
print a[2]  
print a[3]


