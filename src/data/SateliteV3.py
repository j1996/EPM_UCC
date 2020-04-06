from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth, Sun
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.util import norm_fast
import numpy as np
import trimesh
from Orbitas import *
import numba
import pandas as pd
from SatelitteSolarPowerSystemV3 import SatelitteSolarPowerSystem
from tqdm import tqdm
simulacion = random_generator()

a = 7278 * u.km
ecc = 0 * u.one
inc = 90 * u.deg
raan = 0* u.deg
argp_ini = 0 * u.deg
nu = 0 * u.deg
time = Time("2020-01-01 12:00:00", scale="utc")
i=0
direccion = 'models/12Unuv.stl'
EPM = SatelitteSolarPowerSystem(direccion)
for k in tqdm(np.arange(0, 365)):
    time_ini = time+TimeDelta(1*u.day)*k
    iter = pd.MultiIndex.from_arrays([[time_ini.iso[0:10]]*len(EPM.name), EPM.name])
    W, Area_potencia, Ang=propagate_fast_one_orbit(a, ecc, inc,raan, nu,  time_ini,argp_ini, EPM,50)
    if k==0:
        Wpot=pd.DataFrame(W, columns= iter)
        pot=np.matrix(W).sum(axis=0) / len(W)
        potOrb=pd.DataFrame(pot, columns=iter)
        Area_pot=pd.DataFrame(Area_potencia, columns= iter)
        Ang_pot=pd.DataFrame(Ang, columns= iter)
    else:
        Wpot2 = pd.DataFrame(W, columns=iter)
        Area_pot2 = pd.DataFrame(Area_potencia, columns=iter)
        Ang_pot2 = pd.DataFrame(Ang, columns=iter)
        pot = np.matrix(W).sum(axis=0) / len(W)
        potOrb2 = pd.DataFrame(pot, columns=iter)
        Wpot=pd.concat([Wpot,Wpot2],axis=1)
        Area_pot=pd.concat([Area_pot,Area_pot2],axis=1)
        Ang_pot=pd.concat([Ang_pot,Ang_pot2], axis=1)
        potOrb=pd.concat([potOrb, potOrb2], axis=1)

Wpot.to_csv(f'resultados/Wpot_ID-{simulacion}.csv')
Wpot.to_excel(f'resultados/Wpot_ID-{simulacion}.xlsx')
Area_pot.to_csv(f'resultados/Area_pot_ID-{simulacion}.csv')
Area_pot.to_excel(f'resultados/Area_pot_ID-{simulacion}.xlsx')
Ang_pot.to_csv(f'resultados/Ang_pot_ID-{simulacion}.csv')
Ang_pot.to_excel(f'resultados/Ang_pot_ID-{simulacion}.xlsx')
potOrb.to_csv(f'resultados/Potencia_por_orbita_ID-{simulacion}.csv')
potOrb.to_excel(f'resultados/Potencia_por_orbita_ID-{simulacion}.xlsx')
texto=f"ID Simulacion: {simulacion}\n" \
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

f = open(f'resultados/ID-{simulacion}', 'wb')
f.write(texto.encode())
f.close()