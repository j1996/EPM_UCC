from astropy.coordinates import get_sun
from astropy.time import Time, TimeDelta
from poliastro.bodies import Earth, Sun
from astropy import units as u
from poliastro.twobody import Orbit
from poliastro.util import norm_fast
import numpy as np
import string
import random
def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def SolarAngle_a_VNB(Orbit):
    sun = get_sun(Orbit.epoch).cartesian.xyz.value
    sun = sun / np.linalg.norm(sun)
    V = np.array(Orbit.v*u.s/(u.km*np.linalg.norm(Orbit.v)))
    N = np.array(Orbit.r*1/(np.linalg.norm(Orbit.r)*u.km))
    B = np.cross(Orbit.r, Orbit.v)*1/np.linalg.norm(np.cross(Orbit.r, Orbit.v))
    VNB = [ V, N, B]
    solardirection = np.matrix(VNB)*sun.reshape(3,1)
    solardirection = np.array(solardirection).flatten()
    return solardirection

def EclipseLocator(Orbit):

    sat = Orbit.r.value
    sun = get_sun(Orbit.epoch).cartesian.xyz.to_value(u.km)
    satsun = sat+sun

    if norm_fast(satsun) > norm_fast(sun):
        ang = np.arccos(np.dot(sat/norm_fast(sat), satsun/norm_fast(satsun)))

        h = np.sin(ang) * norm_fast(sat)

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
    sat = Orbit.from_classical(Earth, a, ecc, inc, raan, argp_ini, nu, time_ini)
    dt=sat.period.value/iteraciones_orbita
    argp_nom=(2*np.pi)/iteraciones_orbita
    for i in np.arange(0,iteraciones_orbita):
        argp=(argp_nom*i)*(180/np.pi)*u.deg
        time = time_ini+TimeDelta(dt*u.second)*i

        sat = Orbit.from_classical(Earth, a, ecc, inc, raan, argp, nu, time)

        if not EclipseLocator(sat):
            sun_vector = SolarAngle_a_VNB(sat)
            W, area_potencia, ang = EPM.Calculo_potencia(sun_vector)
        else:
            zeros=[0.0]*EPM.numero_caras
            W=zeros
            area_potencia=zeros
            ang=zeros

        w.append(W), Area_potencia.append(area_potencia), Ang.append(ang)
    return w, Area_potencia, Ang

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
