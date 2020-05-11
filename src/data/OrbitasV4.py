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
    #https://help.agi.com/stk/11.0.1/Content/gator/eq-coordsys.htm
    #https://ai-solutions.com/_freeflyeruniversityguide/attitude_reference_frames.htm
    # se obtiene el vector sol en GCRS en coordenadas cartesianas
    sun = get_sun(Orbit.epoch).cartesian.xyz.value
    sun = sun / np.linalg.norm(sun)


    V = np.array(Orbit.v.value/(np.linalg.norm(Orbit.v)))
    X = V #el vector velocidad es el eje X
    R = np.array(Orbit.r.value*1/(np.linalg.norm(Orbit.r)))
    N = np.cross(R, V) 
    N = N/np.linalg.norm(N)
    Y = N # El vector es en la direccion de la normal de la orbita
    B = np.cross(X, Y)
    B = B/np.linalg.norm(B)
    Z = B

    #B = Orbit.h_vec.value/np.linalg.norm(Orbit.h_vec.value)
    VNB = np.column_stack((X.reshape(3, 1), Y.reshape(3, 1), Z.reshape(3, 1)))

    solardirection = np.dot(np.linalg.inv(VNB), sun.reshape(3, 1))
    solardirection = np.array(solardirection).flatten()
    return solardirection
def to_VNB(Orbit):
    #https://help.agi.com/stk/11.0.1/Content/gator/eq-coordsys.htm
    #https://ai-solutions.com/_freeflyeruniversityguide/attitude_reference_frames.htm
    # se obtiene el vector sol en GCRS en coordenadas cartesianas
    
    V = np.array(Orbit.v.value/(np.linalg.norm(Orbit.v)))
    X = V #el vector velocidad es el eje X
    R = np.array(Orbit.r.value*1/(np.linalg.norm(Orbit.r)))
    N = np.cross(R, V) 
    N = N/np.linalg.norm(N)
    Y = N # El vector es en la direccion de la normal de la orbita
    B = np.cross(X, Y)
    B = B/np.linalg.norm(B)
    Z = B

    #B = Orbit.h_vec.value/np.linalg.norm(Orbit.h_vec.value)
    VNB = np.column_stack((X.reshape(3, 1), Y.reshape(3, 1), Z.reshape(3, 1)))

    
    return VNB

def SolarRay_to_LVLH(Orbit):
    sun = get_sun(Orbit.epoch).cartesian.xyz.value
    sun = sun / np.linalg.norm(sun)
    V = np.array(Orbit.v.value/(np.linalg.norm(Orbit.v)))

    R = -np.array(Orbit.r.value*1/(np.linalg.norm(Orbit.r)))
    X=R
    Z = np.cross(V, R)
    Z = Z/np.linalg.norm(Z)
    Y = np.cross(Z, X)
    Y = Y/np.linalg.norm(Y)
    #B = Orbit.h_vec.value/np.linalg.norm(Orbit.h_vec.value)
    LVLH = np.column_stack((X.reshape(3, 1), Y.reshape(3, 1), Z.reshape(3, 1)))

    solardirection = np.dot(np.linalg.inv(LVLH), sun.reshape(3, 1))
    solardirection = np.array(solardirection).flatten()
    
    return solardirection

def to_LVLH(Orbit):
    
    V = np.array(Orbit.v.value/(np.linalg.norm(Orbit.v)))

    R = -np.array(Orbit.r.value*1/(np.linalg.norm(Orbit.r)))
    X=R
    Z = np.cross(V, R)
    Z = Z/np.linalg.norm(Z)
    Y = np.cross(Z, X)
    Y = Y/np.linalg.norm(Y)
    #B = Orbit.h_vec.value/np.linalg.norm(Orbit.h_vec.value)
    LVLH = np.column_stack((X.reshape(3, 1), Y.reshape(3, 1), Z.reshape(3, 1)))
    
    return LVLH

def EclipseLocator(Orbit):

    sat = Orbit.r.value
    sun = get_sun(Orbit.epoch).cartesian.xyz.to_value(u.km)
    satsun = sat+sun

    if np.linalg.norm(satsun) > np.linalg.norm(sun):
        ang = np.arccos(np.dot(sat/np.linalg.norm(sat),
                               satsun/np.linalg.norm(satsun)))

        h = np.sin(ang) * np.linalg.norm(sat)

        if h <= Earth.R.to(u.km).value:

            return True
        else:
            return False
    else:

        return False

