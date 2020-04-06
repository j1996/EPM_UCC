# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:11:05 2020

@author: ignacio.garciasanche
"""

import numpy as np

from Calculos_Orbitales import Constants as cons

"""
    Posicion del Satelite  : ofrece la posicion y la velocidad del satelite en un determinado tiempo t
            
            Funcion ' position(t) '              : input  = tiempo t [s]
                                                   output = vector posicion (x,y,z) con sistema de referncia Tierra [km]

            Funcion ' speed(t) '                 : input  = tiempo t [s]
                                                   output = vector velocidad (Vx,Vy,Vz) con sistema de referncia Tierra [km/s]

            Funcion Aux ' Anom_E(a,exc,tau,t) '  : input  = tiempo t [s] y parametros orbitales (a,e,tau)
                                                   output = Anomalia Excentrica
"""

class Sat_Position():
    """
        DATOS DEL SATELITE
    """
    def __init__(self,RAAN,w):       
        """ Parametros orbitales """
        self.a = 7278.14                                                                                                                    # Semieje Mayor [km] 
        self.e = 0   
        self.i = 90 ; self.i = self.i*np.pi/180                                                                                  # Inclinacion en radianes [rad]
        self.tau = 0                                                                                                         # Tiempo de paso por el perigeo [s]
    
        self.RAAN = RAAN                                                                                                                # RAAN en radianes [rad]
        self.w = w ; self.w = self.w*np.pi/180                                                                                         # Omega en radianes [rad]

        
    
    """
        Situación del Satelite
    """
    def sat_position(self,t):
        AnomE=Anom_E(self.a,self.e,self.tau,t)
        Anom_V=2*(np.arctan((np.sqrt((1+self.e)/(1-self.e))))*180/np.pi*(180/np.pi*np.tan(AnomE/2)))
        
        r_norm=self.a*(1-(self.e*(180/np.pi*np.cos(AnomE))))
        
        A=np.matrix([[180/np.pi*np.cos(self.RAAN),(-180/np.pi*np.sin(self.RAAN)),0],
            [180/np.pi*np.sin(self.RAAN),180/np.pi*np.cos(self.RAAN),0],
            [0,0,1]])
     
        B=np.matrix([[1,0,0],
             [0,180/np.pi*np.cos(self.i),(-180/np.pi*np.sin(self.i))],
             [0,180/np.pi*np.sin(self.i),180/np.pi*np.cos(self.i)]])
      
        C=np.matrix([[180/np.pi*np.cos(self.w),(-180/np.pi*np.sin(self.w)),0],
             [180/np.pi*np.sin(self.w),180/np.pi*np.cos(self.w),0],
             [0,0,1]])
             
        u_r=A*B*C*np.matrix([180/np.pi*np.cos(Anom_V),180/np.pi*np.sin(Anom_V),0]).reshape(3,1)
  
        r=r_norm*u_r
        
        self.pos=r.T
        return(self.pos)
        
    def sat_speed(self,t):
        AnomE=Anom_E(self.a,self.e,self.tau,t)
        Anom_V=2*(np.arctan((np.sqrt((1+self.e)/(1-self.e))))*180/np.pi*(180/np.pi*np.tan(AnomE/2)))
        
        r_norm=self.a*(1-(self.e*(180/np.pi*np.cos(AnomE))))
        v_norm=np.sqrt((2*cons.mu/r_norm)-(cons.mu/self.a))
  
        path=(np.arctan((self.e*np.sin(Anom_V)*180/np.pi)*180/np.pi)/(1+(self.e*180/np.pi*np.cos(Anom_V))))
  
        A=np.matrix([[180/np.pi*np.cos(self.RAAN),(-180/np.pi*np.sin(self.RAAN)),0],
            [180/np.pi*np.sin(self.RAAN),180/np.pi*np.cos(self.RAAN),0],
            [0,0,1]])
     
        B=np.matrix([[1,0,0],
             [0,180/np.pi*np.cos(self.i),(-180/np.pi*np.sin(self.i))],
             [0,180/np.pi*np.sin(self.i),180/np.pi*np.cos(self.i)]])
      
        C=np.matrix([[180/np.pi*np.cos(self.w),(-180/np.pi*np.sin(self.w)),0],
             [180/np.pi*np.sin(self.w),180/np.pi*np.cos(self.w),0],
             [0,0,1]])
         
        D=np.matrix([[180/np.pi*np.cos(Anom_V),(-180/np.pi*np.sin(Anom_V)),0],
             [180/np.pi*np.sin(Anom_V),180/np.pi*np.cos(Anom_V),0],
             [0,0,1]])
     
        u_v=A*B*C*D*np.matrix([180/np.pi*np.sin(path),180/np.pi*np.cos(path),0]).reshape(3,1)
  
        v=v_norm*u_v
        
        self.spd=v.T
        return(self.spd)
        
        
        
    
"""
    Funciones
"""
def Anom_E(a,exc,tau,t):
    
    T=2*np.pi*np.sqrt((a**3)/cons.mu)
    
    while t<tau or t>(T+tau):
        if t<tau:
            t=t+T
        elif t>(T+t):
            t=t-T
    
    E_0=(360*(t-tau))/T
    prec=0.000001
    
    E_1=(E_0*np.pi)/180
    F=E_1-(exc*np.sin(E_1))-((np.sqrt(cons.mu/(a**3)))*(t-tau))
  
    while F<(-prec) or F>prec:
        E_1=E_1-((E_1-(exc*np.sin(E_1))-((np.sqrt(cons.mu/(a**3)))*(t-tau)))/(1-(exc*np.cos(E_1))))
        F=E_1-(exc*np.sin(E_1))-((np.sqrt(cons.mu/(a**3)))*(t-tau))
  
    Anom_E=(E_1*180)/np.pi
    
    return(Anom_E)
