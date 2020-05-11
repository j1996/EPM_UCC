from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth, Sun
from astropy import units as u
from poliastro.twobody import Orbit

import numpy as np
import trimesh

import numba
import pandas as pd
try:
    from SatelitteSolarPowerSystemV4 import SatelitteSolarPowerSystem
    from SatelitteActitud import SatelitteActitud
    from OrbitasV4 import *
except:
    from src.data.SatelitteSolarPowerSystemV4 import SatelitteSolarPowerSystem
    from src.data.SatelitteActitud import SatelitteActitud
    from src.data.OrbitasV4 import *
from tqdm import tqdm
simulacion = random_generator()

a = 7278 * u.km
ecc = 0 * u.one
inc = 90 * u.deg
raan =  0* u.deg
argp_ini = 0.5 * u.deg
nu = 0 * u.deg
time = Time("2020-01-01 12:00:00", scale="utc")
i = 0
direccion = 'models/3U1P.stl'
actitud = SatelitteActitud(eje_de_spin=[1, 0, 0], control=False)
EPM = SatelitteSolarPowerSystem(
    direccion, actitud, Despegables_orientables=False)
EPM.actitud.apuntado_constante_sol = False
EPM.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0], [0, 0, 0]))

for k in tqdm(np.arange(0, 365)):
    time_ini = time+TimeDelta(1*u.day)*k
    iter = pd.MultiIndex.from_arrays(
        [[time_ini.iso[0
        :10]]*len(EPM.name), EPM.name])
    iter2 = pd.MultiIndex.from_arrays([[time_ini.iso[0:10]]*(len(EPM.Caras_Despegables)+1), [
                                      "Spin Axis"]+[EPM.name[i] for i in EPM.Caras_Despegables]])
    W, Area_potencia, Ang, Angulo_giro = propagate_orbit(
        a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, 100, 1)

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
with pd.ExcelWriter(f'data/processed/ID-{simulacion}.xlsx') as writer:
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
