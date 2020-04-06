# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:45:36 2020

@author: ignacio.garciasanche
"""

"""
    Subsistema de Potencia del Satelite  : define atributos variables que serán los que vayan describiendo el estado del subsistema en cada instante t.

            Funcion Metodo ' ilumination(t) '    : input  = instante t [s]
                                                   output = potencia generada [W], asi como, cabio de estado del panel (generando / no generando)

            Funcion Metodo ' potencia(t) '       : input  = instante t [s] e instante anterior t0 que se asigna en la propia funcion [s]
                                                   output = none

            Funcion Estado ' potencia_estado() ' : input  = none 
                                                   output = descripcion del estado del sistema de potencia (carga de trabjo del sistema, estado de baterias y paneles olares)
"""

import numpy as np

from Calculos_Orbitales import Constants as cons

from Calculos_Orbitales.Satellite_Panel_Solar import *
from Calculos_Orbitales.Satellite_Bateria import *
from Calculos_Orbitales.Satellite_Sist_Pos import *
from Calculos_Orbitales.Astros import *

"""
    SATELITE
"""

class Sat_Potencia(Bateria,Sat_Position):  #Sat_Potencia(Panel_Solar,Bateria,Sat_position):      
    
    """
        ATRIBUTOS
    """
    def __init__(self,RAAN,w):
        
        """ Atributos de Panel_Solar y Baterias """
#        Panel_Solar.__init__(self,0)                   # En un primer momento se penso recibir herencia del modulo de paneles solares
        Bateria.__init__(self)
        Sat_Position.__init__(self,RAAN,w)
        
        """ Parametros de potencia """
        self.pot_necesaria = 1.                                                                            # Inicializacion de potencia requerida por el sat [W]
        self.pot_generada = 1.                                                                  # Inicializacion de potencia generada por las placas solares [W]
        self.pot_baterias = 1.                                        # Inicializacion de potencia [descargandose(-)/cargadandose(+)/sin uso(0)] de baterias [W]
        self.pot_suministrada = 1.                                                # Inicializacion de potencia suministrada entre paneles solares y baterias [W]
        
        self.estado = 0.                                                                     # Inicializacion del estado de la carga de trabajo del satelite [%]
        
        
        """ Definicion de los paneles solares """
        self.ps_Xp = Panel_Solar("Xp",250)                                        # Decalracion de los distintos paneles solares, introduciendo el area en [cm2]
        self.ps_Xn = Panel_Solar("Xn",250)                                        #    p : cara en en semieje positivo
        self.ps_Yp = Panel_Solar("Yp",50)                                         #    n : cara en el semieje negativo
        self.ps_Yn = Panel_Solar("Yn",0)                                          # 
        self.ps_Zp = Panel_Solar("Zp",250)                                        # 
        self.ps_Zn = Panel_Solar("Zn",250)                                        # 
    
    
    
    """
        METODOS
    """
    
    """ Generacion : Metodo que retorna la potencia generada en cada instante t por los paneles solares """
    def ilumination(self,t):
        """ Defino los Astros """
        Tierra = Earth()
        Sol = Sun()
        
        """ Defino la posicion de los astros """
        Sol.position(t)
        Tierra.position()

        """ Defino la posicion del satelite """
        self.sat_position(t)                                                                                   # Asigna la posicion del satelite a ' self.pos '
        
        """ Calculo la posicion relativa (angulo de incidencia, eclipse) """
        
        
        
        
        self.pot_generada = self.pot_generada
        
        if self.pot_generada > 0.:
            self.psolar_generando = True
        else:
            self.psolar_generando = False
        pass
    
    
    """ Gestion : Metodo que analiza la situacion de potencia en cada instante t """
    def potencia(self,t,Com_consumo,Act_consumo,Term_consumo):        
        
        if t == 0:
            t0 = 0                                                                                                # Inicializacion del instante anterior inicial
        
        """ Primero : distinguir estado de suministro de energia """
        if self.pot_generada > self.pot_necesaria:
            self.pot_baterias = (self.pot_generada-self.pot_necesaria)                                     # Potencia destinada a cargar las baterias (positiva)
            self.bat_descargando = False ; self.bat_cargando = True
        
        elif self.pot_generada < self.pot_necesaria:
            self.pot_baterias = (self.pot_generada-self.pot_necesaria)      # Potencia de las baterias descargandose destinada a cubrir pot_necesaria (negativa)
            self.bat_cargando = False ; self.bat_descargando = True
        
        else:
            self.pot_baterias = 0
            self.bat_cargando = False ; self.bat_descargando = False
        
        
        """ Segundo : calculo y analisis de la pot suministrad """
        self.pot_suministrada = self.pot_generada - self.pot_baterias                           # La potencia suministrada debe ser igual siempre a la necesaria
        
        if self.pot_suministrada<self.pot_necesaria:
            print("ERROR: El satelite no dispone de la energía necesaria")                                       # Error grave de diseño -> Alto nivel de ALARMA
            i=0
            while i<=5:
                print("ERROR  ERROR  ERROR  ERROR  ERROR  ERROR  ERROR ERROR  ERROR")
                i=i+1
            print("ERROR: El satelite no dispone de la energía necesaria")
        
        
        """ Tercero : carga o descarga de la batería """
        if self.bat_cargando == True:
            self.bateria_carga(t,t0)
        elif self.bat_descargando == True:
            self.bateria_descarga(t,t0)
        else:
            print("La Bateria no esta trabajando")
        
        if t > 0:
            t0 = t                                                                                # Definicion del instante anterior para la siguiente iteracion

        pass
        
    
    
    
    """
        ESTADOS
    """
    
    """ Estado del subsistema de potencia en lo referente a carga de trabajo """
    def potencia_estado(self):
        self.pot_estado=(1.-(self.pot_suministrada-self.pot_necesaria)/self.pot_suministrada)*100
        
        print("Subsistema de POTENCIA","\nLa carga de trabajo es:",self.pot_estado,"%")
        self.bateria_estado()
        print("PANELES SOLARES")
        self.ps_Xp.psolar_estado()
        self.ps_Xn.psolar_estado()
        self.ps_Yp.psolar_estado()
        self.ps_Yn.psolar_estado() 
        self.ps_Zp.psolar_estado() 
        self.ps_Zn.psolar_estado()  
        pass






