import numpy as np
import trimesh
try:
    from Satellite_Panel_Solar import Panel_Solar
    from SatelitteActitud import SatelitteActitud
except:
    from src.data.Satellite_Panel_Solar import Panel_Solar
    from src.data.SatelitteActitud import SatelitteActitud

# noinspection SpellCheckingInspection
"""Satelitte Solar Power System 
Es una clase donde se incluye todo el sistema de potencia del satelitte, permite incluir un modelo en CAD
y realizar su analisis de potencia dependiento de un vector utilizado como la direccion del sol hacia el satelite 

Example:
    Para llamar a esta clase solo hace falta, una linea como la de abajo:

        $ Sat = SatelitteSolarPowerSystem(direccion='models/12U.stl')

Esta clase tiene varios atributos incluidos como la caracteristica de cada panel solar
para ello solo se necesita llamar a la clase con:
    $ from Satellite_Panel_Solar import Panel_Solar
    $ Sat.caracteristicas_panel_solar=[Panel_solar()] 
Para ver como se configura cada Panel_solar hay que remitirse a su documentacion
Finalmente notar que el atributo mesh incluye todos aquellos del paquete trimesh
"""


class SatelitteSolarPowerSystem(object):

    def __init__(self, direccion, SatelitteActitud, panel_despegable_dual=True, Despegables_orientables=False):
        """Se inicia la clase con el analisis de la figura para
        encontrar paneles despegables, sombra, etc.

        Args:
            direccion: string con la direcion del archivo y con el tipo del archivo Ex. .STL, .OBJ, .PLY
            panel_despegable_dual: Default(True)
            """
        self.mesh = self.cargar_modelo(direccion)
        self.numero_caras = len(self.mesh.facets)
        # Normales de las caras en el momento 0
        self.Normales_caras = self.mesh.facets_normal
        self.Area_caras = self.mesh.facets_area
        self.caracteristicas_panel_solar = [
            Panel_Solar('Estandar')] * self.numero_caras
        self.Caras_Despegables = self.caras_despegables()
        self.sombra = self.posible_sombra()
        self.mesh.vertices -= self.mesh.centroid
        self.sun_plane = self.puntos_sol()
        self.panel_despegable_dual = panel_despegable_dual
        self.name = self.nombrar_caras()
        self.actitud = SatelitteActitud
        self.Despegables_orientables = Despegables_orientables

    def cargar_modelo(self, direccion):
        """
        cargar_modelo
        Args:
            direccion: string con la direcion del y con el tipo del archivo Ex. .STL, .OBJ, .PLY

        Returns:
            trimesh.mesh
        """
        return trimesh.load_mesh(direccion)

    def nombrar_caras(self):
        """
        nombrar_caras
        Nombra las caras del modelo para poder utilizarlas se realiza al principio porque si se gira cambiara
        Simplemente nombra las caras con X, Y, Z

        Returns:
            name: devuelve el nombre de las caras de manera X, Y, Z
        """
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
        """
        caras_despegables
        Localiza los paneles despegables, es un metodo bastante dificil

        Returns:
            caras_despeables: es el numero de las caras
        """
        caras_despegables = []

        # si las caras se encuentran con otras sin volumen como los paneles,
        # esta las toman como rotas por trimesh por lo que se pueden localizar

        for i in np.arange(0, len(trimesh.repair.broken_faces(self.mesh))):

            caras_despegables.append(
                np.array(np.where(self.mesh.facets == trimesh.repair.broken_faces(self.mesh)[i])).flatten()[0])

        # se encuentran las caras que son despegables
        # elimina las repetidas
        caras_despegables = list(set(caras_despegables))

        return caras_despegables

    def posible_sombra(self):
        """
        posible_sombra
        buscar la cara mas cercana a los paneles que puede dar sombra
        Returns:
            sombra:numero de las caras que pueden tener sombra
        """

        sombra = np.array(
            np.where(self.mesh.facets_on_hull == False)).flatten()
        return sombra

    def puntos_sol(self):
        """
        puntos_sol 
        Crea un conjunto de puntos de aquellos que darian sombra 
        con los centros de los paneles

        Returns:
            trimesh.mesh : Plano de puntos 
        """
        p = self.mesh.facets[self.sombra].flatten()
        sun_plane = self.mesh.triangles_center[p]

        return sun_plane

    def celdas_activas(self, sun_vector):
        """
        celdas_activas 
        Localiza las celdas activas de un mallado al buscarse los puntos donde golpearia un rayo en la malla des los puntos_sol

        Args:
            sun_vector (array(,3)) : Vector sol

        Returns:
            index_tri [array(n)]: El numero de triangulo que esta activo al ser golpeado por el sol 
        """

        sun_planeAux = self.puntos_sol()+5000*sun_vector
        ray_origins = sun_planeAux
        ray_directions = np.array([-sun_vector] * len(sun_planeAux))

        if trimesh.ray.has_embree:  # Hay una  libreria que es embree solo funciona en linux pero va 50x mas rapido

            index_tri = self.mesh.ray.intersects_first(
                ray_origins=ray_origins, ray_directions=ray_directions)

        else:

            locations, index_ray, index_tri = self.mesh.ray.intersects_location(ray_origins=ray_origins,
                                                                                ray_directions=ray_directions,
                                                                                multiple_hits=False)
        index_tri = list(set(index_tri))
        return index_tri

    def Add_prop_Panel(self, e):
        """
        Add_prop_Panel 
        Añade propiedades al panel 

        Args:
            e (Panel_Solar): Panel Solar
        """
        self.caracteristicas_panel_solar.append(e)

    def power_panel_solar(self, index_tri, Sun_vector, WSun):
        """
        power_panel_solar 
        Obtiene la potencia producida por el satelite con actitud fija 

        Args:
            index_tri (array(,:)): Celdas activas por el rayo 
            Sun_vector (array(,3)): Vector sol en LVLH
            WSun (float): Potencia irradiada por el sol 

        Returns:
            W (array(,n)) : Potencia generada
            area_potencia (array(,n)) : Areas que generan potencia
            ang (array(,n)) : Angulo de incidencia del vector sol con las caras

        n : numero de caras
        """

        # Producto escalar

        ang = list(map(Sun_vector.dot, self.mesh.facets_normal))

        # Se inicializan las variables

        area_potencia = []
        W = []

        for i in np.arange(0, len(self.mesh.facets)):

            # Esto es para si consideramos que

            if (i in self.Caras_Despegables) & (self.panel_despegable_dual == True) & (ang[i] < 0):
                ang_inc = -ang[i]
            else:
                ang_inc = ang[i]

            # Buscar en las zonas donde es posible la sombra el valor propocional de area en los que incide la luz

            if i in self.sombra:
                o = np.isin(index_tri, self.mesh.facets[i])
                o = o[o == True]
                area = (
                    len(o) / len(self.mesh.facets[i])) * self.mesh.facets_area[i] / (1000 ** 2)
                area_potencia.append(area)
            else:
                area = self.mesh.facets_area[i] / (1000 ** 2)  # esta en mm^2
                area_potencia.append(area)

            # Esto es para eliminar las areas que no cumplen la ley de que menos de 15 grados no producen energia

            if (ang_inc >= 0) & (ang_inc > (np.cos((np.pi / 180) * 75))):
                W.append(
                    area * self.caracteristicas_panel_solar[i].psolar_rendimiento * WSun * ang_inc)
            else:
                W.append(0.)

        return W, area_potencia, ang

    def power_panel_con_actitud(self, Sun_vector, WSun):
        """
        power_panel_con_actitud 
        Obtiene la potencia producida por el satelite con actitud apuntando al sol

        Args:
            Sun_vector (array(,3)): Vector sol en LVLH
            WSun (float): Potencia irradiada por el sol 

        Returns:
            W (array(,n)) : Potencia generada
            area_potencia (array(,n)) : Areas que generan potencia
            ang (array(,n)) : Angulo de incidencia del vector sol con las caras
            angulo_giro (array(,n)) : Angulo de giro del satelite 
        n : numero de caras
        """
        # Si los paneles son fijos al satelite
        if self.Despegables_orientables == False:
            if self.actitud.apuntado_sol == True:

                # aqui empieza la magia
                # la intencion era formar dos planos entre el eje de spin y el vector sol y otro
                # con el eje de spin y una direccion principal de los paneles solares
                # para poder calcular el angulo que deberia girarse entre los dos planos

                direcion_principal = self.mesh.facets_normal[self.Caras_Despegables[0]]

                plano0 = np.cross(Sun_vector, self.actitud.eje_de_spin)
                plano0 = plano0/np.linalg.norm(plano0)

                plano1 = np.cross(direcion_principal, self.actitud.eje_de_spin)

                plano1 = plano1/np.linalg.norm(plano1)

                angulo_giro = np.arccos(np.absolute(
                    np.dot(plano0, plano1)))/(np.linalg.norm(plano0)*np.linalg.norm(plano1))

                if np.isnan(angulo_giro):
                    angulo_giro = 0.0

                if angulo_giro == 0:
                    pass

                else:

                    # Comprueba si la transformacion produciria que fuesen iguales los giros

                    prim = trimesh.transform_points(plano1.reshape(1, 3), trimesh.transformations.rotation_matrix(
                        angulo_giro, self.actitud.eje_de_spin, [0, 0, 0]))
                    if not np.allclose(prim, plano0):
                        angulo_giro = -angulo_giro
                    self.mesh = self.mesh.apply_transform(trimesh.transformations.rotation_matrix(
                        angulo_giro, self.actitud.eje_de_spin, [0, 0, 0]))
            else:
                angulo_giro = 0.0

            index_tri = self.celdas_activas(Sun_vector)
            W, area_potencia, ang = self.power_panel_solar(
                index_tri, Sun_vector, WSun)

            return W, area_potencia, ang, angulo_giro

        else:

            if self.actitud.apuntado_sol == True:

                # mas magia por aqui
                # pero ahora con lo de la proyeccion en unos ejes para poder utilizar el giro
                # esto funciona bastante bien el problema es cuando se pasa el ecuador

                direcion_principal = self.mesh.facets_normal[self.Caras_Despegables[0]]
                direcion_principal = np.round(
                    direcion_principal/np.linalg.norm(direcion_principal), 5)

                matrix_projection = trimesh.transformations.projection_matrix(
                    [0, 0, 0], self.actitud.eje_de_spin)[0:3, 0:3]
                proyeccion = np.dot(matrix_projection, Sun_vector)
                proyeccion = proyeccion/np.linalg.norm(proyeccion)
                ver = np.arccos(np.dot(proyeccion, direcion_principal))

                if np.isnan(ver):
                    ver = 0.0
                if ver < 0.1e-4:
                    angulo_giro = 0.0
                    pass
                else:

                    # print("proyeccion",proyeccion)
                    # print("direprinci",direcion_principal)
                    #angulo_giro=np.arccos(np.absolute(np.dot(direcion_principal, proyeccion)))/(np.linalg.norm(direcion_principal)*np.linalg.norm(proyeccion))
                    transforma = trimesh.geometry.align_vectors(
                        direcion_principal, proyeccion)
                    # posicion_eje=np.array(np.where(np.array(self.actitud.eje_de_spin)==1)).flatten().max()

                    angulo_giro = trimesh.transformations.rotation_from_matrix(transforma)[
                        0]
                    dir = trimesh.transform_points(
                        direcion_principal.reshape(1, 3), transforma)

                    if np.absolute(angulo_giro) > 0.05:

                        transforma2 = np.round(trimesh.geometry.align_vectors(
                            direcion_principal, -proyeccion), 5)
                        angulo_giro2 = trimesh.transformations.rotation_from_matrix(transforma2)[
                            0]
                        dir = trimesh.transform_points(
                            direcion_principal.reshape(1, 3), transforma)

                        if np.absolute(angulo_giro2) < np.absolute(angulo_giro):
                            transforma = transforma2
                            angulo_giro = angulo_giro2

                        else:
                            pass
                    # if plano1[posicion_eje]==0:
                    #   angulo_giro=0.0
                    if np.isnan(angulo_giro):
                        angulo_giro = 0.0
                        pass
                    else:
                        self.mesh.apply_transform(transforma)
            else:
                angulo_giro = 0.0

            ang = list(map(Sun_vector.dot, self.mesh.facets_normal))
            area_potencia = []
            W = []
            angulo_giro = [angulo_giro]

            for i in np.arange(0, len(self.mesh.facets)):
                area = self.mesh.facets_area[i] / (1000 ** 2)
                area_potencia.append(area)
                if (i in self.Caras_Despegables):
                    angulo_giro.append(np.arccos(ang[i]))
                    ang[i] = 1
                if (ang[i] >= 0) & (ang[i] > (np.cos((np.pi / 180) * 75))):
                    W.append(
                        area * self.caracteristicas_panel_solar[i].psolar_rendimiento * WSun * ang[i])
                else:
                    W.append(0.)
            return W, area_potencia, ang, angulo_giro

    def Calculo_potencia(self, Sun_vector, WSun=1310):
        """
        Calculo_potencia 
        Funcion general para llamar a las distintas funciones para calcular la potencia 

        Args:
            Sun_vector ([type]): [description]
            WSun (int, optional): [description]. Defaults to 1310.

        Returns:
            W (array(,n)) : Potencia generada
            area_potencia (array(,n)) : Areas que generan potencia
            ang (array(,n)) : Angulo de incidencia del vector sol con las caras
            angulo_giro (array(,n)) : Angulo de giro del satelite 
        n : numero de caras
        """
        if self.actitud.control_en_actitud == False:

            index_tri = self.celdas_activas(Sun_vector)
            W, area_potencia, ang = self.power_panel_solar(
                index_tri, Sun_vector, WSun)
            angulo_giro = []
            # Ya que no hay giro pero nos lo piden habra que crearlo
            [angulo_giro.append(np.NaN) for i in len(self.Caras_Despegables)]

        else:

            W, area_potencia, ang, angulo_giro = self.power_panel_con_actitud(
                Sun_vector, WSun)

        return W, area_potencia, ang, angulo_giro

    def apply_transform(self, matrix):
        """
        apply_transform 
        creada para hacer coincidir correctamente las caras
        aplica una transformacion al satelite y reinicia los nombres 

        Args:
            matrix (array(4,4)): matriz de transformacion
        """
        self.mesh = self.mesh.apply_transform(matrix)
        self.name = []
        self.name = self.nombrar_caras()
        self.Normales_caras = np.round(self.mesh.facets_normal)

    def visual(self):
        """
        visual 
        Crea una imagen visual del satelite con unos ejes funciona muy bien en notebook 
        y en linux tambien deberia de poder funcionar

        Returns:
            (scene): retoma una escena con los ejes
        """
        ax = trimesh.creation.axis(axis_radius=25, axis_length=200)
        scene = trimesh.Scene([self.mesh.apply_scale(1), ax])

        return scene.show()

    def separar_satelite(self):
        """
        separar_satelite 
        Separa el satelite en mallas 

        Returns:
            [type]: [description]
        """
        y = np.array(
            np.where(np.isin(self.sombra, self.Caras_Despegables) == False)).flatten()
        despiece = []
        despiece.append(self.mesh.split()[0])
        for i in self.sombra[y]:
            normal = self.mesh.facets_normal[i]
            despiece.append(trimesh.intersections.slice_mesh_plane(self.mesh,
                                                                   self.mesh.facets_normal[i],
                                                                   self.mesh.facets_origin[i]+0.0001*self.mesh.facets_normal[i]))
        return despiece


if __name__ == '__main__':

    filename = '12Unuv.stl'
    actitud = SatelitteActitud(eje_de_spin=[0, 1, 0], control=True)
    d = SatelitteSolarPowerSystem(
        filename, actitud, Despegables_orientables=True)
    d.apply_transform(trimesh.transformations.rotation_matrix(
        np.pi/2, [0, 1, 0], [0, 0, 0]))
    Sun_vector = np.array([-0.10486044,  0.91244007,  0.39554696])
    print(d.mesh.facets_normal)
    W, area_potencia, ang, angulo_giro = d.power_panel_con_actitud(
        Sun_vector, 1)
