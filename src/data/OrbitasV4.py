from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth, Sun
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.util import norm
import numpy as np
import string
import random
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def SolarAngle_a_VNB(Orbit):
    sun = get_sun(Orbit.epoch).cartesian.xyz.value
    sun = sun / np.linalg.norm(sun)
    V = np.array(Orbit.v.value/(np.linalg.norm(Orbit.v)))
    
    N = np.array(Orbit.r.value*1/(np.linalg.norm(Orbit.r)))
    
    B = np.cross(Orbit.r.value, Orbit.v.value)*1/np.linalg.norm(np.cross(Orbit.r.value, Orbit.v.value))
    
    VNB = np.column_stack((V.reshape(3,1), N.reshape(3,1),B.reshape(3,1)))
    
    solardirection = np.dot(np.linalg.inv(VNB),sun.reshape(3,1))
    solardirection = np.array(solardirection).flatten()
    return solardirection

def EclipseLocator(Orbit):

    sat = Orbit.r.value
    sun = get_sun(Orbit.epoch).cartesian.xyz.to_value(u.km)
    satsun = sat+sun

    if norm(satsun) > norm(sun):
        ang = np.arccos(np.dot(sat/norm(sat), satsun/norm(satsun)))

        h = np.sin(ang) * norm(sat)

        if h <= Earth.R.to(u.km).value:

            return True
        else:
            return False
    else:

        return False

def propagate_fast_one_orbit(a, ecc, inc,raan, nu,  time_ini,argp_ini, EPM,iteraciones_orbita=100):
    w=[]
    Area_potencia=[]
    Ang=[]
    Angulo_giro=[]
    sat = Orbit.from_classical(Earth, a, ecc, inc, raan, argp_ini, nu, time_ini)
    dt=sat.period.value/iteraciones_orbita
    argp_nom=(2*np.pi)/iteraciones_orbita
    for i in np.arange(0,iteraciones_orbita):
        argp=(argp_nom*i)*(180/np.pi)*u.deg
        time = time_ini+TimeDelta(dt*u.second)*i

        sat = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, time)
        if (EPM.actitud.apuntado_constante_sol==False) :
            if (i==0) :
                EPM.actitud.apuntado_sol=True
            else:
                EPM.actitud.apuntado_sol=False

            
        if not EclipseLocator(sat):
            sun_vector = SolarAngle_a_VNB(sat)
            W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(sun_vector)
        else:
            zeros=[0.0]*EPM.numero_caras
            W=zeros
            area_potencia=zeros
            ang=zeros
            angulo_giro=[0.0, 0.0, 0.0]

        w.append(W), 
        Area_potencia.append(area_potencia),
        Ang.append(ang), 
        
        Angulo_giro.append(angulo_giro)
    return w, Area_potencia, Ang, Angulo_giro

if __name__ == '__main__':
    time = Time("2018-09-28 00:00:00", scale="utc")

    #eclipse locator
    n=np.array([0, 0, 1])

    a = 7278 * u.km
    ecc = 0 * u.one
    inc = 90 * u.deg
    raan = 0* u.deg
    argp = 0 * u.deg
    nu = 0 * u.deg
    i=0
    ss = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, time)
    # for o in np.arange(0,103):
    #     ss=ss.propagate(1*u.min)
    #     d=EclipseLocator(ss)
    #     print(d)
    #     if d:
    #         i+=1
    #         print(i)
    #
