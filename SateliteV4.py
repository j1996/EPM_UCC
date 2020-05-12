from astropy.time import Time, TimeDelta 
from astropy import units as u
import numpy as np
import trimesh #permite la creacion de un mallado y su interaccion con un rayo 
import pandas as pd
from src.data.SatelitteSolarPowerSystemV4 import SatelitteSolarPowerSystem
from src.data.SatelitteActitud import SatelitteActitud
from src.data.OrbitasV4 import *
from tqdm import tqdm #Para la barra de progreso

#Crea un ID para cada simulacion de manera aleatoria 

simulacion = random_generator() 

#Se determina la orbita del satelite de manera clasica

a = 7278 * u.km             # Semieje mayor de la orbita en [km]
ecc = 0 * u.one             # Excentricida de la orbita
inc = 90 * u.deg            # Inclinacion de la orbita en [º]
raan =  0* u.deg            # RAAN de la orbita en [º]
argp_ini = 0.5 * u.deg      # Argumento  del perihelio [º]
nu = 0 * u.deg              # Anomalia verdadera [º]

# Tiempo de inicio de la simulacion

time = Time("2020-01-01 12:00:00", scale="utc") 

# Direcion donde se encuentra el modelo tiene que estar dentro de la carpeta del proyecto

direccion = 'models/12U_2Despegables.stl'    

#Estos son los siguientes modelos creados en la carpeta models
#   1U.stl
#   3U_1Despegables.stl
#   3U_4Despegables.stl
#   12U_2Despegables.stl
# Se crea una clase que es el sistema de actitud
# El eje de spin es el cual va a estar rotando en ejes LVLH
# Para ver como estan declarados: https://ai-solutions.com/_freeflyeruniversityguide/attitude_reference_frames.htm
# el parametro Control es si hay control o no sobre actitud 
# Para mas informacion revisar la documentacion en SatelitteActitud

actitud = SatelitteActitud(eje_de_spin=[1, 0, 0], control=True)

# Se crea la clase SatelitteSolarPowerSystem que es la mas importante de todo el programa 

EPM = SatelitteSolarPowerSystem(
    direccion, actitud, Despegables_orientables=True)

# En la mayoria de casos los ejes de la orbita y los de la figura no son correctos 
# por lo que se necesita el mirar como tiene que ser esta transformacion 
# Hay que recordar que:
#   X = Vector posicion de la orbita
#   Y = Vector velocidad de la orbita (mas menos ver el enlace en LVLH)
#   Z = Vector normal al plano de la orbita RxV

#EPM.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0], [0, 0, 0]))

Num_dias=365    # Numero de dias a propagar/obtener resultados

for k in tqdm(np.arange(0, Num_dias)):

    time_ini = time+TimeDelta(1*u.day)*k # Asi se pasa de un dia a otro para cambiar de fecha

    # Se crean los Nombres para pandas.DataFrame para que todo este bonito al sacar resultados

    iter = pd.MultiIndex.from_arrays(
        [[time_ini.iso[0
        :10]]*len(EPM.name), EPM.name])   

    iter2 = pd.MultiIndex.from_arrays([[time_ini.iso[0:10]]*(len(EPM.Caras_Despegables)+1), [
                                      "Spin Axis"]+[EPM.name[i] for i in EPM.Caras_Despegables]])

    # Esta la funcion principal que permite la propagacion del satelite Vease OrbitasV4
    # Tambien existen:
    #       propagate_orbit(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1)
    #       propagate_fast_one_orbit(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1)
    #       propagate_orbit2(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1)

    W, Area_potencia, Ang, Angulo_giro = propagate_orbit(
        a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, 100, 1)

    # A partir de aqui lo unico que hace es sacar los valores bonitos 
    # Se guardan los datos en la carpeta "data"
    
    if k == 0:

        Wpot = pd.DataFrame(W, columns=iter)
        pot = np.matrix(W).sum(axis=0) / len(W)
        potOrb = pd.DataFrame(pot, columns=EPM.name,
                              index=[time_ini.iso[0:10]])
        Area_pot = pd.DataFrame(Area_potencia, columns=iter)
        Ang_pot = pd.DataFrame(Ang, columns=iter)
        Ang_giro = pd.DataFrame(Angulo_giro, columns=iter2)

    else:

        Wpot2 = pd.DataFrame(W, columns=iter)
        Area_pot2 = pd.DataFrame(Area_potencia, columns=iter)
        Ang_pot2 = pd.DataFrame(Ang, columns=iter)
        Ang_giro2 = pd.DataFrame(Angulo_giro, columns=iter2)
        pot = np.matrix(W).sum(axis=0) / len(W)
        potOrb2 = pd.DataFrame(pot, columns=EPM.name,
                               index=[time_ini.iso[0:10]])
        Wpot = pd.concat([Wpot, Wpot2], axis=1)
        Area_pot = pd.concat([Area_pot, Area_pot2], axis=1)
        Ang_pot = pd.concat([Ang_pot, Ang_pot2], axis=1)
        potOrb = pd.concat([potOrb, potOrb2], axis=0)
        Ang_giro = pd.concat([Ang_giro, Ang_giro2], axis=1)

with pd.ExcelWriter(f'data/ID-{simulacion}.xlsx') as writer:
    
    Wpot.to_excel(writer, sheet_name='Potencia')
    Area_pot.to_excel(writer, sheet_name='Area expuesta')
    Ang_pot.to_excel(writer, sheet_name='Angulo de incidencia')
    potOrb.to_excel(writer, sheet_name='Potencia por orbita')
    Ang_giro.to_excel(writer, sheet_name='Angulo de giro')

texto = f"ID Simulacion: {simulacion}\n" \
    f"#############################\n" \
    f"############ Datos ##########\n" \
    f"#############################\n" \
    f"\n" \
    f"    #### Orbita ####" \
    f"\n" \
    f"    Semieje Mayor: {a}    \n" \
    f"    Excentricidad: {ecc}  \n" \
    f"    Inclinacion:   {inc}  \n" \
    f"    RAAN:          {raan} \n" \
    f"\n" \
    f"\n" \
    f"    #### Satelite #### \n" \
    f"\n" \
    f"    Modelo:                 {direccion} \n" \
    f"    Nº Caras:               {EPM.numero_caras}\n" \
    f"    Area Paneles            {EPM.Area_caras}\n" \
    f"    Paneles Despegables:    {EPM.Caras_Despegables}\n" \
    f"    Normales Caras:         {EPM.Normales_caras}\n" \
    f"    Nombres Caras:          {EPM.name}\n"

f = open(f'data/processed/ID-{simulacion}.txt', 'wb')
f.write(texto.encode())
f.close()
print(f'{simulacion}')