def propagate_orbit(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1):
    w = []
    Area_potencia = []
    Ang = []
    Angulo_giro = []
    sat = Orbit.from_classical(
        Earth, a, ecc, inc, raan, argp_ini, nu, time_ini)
    dt = sat.period.value/iteraciones_orbita
    
    for p in np.arange(0, num_orbitas):
        for i in np.arange(0, iteraciones_orbita):
            
            sat=sat.propagate(dt*u.second)

            
            if (EPM.actitud.apuntado_constante_sol == False):
                if (i == 0):
                    EPM.actitud.apuntado_sol = True
                else:
                    EPM.actitud.apuntado_sol = False

            if not EclipseLocator(sat):
                sun_vector = SolarRay_to_LVLH(sat)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun_vector)
            else:
                sun_vector = SolarRay_to_LVLH(sat)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun_vector)
                zeros = [0.0]*EPM.numero_caras
                W = zeros
                area_potencia = zeros
                ang = zeros

            w.append(W),
            Area_potencia.append(area_potencia),
            Ang.append(ang),

            Angulo_giro.append(angulo_giro)
        
    return w, Area_potencia, Ang, Angulo_giro
def propagate_fast_one_orbit(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1):
    w = []
    Area_potencia = []
    Ang = []
    Angulo_giro = []
    sat = Orbit.from_classical(
        Earth, a, ecc, inc, raan, argp_ini, nu, time_ini)
    dt = sat.period.value/iteraciones_orbita
    argp_nom = (2*np.pi)/iteraciones_orbita
    for p in np.arange(0, num_orbitas):
        for i in np.arange(0, iteraciones_orbita):
            argp = (argp_nom*i)*(180/np.pi)*u.deg + argp_ini
            time = time_ini+TimeDelta(dt*u.second)*i

            sat = Orbit.from_classical(
                Earth, a, ecc, inc, raan, argp, nu, time)
            if (EPM.actitud.apuntado_constante_sol == False):
                if (i == 0):
                    EPM.actitud.apuntado_sol = True
                else:
                    EPM.actitud.apuntado_sol = False

            if not EclipseLocator(sat):
                sun_vector = SolarRay_to_LVLH(sat)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun_vector)
            else:
                sun_vector = SolarRay_to_LVLH(sat)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun_vector)
                zeros = [0.0]*EPM.numero_caras
                W = zeros
                area_potencia = zeros
                ang = zeros

            w.append(W),
            Area_potencia.append(area_potencia),
            Ang.append(ang),

            Angulo_giro.append(angulo_giro)
        time_ini = time
    return w, Area_potencia, Ang, Angulo_giro

def propagate_orbit2(a, ecc, inc, raan, nu,  time_ini, argp_ini, EPM, iteraciones_orbita=100, num_orbitas=1):
    w = []
    Area_potencia = []
    Ang = []
    Angulo_giro = []
    sat = Orbit.from_classical(
        Earth, a, ecc, inc, raan, argp_ini, nu, time_ini)
    dt = sat.period.value/iteraciones_orbita
    
    for p in np.arange(0, num_orbitas):
        for i in np.arange(0, iteraciones_orbita):
            
            sat=sat.propagate(dt*u.second)
            sun = get_sun(sat.epoch).cartesian.xyz.value
            sun = sun / np.linalg.norm(sun)
            
            if (EPM.actitud.apuntado_constante_sol == False):
                if (i == 0):
                    EPM.actitud.apuntado_sol = True
                else:
                    EPM.actitud.apuntado_sol = False

            if not EclipseLocator(sat):
                trans=to_LVLH(sat)
                trans2=np.zeros((4,4))
                trans2[0:3,0:3]=trans
                trans2[3,3]=1
                EPM.mesh.apply_transform(trans2)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun)
            else:
                trans=to_LVLH(sat)
                trans2=np.zeros((4,4))
                trans2[0:3,0:3]=trans
                trans2[3,3]=1
                EPM.mesh.apply_transform(trans2)
                W, area_potencia, ang, angulo_giro = EPM.Calculo_potencia(
                    sun)
                zeros = [0.0]*EPM.numero_caras
                W = zeros
                area_potencia = zeros
                ang = zeros

            w.append(W),
            Area_potencia.append(area_potencia),
            Ang.append(ang),

            Angulo_giro.append(angulo_giro)
        
    return w, Area_potencia, Ang, Angulo_giro

if __name__ == '__main__':
    time = Time("2018-09-28 00:00:00", scale="utc")

    # eclipse locator
    n = np.array([0, 0, 1])

    a = 7278 * u.km
    ecc = 0 * u.one
    inc = 90 * u.deg
    raan = 0 * u.deg
    argp = 0 * u.deg
    nu = 0 * u.deg
    i = 0
    ss = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, time)
    # for o in np.arange(0,103):
    #     ss=ss.propagate(1*u.min)
    #     d=EclipseLocator(ss)
    #     print(d)
    #     if d:
    #         i+=1
    #         print(i)
    #
