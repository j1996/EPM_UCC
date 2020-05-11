import numpy as np
import trimesh


class SatelitteActitud(object):
    def __init__(self, eje_de_spin, control):
        self.control_en_actitud = control
        self.eje_de_spin = eje_de_spin
        self.apuntando_a_tierra = True
        self.apuntado_sol = True
        self.apuntado_constante_sol = True

    def Apuntar_Sol(self, Sun_vector, Cara_principal):

        direcion_principal = self.mesh.facets_normal[self.Caras_Despegables[0]]
        plano0 = np.cross(Sun_vector, self.actitud.eje_de_spin)
        plano0 = plano0/np.linalg.norm(plano0)

        plano1 = np.cross(direcion_principal, self.actitud.eje_de_spin)

        plano1 = plano1/np.linalg.norm(plano1)

        angulo_giro = np.arccos(np.absolute(
            np.dot(plano0, plano1)))/(np.linalg.norm(plano0)*np.linalg.norm(plano1))
        posicion_eje = np.array(np.where(self.eje_de_spin == 1)).max()
        if plano0(posicion_eje) == 0:
            angulo_giro = 0.0
        elif np.isnan(angulo_giro):
            angulo_giro = 0.0

        if angulo_giro == 0:
            pass
        else:
            prim = trimesh.transform_points(plano1.reshape(1, 3), trimesh.transformations.rotation_matrix(
                angulo_giro, self.actitud.eje_de_spin, [0, 0, 0]))
            if not np.allclose(prim, plano0):
                angulo_giro = -angulo_giro
            self.mesh = self.mesh.apply_transform(trimesh.transformations.rotation_matrix(
                angulo_giro, self.actitud.eje_de_spin, [0, 0, 0]))
