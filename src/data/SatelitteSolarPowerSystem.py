import numpy as np
import trimesh
from Satellite_Panel_Solar import Panel_Solar

# noinspection SpellCheckingInspection
"""Satelitte Solar Power System 
Es una clase donde se incluye todo el sistema de potencia del satelitte, permite incluir un modelo en CAD
y realizar su analisis de potencia dependiento de un vector utilizado como la direccion del sol hacia el satelite 



"""

class SatelitteSolarPowerSystem(object):

    def __init__(self, direccion, panel_despegable_dual=True):

        self.mesh = self.cargar_modelo(direccion)
        self.numero_caras = len(self.mesh.facets)
        self.Normales_caras = self.mesh.facets_normal
        self.Area_caras = self.mesh.facets_area
        self.caracteristicas_panel_solar = [Panel_Solar('Estandar')] * self.numero_caras
        self.Caras_Despegables = self.caras_despegables()
        self.sombra = self.posible_sombra()
        self.mesh.vertices -= self.mesh.centroid
        self.sun_plane = self.puntos_sol()
        self.panel_despegable_dual = panel_despegable_dual
        self.name = self.nombrar_caras()

    def cargar_modelo(self, direccion):

        return trimesh.load_mesh(direccion)

    def nombrar_caras(self):

        name = []
        j = 0
        o = 0
        for i in self.mesh.facets_normal:
            i = np.round(i)
            if (i == [1, 0, 0]).all():
                name.append('X+')
            elif (i == [-1, 0, 0]).all():
                name.append('X-')
            elif (i == [0, 1, 0]).all():
                name.append('Y+')
            elif (i == [0, -1, 0]).all():
                name.append('Y-')
            elif (i == [0, 0, -1]).all():
                name.append('Z-')
            elif (i == [0, 0, 1]).all():
                name.append('Z+')
            else:
                name.append(f'Panel direction {i}')
            if j in self.Caras_Despegables:
                name[j] = name[j] + f'  Panel Despegable {o}'
                o += 1

            j += 1
        return name

    def caras_despegables(self):

        caras_despegables = []
        for i in np.arange(0, len(trimesh.repair.broken_faces(self.mesh))):
            caras_despegables.append(
                np.array(np.where(self.mesh.facets == trimesh.repair.broken_faces(self.mesh)[i])).flatten()[0])
        caras_despegables = list(set(caras_despegables))  # se encuentran las caras que son despegables
        return caras_despegables

    def posible_sombra(self):
        """buscar la cara mas cercana a los paneles que puede dar sombra"""

        sombra = np.array(np.where(self.mesh.facets_on_hull == False)).flatten()
        return sombra

    def puntos_sol(self):
        n = round(self.mesh.scale * 1.2)
        mesh2 = trimesh.Trimesh(vertices=[[0, 0, 0], [n, 0, 0], [0, n, 0], [n, n, 0]],
                                faces=[[0, 1, 2], [2, 1, 3]])
        mesh2 = trimesh.remesh.subdivide_to_size(vertices=mesh2.vertices, faces=mesh2.faces, max_edge=15)
        sun_plane = trimesh.Trimesh(mesh2[0], mesh2[1])
        sun_plane.vertices -= sun_plane.centroid
        sun_plane.vertices += np.array([0, 0, n])
        return sun_plane

    def celdas_activas(self, Sun_vector):
        sun_planeAux = self.sun_plane
        sun_planeAux.apply_transform(trimesh.geometry.align_vectors(sun_planeAux.facets_normal.flatten(), Sun_vector))
        ray_origins = sun_planeAux.vertices
        ray_directions = np.array([-Sun_vector] * len(sun_planeAux.vertices))
        if trimesh.ray.has_embree == True:

            index_tri = self.mesh.ray.intersects_first(ray_origins=ray_origins, ray_directions=ray_directions)
        else:
            locations, index_ray, index_tri = self.mesh.ray.intersects_location(ray_origins=ray_origins,
                                                                                ray_directions=ray_directions,
                                                                                multiple_hits=False)
        index_tri = list(set(index_tri))
        return index_tri

    def Add_prop_Panel(self, e):

        self.caracteristicas_panel_solar.append(e)

    def power_panel_solar(self, index_tri, Sun_vector, WSun):
        ang = list(map(Sun_vector.dot, self.mesh.facets_normal))
        # np.isin(self.index_tri, self.mesh.facets[9]).any()
        area_potencia = []
        W = []
        for i in np.arange(0, len(self.mesh.facets)):
            if (i in self.Caras_Despegables) & (self.panel_despegable_dual == True) & (ang[i] < 0):
                ang_inc = -ang[i]
            else:
                ang_inc = ang[i]

            if i in self.sombra:
                o = np.isin(index_tri, self.mesh.facets[i])
                o = o[o == True]
                area = (len(o) / len(self.mesh.facets[i])) * self.mesh.facets_area[i] / (1000 ** 2)
                area_potencia.append(area)
            else:
                area = self.mesh.facets_area[i] / (1000 ** 2)
                area_potencia.append(area)

            if (ang_inc >= 0) & (ang_inc < ((np.pi / 180) * 75)):
                W.append(area * self.caracteristicas_panel_solar[i].psolar_rendimiento * WSun * ang_inc)
            else:
                W.append(0.)

        return W, area_potencia, ang

    def Calculo_potencia(self, Sun_vector, WSun=1310):
        index_tri = self.celdas_activas(Sun_vector)

        W, area_potencia, ang = self.power_panel_solar(index_tri, Sun_vector, WSun)
        return W, area_potencia, ang

    def apply_transform(self, matrix):
        self.mesh.apply_transform(matrix)
        self.name = []
        self.name = self.nombrar_caras()
    def visual(self):

        ax = trimesh.creation.axis(axis_radius=50, axis_length=500)
        scene = trimesh.Scene([self.mesh.apply_scale(0.1), ax])

        return scene.show()
if __name__ == '__main__':
    d = SatelitteSolarPowerSystem(direccion='models/12Unuv.stl')


    Sun_vector =np.array([-0.10486044,  0.91244007,  0.39554696])
    W, area_potencia, ang = d.Calculo_potencia(Sun_vector)
