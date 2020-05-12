# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:30:07 2020

@author: ignacio.garciasanche
"""
"""
    Baterias : definimos los Atributos (tanto los parametros inmutables como las variables) y los metodos y estados que las baterias poseen.

            Funcion Metodo ' bateria_carga(t,t0) '    : input  = instante t [s] e instante anterior t0 [s]
                                                        output = none
                                                        ' realiza la carga de la bateria, tenindo encuenta tiempo y potencia de carga y degradacion de la bateria ' 

            Funcion Metodo ' bateria_descarga(t,t0) ' : input  = instante t [s] e instante anterior t0 [s]
                                                        output = none
                                                        ' realiza la descarga de la bateria, tenindo encuenta tiempo y potencia de descarga '

            Funcion Estado ' bateria() '              : input  = none 
                                                        output = descripcion de las baterias usados (tipo,masa,volumen,tension,intensidad,capacidad)  

            Funcion Estado ' bateria_estado() '       : input  = none
                                                        output = estado de la bateria, es decir, nivel de carga, si esta cargando o descargando, salud de la bateria
"""

#import numpy as np
#
#import Constants as cons


class Bateria():

    """
        ATRIBUTOS
    """

    def __init__(self):
        """ Parametros de baterias """
        self.bat_tipo = ""  # Descripcion de la batería
        # Capacidad [mAh]
        self.bat_capacidad = 2200
        # Voltaje [V]
        self.bat_tension = 0.
        # Intensidad [mA]
        self.bat_intensidad = 0.

        # Masa de las baterias [kg]
        self.bat_masa = 0.
        # Volumen de las baterias [cm3]
        self.bat_volumen = 0.

        # Nivel de batería [%]
        self.bat_nivelcarga = 50.
        # Estado de la bateria ¿cargando?
        self.bat_cargando = False
        # Estado de la bateria ¿descargando?
        self.bat_descargando = False
        # Rendimiento [tanto por uno]
        self.bat_rendimiento = 1.
        # Ciclos de carga/descarga
        self.bat_ciclos = 0
        self.bat_cicloestado = 0


    """
        METODOS
    """

    def bateria_carga(self, t, t0):
        """ Cantidad de capacidad cargada """
        carg = (0)/self.bat_capacidad * \
            100             # Donde el 0 debemos poner la ecuacion de la carga

        """ Nivel de bateria una vez cargada """
        self.bat_nivelcarga = (self.bat_nivelcarga + carg)*self.bat_rendimiento

        """ Degradacion de la bateria segun el numero de ciclos """                    # Aqui hacemos un analisis de la degradacion (rendimiento) de la bateria
        self.bat_cicloestado = self.bat_cicloestado + \
            carg  # segun van sucediendose los ciclos de carga
        # Un ciclo se alcanza cuando las repetidas cargas acumulan el 100% de la
        if self.bat_cicloestado >= (100*self.bat_rendimiento):
            # capacidad de la bateria, y eso es lo que hacemos aqui. Luego, variamos
            self.bat_cicloestado = self.bat_cicloestado - 100*self.bat_rendimiento
            # el rendimiento de la bateria  siguiendo el criterio de que cada 100
            self.bat_ciclos = self.bat_ciclos + 1
        # ciclos, el rendimiento cae un 5%.
        self.bat_rendimiento = self.bat_rendimiento - \
            (0.05/100)*self.bat_ciclos

        if self.bat_nivelcarga >= (100*self.bat_rendimiento):
            self.bat_nivelcarga = 100*self.bat_rendimiento
            print("Bateria cargada")

        pass

    def bateria_descarga(self, t, t0):

        # Donde el 0 debemos poner la ecuacion de la descarga
        descarg = (0)/self.bat_capacidad*100

        self.bat_nivelcarga = self.bat_nivelcarga - descarg

        if self.bat_nivelcarga <= 0:
            descarg_real = descarg + self.bat_nivelcarga
            self.bat_nivelcarga = 0
            print("Bateria descargada")
            print("La bateria no cubre lo que el Satelite necesita")

        pass


    """
        ESTADOS
    """

    def bateria(self):
        print(self.bat_tipo, "\nMasa:", self.bat_masa, "kg", "  Volumen:", self.bat_volumen, "cm3", "\nTension:",
              self.bat_tension, "V", "  Intensidad:", self.bat_intensidad, "mA", "  Capacidad:", self.bat_capacidad, "mAh")

    def bateria_estado(self):
        print("BATERIA")
        print("Nivel de carga:", self.bat_nivelcarga, "%", "   Salud de bateria:", self.bat_rendimiento *
              100, "%", "\n   Cargando:", self.bat_cargando, "   Descargando:", self.bat_descargando)
