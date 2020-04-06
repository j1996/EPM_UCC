# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:33:51 2020

@author: ignacio.garciasanche
"""

import numpy as np

from Calculos_Orbitales import Constants as cons

"""
    Modulo del consumo de los diferentes Subsistemas. Servirá para analizar posibles escenarios "reales" de consumo de potencia y así dimensionar la generacion 
    (Paneles Solares) y el almacenamiento (Baterias) de energia.
    
                ' carga_trabajo ' :  se refiere a la carga de trabajo medida en tiempo [s] que realiza el subsistema durante un año.
"""

"""
    Subsistema de Actitud del Satelite  : ofrece su consumo mediante parametros y variables.
"""

class Sat_Actitud():        
    """
        DATOS DEL SATELITE
    """
    def __init__(self):
        self.Act_funcionando = False
        self.Act_consumo = 0
        self.Act_tension = 0
        self.Act_intensidad = 0
    
    """
        Consumo
    """   
    def consumo(self,carga_trabajo):
        pass

  
"""
    Subsistema de Comunicaciones del Satelite  : ofrece su consumo mediante parametros y variables.
"""

class Sat_Comunicaciones():        
    """
        DATOS DEL SATELITE
    """
    def __init__(self):
        self.Com_funcionando = False
        self.Com_consumo = 0
        self.Com_tension = 0
        self.Com_intensidad = 0
        
    """
        Consumo
    """   
    def consumo(self,carga_trabajo):
        pass


"""
    Subsistema Termico del Satelite  : ofrece su consumo mediante parametros y variables.
"""

class Sat_Termico():        
    """
        DATOS DEL SATELITE
    """
    def __init__(self):
        self.Term_funcionando = False
        self.Term_consumo = 0
        self.Term_tension = 0
        self.Term_intensidad = 0
        
    """
        Consumo
    """   
    def consumo(self,carga_trabajo):
        pass






