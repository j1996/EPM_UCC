class SatelitteActitud(object):
    def __init__(self,eje_de_spin, control):
        self.control_en_actitud=control
        self.eje_de_spin=eje_de_spin
        self.apuntando_a_tierra=True