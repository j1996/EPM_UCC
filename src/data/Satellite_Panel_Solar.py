 # -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:26:53 2020

@author: ignacio.garciasanche
"""

"""
    Paneles Solares : definimos tanto los atributos (tanto parametros inmutables como variables) y los estados que poseen los paneles solares.

            Funcion Estado ' psolar() '        : input  = none 
                                                 output = descripcion de los paneles solares usados (tipo,masa,tension,intensidad)  

            Funcion Estado ' psolar_estado() ' : input  = none
                                                 output = estado del panel, es decir, si esta generando, o no, potencia
"""

#import numpy as np
#
#import Constants as cons


class Panel_Solar():
    
    """
        ATRIBUTOS
    """
    def __init__(self, name):
        """ Parametros de paneles solares """        
        self.nombre = name
        self.psolar_tipo = ""  # Descripcion del panel solar
        self.psolar_tension = 0.                                                             # Voltaje [V]
        self.psolar_intensidad = 0.                                                          # Intensidad [mA]
        self.psolar_eficiencia = 28.                                                         # Eficiencia [%]

        self.psolar_masa = 0.1                                                               # Masa del panel solar [kg]
        self.psolar_area = 0                                                          # Area del panel solar [cm2]
        
        self.psolar_rendimiento = 0.28                                                         # Rendimiento del panel en funcion de la incidencia solar [%]
        self.psolar_generando = False                                                        # Estado del panel

    
    
    """
        ESTADOS
    """
    
    def psolar(self):
        print(self.psolar_tipo,"\nMasa:",self.psolar_masa,"kg","\nTension:",self.psolar_tension,"V","  Intensidad:",self.psolar_intensidad,"mA")
    
    def psolar_estado(self):
        print("Panel solar",self.nombre,": ","Generando:",self.psolar_generando)

if __name__ == '__main__':
    [Panel_Solar('Estandar')]
