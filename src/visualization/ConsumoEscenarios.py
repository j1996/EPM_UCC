# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:58:07 2020

@author: Ignacio García Sánch
"""

""" IMPORTACIONES """

""" Biblioteca Python """
import numpy as np ; import sys
from tkinter import * ; from tkinter import messagebox ; from tkinter import filedialog as fd
import random
import itertools
import matplotlib.pyplot as plt ; from matplotlib.figure import Figure ; """ from matplotlib.backends.backend_pdf import PdfPages """
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg ; """ import matplotlib.animation as anmt """
import os
""" Mis modulos """




"""
    Creacion de la interface grafica
"""

""" Raiz """
raiz = Tk()
raiz.title("Subsistema de Potencia :  Analisis")
raiz.iconbitmap() ; raiz.config(bg="white")


""" Tipografía """
menuBG = "white"
escenBG = "#0084d4" ; escenFontType = "Montserrat" ; escenFontSize = 10 ; escenFontSizeTitle = 11
datosBG = "#0b3772" ; datosFontType = "Montserrat" ; datosFontSize = 10 ; datosFontSizeTitle = 12

botonBG= "#828282" ; entryBG = "#bcbcbc"


""" Frames """
frameEscenarios = Frame(raiz)
frameEscenarios.pack(expand="True",fill="both")
frameEscenarios.config(width="300",height="100",bg=escenBG,relief="groove",bd="10",cursor="hand2")
                       
frameDatos = Frame(raiz)
frameDatos.pack(expand="True",fill="both")
frameDatos.config(width="300",height="100",bg=datosBG,relief="groove",bd="10",cursor="hand2")






"""
    Variables
"""

""" Datos de entrada """
Com_consumo = IntVar()
Act_consumo = IntVar()
Term_consumo = IntVar()

fecha_simulacion = StringVar()
t_simulacion = IntVar()

var_Escen = IntVar()

""" Ajustes de Subsistemas """
Com_pot = StringVar() ; Com_var2 = StringVar()  ; Com_var3 = StringVar() 
Act_pot = StringVar() ; Act_var2 = StringVar() ; Act_var3 = StringVar()
Term_pot  = StringVar() ; Term_var2 = StringVar() ; Term_var3 = StringVar()

with open(os.path.abspath('datos_subsistema.txt'),'r') as data:
    lineas = itertools.islice(data,0,sys.maxsize)
    
    datos_Subsist = [] ; j=0
    for i in lineas:
        if j == 1:
            datos_Subsist.append(i)
            j=0
        else:
            j=1
    
    # Comunicaciones
    Com_pot.set(datos_Subsist[0].strip())      # Puse un .strip() para eliminar unos 
    Com_var2.set(datos_Subsist[1].strip())     #  espacios que me aparecian, y me 
    Com_var3.set(datos_Subsist[2].strip())     #  trastocaban la escritura y lectura
    # Actitud
    Act_pot.set(datos_Subsist[3].strip())      #  del documento .txt
    Act_var2.set(datos_Subsist[4].strip())
    Act_var3.set(datos_Subsist[5].strip())
    # Termico
    Term_pot.set(datos_Subsist[6].strip())
    Term_var2.set(datos_Subsist[7].strip())
    Term_var3.set(datos_Subsist[8].strip())
    # Cierre del archivo
    data.close()

""" Resultados """
consumo_total = 0
consumo_totalxcent = ""

potencia_requerida = StringVar()
potencia_generada = StringVar()

bat_nivel = StringVar()






"""
    Funciones
"""

def escenarios_elec():
    global var_Escen
    
    if var_Escen.get() == 1:
        pass             # Aqui va lo
    elif var_Escen.get() == 2:
        pass             # que hacen
    elif var_Escen.get() == 3:
        pass             # los escenarios


def analisis():
    global Com_consumo,Act_consumo,Term_consumo ; global consumo_total,consumo_totalxcent
    global t_simulacion,fecha_simulacion ; global tiempo_matrix
    global potencia_requerida,potencia_generada,potRequerida_matrix,potGenerada_matrix
    global bat_nivel,batNivel_matrix
    
    """ Array de datos """
    array = np.zeros((1,t_simulacion.get()))
    
    potRequerida_matrix = np.array(array)
    potGenerada_matrix = np.array(array)
    tiempo_matrix = np.array(array)
    
    batNivel_matrix = np.array(array)
    
    """ Simulacion """
    potRequerida = 0 ; potGenerada = 0
    batNivel = "50"  # Nivel de bateria inicial
    
    for i in range(0,t_simulacion.get()):
        Requerida = 2 # Ec. de requerimentos energeticis [w]
        Generada = 0  # Ec. de generacion de potencia [w]
        
        potRequerida_matrix[0,i] = Requerida
        potGenerada_matrix[0,i] = Generada
        tiempo_matrix[0,i] = i
        
        des_carga = random.randint(-10, 10) # Ec. de la carga/descarga de la bateria
        
        batNivel = str(int(batNivel) + des_carga)
        
        batNivel_matrix[0,i]=batNivel
        
        potRequerida = potRequerida + Requerida
        potGenerada = potGenerada + Generada
        
    
    consumo_total = Com_consumo.get() + Act_consumo.get() + Term_consumo.get()
    consumo_totalxcent = (int(consumo_total)/t_simulacion.get())*100
    
    potencia_requerida.set(str(potRequerida))
    potencia_generada.set(str(potGenerada))
    
    bat_nivel.set(str(batNivel))
    

def guardar_resultados():
    with open("Resultados.txt","w") as data:
        pass


varOK = False
def boton_editar():
    global varOK
    
    entryCom.config(state="normal")  ; radiobotonEsc1.config(state="active")
    entryAct.config(state="normal")  ; radiobotonEsc2.config(state="active")
    entryTerm.config(state="normal") ; radiobotonEsc3.config(state="active")
    entryDate.config(state="normal")
    entryTime.config(state="normal")
    
    varOK = False
  
    
def boton_ok():
    global varOK,var_Escen
    
    if var_Escen.get() == 1 or var_Escen.get() == 2 or var_Escen.get() == 3:
        entryCom.config(state="readonly")  ; radiobotonEsc1.config(state="disabled")
        entryAct.config(state="readonly")  ; radiobotonEsc2.config(state="disabled")
        entryTerm.config(state="readonly") ; radiobotonEsc3.config(state="disabled")
        entryDate.config(state="readonly")
        entryTime.config(state="readonly")
        
        varOK = True
    else:
        messagebox.showerror("Fallo en la elección de escenario",
                             "No has elegido ninguno de los escenarios ofrecidos."\
                             "\n\nPor favor, elija escenario y vuelva a intentarlo."\
                             "\n\n                                               Gracias.").geometry("500x500")
        pass


def escen_informacion(escenario):
    if escenario == 1:
        messagebox.showinfo("Escenario 1 : Trabajo Medio",
                            "En este escenario, los satélites estan bajo una carga de trabajo estandar."\
                            "\nEsto quiere decir que el consumo de los equipos se encuentra"\
                            "\nentre el 10 y el 40 %").geometry("900x900")
    elif escenario == 2:
        messagebox.showinfo("Escenario 2 : Alta Carga de Trabajp",
                            "En este escenario, los satélites estan bajo una carga de trabajo alta."\
                            "\nEsto quiere decir que el consumo de los equipos se encuentra"\
                            "\nentre el 50 y el 100 %").geometry("500x500")
    elif escenario == 3:
        messagebox.showinfo("Escenario 3 : Fallo de un satelite",
                            "En este escenario, ... ."\
                            "\nEsto quiere decir que ... ."\
                            "\n... .").geometry("500x500")
 
    
def sist_informacion(subsist):
    global Com_pot,Com_var2,Com_var3
    global Act_pot,Act_var2,Act_var3
    global Term_pot,Term_var2,Term_var3
    global entryBG
    
    if subsist == 1:
        """ Creacion ventana Comunicaciones"""
        ventanaComunicaciones = Toplevel()
        ventanaComunicaciones.title("Datos y ajustes del Subsitema de Comunicaciones")
        ventanaComunicaciones.iconbitmap() ; ventanaComunicaciones.config(bg="white")
        
        """ Tipografía """
        ComunicacionesBG = "#f57cff" ; ComunicacionesFont = "Montserrat"
        
        frameComunicaciones = Frame(ventanaComunicaciones)
        frameComunicaciones.pack(expand="True",fill="both")
        frameComunicaciones.config(width="300",height="100",bg=ComunicacionesBG,relief="groove",bd="10")
        
        EditOK_Com = True
        def  boton_editarCom():
            global EditOK_Com
            
            entryComcons.config(width=20,state="normal",justify="right")
            entryCom2.config(width=20,state="normal",justify="right")
            entryCom3.config(width=20,state="normal",justify="right")
            
            EditOK_Com = False
            
        def boton_okCom():
            global EditOK_Com
            
            entryComcons.config(width=20,state="readonly",justify="right")
            entryCom2.config(width=20,state="readonly",justify="right")
            entryCom3.config(width=20,state="readonly",justify="right")
            
            EditOK_Com = True
        
        def aceptar_Com():
            global EditOK_Com
            
            if EditOK_Com == True:
                ventanaComunicaciones.destroy()
            else:
                messagebox.showerror("Fallo al guardar ajustes",
                             "No has validado los ajustes presionando OK."\
                             "\n\nPor favor, valídelos y vuelva a intentarlo."\
                             "\n\n                                               Gracias.").geometry("500x500")
        
        #--- Datos del Subsistema de Comunicaciones   
        Label(frameComunicaciones,text="Datos y ajustes del Subsistema de Comunicaciones",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=0,column=0,columnspan=4,sticky=W,padx=4,pady=1)
        
        #--- Consumo 
        Label(frameComunicaciones,text="Consumo :",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=1,column=0,sticky=W,padx=10,pady=2) 
        entryComcons = Entry(frameComunicaciones,textvariable=Com_pot) ; entryComcons.grid(row=1,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryComcons.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameComunicaciones,text="[w]",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=1,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameComunicaciones,text="... :",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=2,column=0,sticky=W,padx=10,pady=2) 
        entryCom2 = Entry(frameComunicaciones,textvariable=Com_var2) ; entryCom2.grid(row=2,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryCom2.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameComunicaciones,text="[-]",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=2,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameComunicaciones,text="... :",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=3,column=0,sticky=W,padx=10,pady=2) 
        entryCom3 = Entry(frameComunicaciones,textvariable=Com_var3) ; entryCom3.grid(row=3,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryCom3.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameComunicaciones,text="[-]",bg=ComunicacionesBG,fg="black",font=(ComunicacionesFont, 10)).grid(row=3,column=3,sticky=W,padx=1,pady=2)
              
        #--- Botones "Edit" y "OK" de Comunicaciones
        botonEditCom = Button(frameComunicaciones,text="Edit",command=lambda:boton_editarCom(),bg=botonBG) ; botonEditCom.grid(row=8,column=1)
        botonOKCom = Button(frameComunicaciones,text="OK",command=lambda:boton_okCom(),bg=botonBG) ; botonOKCom.grid(row=8,column=2)
        
        #--- Boton "Aceptar" que cierra y guardas los ajustes
        botonAceptCom = Button(frameComunicaciones,text="Aceptar",command=lambda:aceptar_Com(),bg=botonBG,width=10,height=2) ; botonAceptCom.grid(row=10,column=10,padx=4,pady=4)
                                   
    elif subsist == 2:
        """ Creacion ventana Actitud"""
        ventanaActitud = Toplevel()
        ventanaActitud.title("Datos y ajustes del Subsitema de Actitud")
        ventanaActitud.iconbitmap() ; ventanaActitud.config(bg="white")
        
        """ Tipografía """
        ActitudBG = "#f57cff" ; ActitudFont = "Montserrat"
        
        frameActitud = Frame(ventanaActitud)
        frameActitud.pack(expand="True",fill="both")
        frameActitud.config(width="300",height="100",bg=ActitudBG,relief="groove",bd="10")
        
        EditOK_Act = True
        def  boton_editarAct():
            global EditOK_Act
            
            entryActcons.config(width=20,state="normal",justify="right")
            entryAct2.config(width=20,state="normal",justify="right")
            entryAct3.config(width=20,state="normal",justify="right")
            
            EditOK_Act = False
            
        def boton_okAct():
            global EditOK_Act
            
            entryActcons.config(width=20,state="readonly",justify="right")
            entryAct2.config(width=20,state="readonly",justify="right")
            entryAct3.config(width=20,state="readonly",justify="right")
        
            EditOK_Act = True
            
        def aceptar_Act():
            global EditOK_Act
            
            if EditOK_Act == True:
                ventanaActitud.destroy()
            else:
                messagebox.showerror("Fallo al guardar ajustes",
                             "No has validado los ajustes presionando OK."\
                             "\n\nPor favor, valídelos y vuelva a intentarlo."\
                             "\n\n                                               Gracias.").geometry("500x500")
        
        #--- Datos del Subsistema de Actitud   
        Label(frameActitud,text="Datos y ajustes del Subsistema de Actitud",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=0,column=0,columnspan=4,sticky=W,padx=4,pady=1)
        
        #--- Consumo 
        Label(frameActitud,text="Consumo :",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=1,column=0,sticky=W,padx=10,pady=2) 
        entryActcons = Entry(frameActitud,textvariable=Act_pot) ; entryActcons.grid(row=1,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryActcons.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameActitud,text="[w]",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=1,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameActitud,text="... :",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=2,column=0,sticky=W,padx=10,pady=2) 
        entryAct2 = Entry(frameActitud,textvariable=Act_var2) ; entryAct2.grid(row=2,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryAct2.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameActitud,text="[-]",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=2,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameActitud,text="... :",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=3,column=0,sticky=W,padx=10,pady=2) 
        entryAct3 = Entry(frameActitud,textvariable=Act_var3) ; entryAct3.grid(row=3,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryAct3.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameActitud,text="[-]",bg=ActitudBG,fg="black",font=(ActitudFont, 10)).grid(row=3,column=3,sticky=W,padx=1,pady=2)
              
        #--- Botones "Edit" y "OK" de Comunicaciones
        botonEditAct = Button(frameActitud,text="Edit",command=lambda:boton_editarAct(),bg=botonBG) ; botonEditAct.grid(row=8,column=1)
        botonOKAct = Button(frameActitud,text="OK",command=lambda:boton_okAct(),bg=botonBG) ; botonOKAct.grid(row=8,column=2)
        
        #--- Boton "Start" que empieza el analisis
        botonAceptAct = Button(frameActitud,text="Aceptar",command=lambda:aceptar_Act(),bg=botonBG,width=10,height=2) ; botonAceptAct.grid(row=10,column=10,padx=4,pady=4)


    elif subsist == 3:
        """ Creacion ventana Térmico"""
        ventanaTermico = Toplevel()
        ventanaTermico.title("Datos y ajustes del Subsitema Termico")
        ventanaTermico.iconbitmap() ; ventanaTermico.config(bg="white")
        
        """ Tipografía """
        TermicoBG = "#f57cff" ; TermicoFont = "Montserrat"
        
        frameTermico = Frame(ventanaTermico)
        frameTermico.pack(expand="True",fill="both")
        frameTermico.config(width="300",height="100",bg=TermicoBG,relief="groove",bd="10")
        
        EditOK_Term = True
        def  boton_editarTerm():
            global EditOK_Term
            
            entryTermcons.config(width=20,state="normal",justify="right")
            entryTerm2.config(width=20,state="normal",justify="right")
            entryTerm3.config(width=20,state="normal",justify="right")
            
            EditOK_Term = False
            
        def boton_okTerm():
            global EditOK_Term
            
            entryTermcons.config(width=20,state="readonly",justify="right")
            entryTerm2.config(width=20,state="readonly",justify="right")
            entryTerm3.config(width=20,state="readonly",justify="right")
            
            EditOK_Term = True
        
        def aceptar_Term():
            global EditOK_Term
            
            if EditOK_Term == True:
                ventanaTermico.destroy()
            else:
                messagebox.showerror("Fallo al guardar ajustes",
                             "No has validado los ajustes presionando OK."\
                             "\n\nPor favor, valídelos y vuelva a intentarlo."\
                             "\n\n                                               Gracias.").geometry("500x500")
                
        
        #--- Datos del Subsistema Termico   
        Label(frameTermico,text="Datos y ajustes del Subsistema Térmico",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=0,column=0,columnspan=4,sticky=W,padx=4,pady=1)
        
        #--- Consumo 
        Label(frameTermico,text="Consumo :",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=1,column=0,sticky=W,padx=10,pady=2) 
        entryTermcons = Entry(frameTermico,textvariable=Term_pot) ; entryTermcons.grid(row=1,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryTermcons.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameTermico,text="[w]",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=1,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameTermico,text="... :",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=2,column=0,sticky=W,padx=10,pady=2) 
        entryTerm2 = Entry(frameTermico,textvariable=Term_var2) ; entryTerm2.grid(row=2,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryTerm2.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameTermico,text="[-]",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=2,column=3,sticky=W,padx=1,pady=2)
              
        #---  - 
        Label(frameTermico,text="... :",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=3,column=0,sticky=W,padx=10,pady=2) 
        entryTerm3 = Entry(frameTermico,textvariable=Term_var3) ; entryTerm3.grid(row=3,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryTerm3.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameTermico,text="[-]",bg=TermicoBG,fg="black",font=(TermicoFont, 10)).grid(row=3,column=3,sticky=W,padx=1,pady=2)
              
        #--- Botones "Edit" y "OK" de Comunicaciones
        botonEditTerm = Button(frameTermico,text="Edit",command=lambda:boton_editarTerm(),bg=botonBG) ; botonEditTerm.grid(row=8,column=1)
        botonOKTerm = Button(frameTermico,text="OK",command=lambda:boton_okTerm(),bg=botonBG) ; botonOKTerm.grid(row=8,column=2)
        
        #--- Boton "Start" que empieza el analisis
        botonAceptTerm = Button(frameTermico,text="Aceptar",command=lambda:aceptar_Term(),bg=botonBG,width=10,height=2) ; botonAceptTerm.grid(row=10,column=10,padx=4,pady=4)

    """ Ajustes de Subsistemas """
    with open("Datos_Subsistemas.txt","w") as data:
        # Comunicaciones
        data.write("{}\n".format("Consumo de Comunicaciones :")) ; data.write("{}\n".format(Com_pot.get()))
        data.write("{}\n".format("Var2 de Comunicaciones :")) ; data.write("{}\n".format(Com_var2.get()))
        data.write("{}\n".format("Var3 de Comunicaciones :")) ; data.write("{}\n".format(Com_var3.get()))
        # Actitud
        data.write("{}\n".format("Consumo de Actitud :")) ; data.write("{}\n".format(Act_pot.get()))
        data.write("{}\n".format("Var2 de Actitud :")) ; data.write("{}\n".format(Act_var2.get()))
        data.write("{}\n".format("Var3 de Actitud :")) ; data.write("{}\n".format(Act_var3.get()))
        # Termico
        data.write("{}\n".format("Consumo de Térmico :")) ; data.write("{}\n".format(Term_pot.get()))
        data.write("{}\n".format("Var2 de Térmico :")) ; data.write("{}\n".format(Term_var2.get()))
        data.write("{}\n".format("Var3 de Térmico :")) ; data.write("{}".format(Term_var3.get()))
        # Cierre del archivo
        data.close()


def ayuda_informacion():
     messagebox.showinfo("Subsistema de Potencia: Información del código de análisis",
                         "Código para el análisis del consumo de potencia."\
                         "\n\nWritten by Ignacio García Sánchez."\
                         "\n\n     Contact :  ignacio.garciasanchez@altran.com").geometry("500x500")


def ventana_resultados():
    global varOK
    global entryBG,menuBG
    global potRequerida_matrix,potGenerada_matrix,batNivel_matrix
    global tiempo_matrix
    
    escenarios_elec()
    
    if varOK == True:
        """ Creacion segunda ventana """
        ventanaResultados = Toplevel()
        ventanaResultados.title("Subsistema de Potencia: Resultados")
        ventanaResultados.iconbitmap() ; ventanaResultados.config(bg="white")
        
        """ Tipografía """
        resultadosBG = "#3eff5b" ; resultadosFont = "Montserrat"
        
        frameResultados = Frame(ventanaResultados)
        frameResultados.pack(expand="True",fill="both")
        frameResultados.config(width="300",height="100",bg="#3eff5b",relief="groove",bd="10")
        
        """ Analisis """
        analisis()
        
        """ Funciones """
        def plt_graficas(elec):
            global menuBG ; global resultadosFont
            global potRequerida_matrix,potGenerada_matrix
            global batNivel_matrix ; global tiempo_matrix
            global grafica,n_gf,ejeX,ejeY
            
            if elec == 1:
                grafica = "Potencia" ; n_gf = 2 ; 
                
                ejeX = np.array((potRequerida_matrix[0,:],potGenerada_matrix[0,:]))
                ejeY = tiempo_matrix
                
            elif elec == 2:
                grafica = ""
                
            elif elec == 3:
                grafica = "Nivel de batería" ; n_gf = 1 ;
                
                ejeX = batNivel_matrix
                ejeY = tiempo_matrix        
            
            """ Ventana de graficas """
            grafTitle = ("{}").format(grafica)
            ventanaGrafica = Toplevel() ; ventanaGrafica.title(grafTitle)
            ventanaGrafica.iconbitmap() ; ventanaGrafica.config(bg="white")
            
            frameGrafica = Frame(ventanaGrafica) ; frameGrafica.pack(expand="True",fill="both")
            frameGrafica.config(width="300",height="100",bg="#3eff5b",relief="groove",bd="10")
            
            """ Ploteo """
            f = Figure(figsize=(9,6),dpi=80 )
            ax0 = f.add_axes((0.25, .25, .50, .50),frameon=False)
            
            clor = ("b","r","g","y","k")
            for i in range(0,n_gf):
                ax0.plot(ejeY[0,:],ejeX[i,:],color=clor[i])
                
            canvas = FigureCanvasTkAgg(f,master=frameGrafica) ; canvas.get_tk_widget().pack()
            
            """ Funcion guardar """
            def guardar_grafica(como):
                global grafica,n_gf,ejeX,ejeY
                
                if como == 1:
                    f = Figure(figsize=(9,6),dpi=80 )
                    ax0 = f.add_axes((0.25, .25, .50, .50),frameon=False)
                    
                    clor = ("b","r","g","y","k")
                    for i in range(0,n_gf):
                        ax0.plot(ejeY[0,:],ejeX[i,:],color=clor[i])
                    saveTitle = "{}.jpg".format(grafica)
                    f.savefig(saveTitle)
                    
                elif como == 2:
                    f = Figure(figsize=(9,6),dpi=80 )
                    ax0 = f.add_axes((0.25, .25, .50, .50),frameon=False)
                    
                    clor = ("b","r","g","y","k")
                    for i in range(0,n_gf):
                        ax0.plot(ejeY[0,:],ejeX[i,:],color=clor[i])
                    saveTitle = "{}.png".format(grafica)
                    f.savefig(saveTitle)
                    
                elif como == 3:
                    f = Figure(figsize=(9,6),dpi=80 )
                    ax0 = f.add_axes((0.25, .25, .50, .50),frameon=False)
                    
                    clor = ("b","r","g","y","k")
                    for i in range(0,n_gf):
                        ax0.plot(ejeY[0,:],ejeX[i,:],color=clor[i])
                    saveTitle = "{}.PDF".format(grafica)
                    f.savefig(saveTitle)
                
                """ Mensaje de guardado """
                messagebox.showinfo("Guardar",
                         "Gráfica guardada con éxito."\
                         "\n\nEl documento ha sido guardado con el nombre de:"\
                         "\n     {}".format(saveTitle)).geometry("500x500")
                    
                    
            
            """ Menu guardar """
            graficaMenu = Menu(ventanaGrafica) ; ventanaGrafica.config(menu=graficaMenu,width=100,height=100)
            guardarMenu = Menu(graficaMenu,tearoff=0,bg=menuBG) ; graficaMenu.add_cascade(label="Guardar como...",menu=guardarMenu)
            guardarMenu.add_command(label="Guardar como JPG",command=lambda:guardar_grafica(1))
            guardarMenu.add_command(label="Guardar como PNG",command=lambda:guardar_grafica(2))
            guardarMenu.add_command(label="Guardar como PDF",command=lambda:guardar_grafica(3))
        
        def guardar():
            with open("Resultados.txt","w") as data:
                pass
            
            
        """ Menu """

        resultadosMenu = Menu(ventanaResultados) ; ventanaResultados.config(menu=resultadosMenu,width=300,height=300)

        graficasMenu = Menu(resultadosMenu,tearoff=0,bg=menuBG) ; resultadosMenu.add_cascade(label="Graficas",menu=graficasMenu)
        graficasMenu.add_command(label="Consumo",command=lambda:plt_graficas(1))
        graficasMenu.add_command(label=" ... ",command=lambda:plt_graficas(2))
        graficasMenu.add_command(label=" ... ",command=lambda:plt_graficas(3))
        
        """ Pantalla 2 : Tabla de resultados """
        #--- Datos de entrada de Consumo de los subsistemas indicado mediante el tiempo de uso durante el tiempo total de simulacion  
        Label(frameResultados,text="Resultados del Consumo de los Subsistemas",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=0,column=0,columnspan=4,sticky=W,padx=4,pady=1)
              
        #--- Consumo 
        Label(frameResultados,text="Consumo total :",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=1,column=0,sticky=W,padx=10,pady=2) 
        entryConsTotal = Entry(frameResultados,textvariable=potencia_requerida) ; entryConsTotal.grid(row=1,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryConsTotal.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameResultados,text="[w]",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=1,column=3,sticky=W,padx=1,pady=2)
    
        #--- Generacion 
        Label(frameResultados,text="Generacion total :",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=2,column=0,sticky=W,padx=10,pady=2) 
        entryGener = Entry(frameResultados,textvariable=potencia_generada) ; entryGener.grid(row=2,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryGener.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameResultados,text="[w]",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=2,column=3,sticky=W,padx=1,pady=2)
        
        #--- Bateria 
        Label(frameResultados,text="Nivel de Bateria :",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=3,column=0,sticky=W,padx=10,pady=2) 
        entryNivelBat = Entry(frameResultados,textvariable=bat_nivel) ; entryNivelBat.grid(row=3,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryNivelBat.config(width=20,state="readonly",justify="right",bg=entryBG)
        Label(frameResultados,text="[%]",bg=resultadosBG,fg="black",font=(resultadosFont, 10)).grid(row=3,column=3,sticky=W,padx=1,pady=2)
    
        
        ventanaResultados.mainloop()
        
    else:
        messagebox.showerror("Confirmacion de datos de esntrada",
                             "No has confirmado los datos de entrada para el análisis."\
                             "\n\nPor favor, confirmelos pulsando OK y vuelva a intentarlo."\
                             "\n\n                                               Gracias.").geometry("500x500")
        pass








"""
    Pantalla
"""

""" Menu """

barraMenu = Menu(raiz) ; raiz.config(menu=barraMenu,width=300,height=300)

subsistemasMenu = Menu(barraMenu,tearoff=0,bg=menuBG) ; barraMenu.add_cascade(label="Subsistemas",menu=subsistemasMenu)
subsistemasMenu.add_command(label="Sist. Comunicaciones",command=lambda:sist_informacion(1))
subsistemasMenu.add_command(label="Sist. Actitud",command=lambda:sist_informacion(2))
subsistemasMenu.add_command(label="Sist. Termico",command=lambda:sist_informacion(3))
#subsistemasMenu.add_separator()

escenariosMenu = Menu(barraMenu,tearoff=0,bg=menuBG) ; barraMenu.add_cascade(label="Escenarios",menu=escenariosMenu)
escenariosMenu.add_command(label="Escenario 1",command=lambda:escen_informacion(1))
escenariosMenu.add_command(label="Escenario 2",command=lambda:escen_informacion(2))
escenariosMenu.add_command(label="Escenario 3",command=lambda:escen_informacion(3))

resultadosMenu = Menu(barraMenu,tearoff=0,bg=menuBG) ; barraMenu.add_cascade(label="Resultados",menu=resultadosMenu)
resultadosMenu.add_command(label="Guardar",command=lambda:guardar_resultados())

ayudaMenu = Menu(barraMenu,tearoff=0,bg=menuBG) ; barraMenu.add_cascade(label="Ayuda",menu=ayudaMenu)
ayudaMenu.add_command(label="Acerca de...",command=lambda:ayuda_informacion())


""" Pantalla 1.1 : Escenarios """

#--- Eleccion de escenarios  
Label(frameEscenarios,text="Elección de escenarios: ",bg=escenBG,fg="black",font=(escenFontType,escenFontSizeTitle,"bold")).grid(row=0,column=0,columnspan=3,sticky=W,padx=4,pady=1)

radiobotonEsc1 = Radiobutton(frameEscenarios,text="Escenario 1",variable=var_Escen,value=1) ; radiobotonEsc1.grid(row=1,column=0,padx=4,pady=1) ; radiobotonEsc1.config(bg=escenBG,fg="black",font=(escenFontType,escenFontSize))
radiobotonEsc2 = Radiobutton(frameEscenarios,text="Escenario 2",variable=var_Escen,value=2) ; radiobotonEsc2.grid(row=1,column=1,padx=4,pady=1) ; radiobotonEsc2.config(bg=escenBG,fg="black",font=(escenFontType,escenFontSize))
radiobotonEsc3 = Radiobutton(frameEscenarios,text="Escenario 3",variable=var_Escen,value=3) ; radiobotonEsc3.grid(row=1,column=2,padx=4,pady=1) ; radiobotonEsc3.config(bg=escenBG,fg="black",font=(escenFontType,escenFontSize))

""" Pantalla 1.2 : Introduccion de datos """

#--- Datos de entrada de Consumo de los subsistemas indicado mediante el tiempo de uso durante el tiempo total de simulacion  
Label(frameDatos,text="Datos de entrada de Consumo de los Subsistemas",bg=datosBG,fg="white",font=(datosFontType,datosFontSizeTitle,"bold")).grid(row=0,column=0,columnspan=4,sticky=W,padx=4,pady=1)
Label(frameDatos,text="( indicado mediante el tiempo de uso durante el tiempo total de simulacion )",bg="#0b3772",fg="white",font=(datosFontType, 8)).grid(row=1,column=0,columnspan=4,sticky=W,padx=4)
      
#--- Consumo Comunicaciones
Label(frameDatos,text="Sist Comunicaciones :",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=2,column=0,sticky=W,padx=10,pady=2) 
entryCom = Entry(frameDatos,textvariable=Com_consumo) ; entryCom.grid(row=2,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryCom.config(width=20,state="normal",justify="right",bg=entryBG)
Label(frameDatos,text="[s]",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=2,column=3,sticky=W,padx=1,pady=2)

#--- Consumo Actitud
Label(frameDatos,text="Sist Actitud :",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=3,column=0,sticky=W,padx=10,pady=2)
entryAct = Entry(frameDatos,textvariable=Act_consumo) ; entryAct.grid(row=3,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryAct.config(width=20,state="normal",justify="right",bg=entryBG)
Label(frameDatos,text="[s]",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=3,column=3,sticky=W,padx=1,pady=2)

#--- Consumo Termico
Label(frameDatos,text="Sist Térmico :",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=4,column=0,sticky=W,padx=10,pady=2)
entryTerm = Entry(frameDatos,textvariable=Term_consumo) ; entryTerm.grid(row=4,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryTerm.config(width=20,state="normal",justify="right",bg=entryBG)
Label(frameDatos,text="[s]",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=4,column=3,sticky=W,padx=1,pady=2)

#--- Datos de entrada de la simulacion
Label(frameDatos,text="Datos de entrada de la simulacion",bg=datosBG,fg="white",font=(datosFontType,datosFontSizeTitle,"bold")).grid(row=5,column=0,columnspan=4,sticky="W",padx=4,pady=4)

#--- Fecha de inicio de simlacion
Label(frameDatos,text="Fecha de inicio de simulación :",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=6,column=0,sticky=W,padx=10,pady=2)
entryDate = Entry(frameDatos,textvariable=fecha_simulacion) ; entryDate.grid(row=6,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryDate.config(width=20,state="normal",justify="right",bg="#bcbcbc")
Label(frameDatos,text="[dd/mm/aaaa]",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=6,column=3,sticky=W,padx=1,pady=2)

#--- Tiempo total de simlacion
Label(frameDatos,text="Tiempo total de simulación :",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=7,column=0,sticky=W,padx=10,pady=2)
entryTime = Entry(frameDatos,textvariable=t_simulacion) ; entryTime.grid(row=7,column=1,columnspan=2,sticky=E,padx=1,pady=2) ; entryTime.config(width=20,state="normal",justify="right",bg="#bcbcbc")
Label(frameDatos,text="[s]",bg=datosBG,fg="white",font=(datosFontType,datosFontSize)).grid(row=7,column=3,sticky=W,padx=1,pady=2)
      
#--- Botones "Edit" y "OK"
botonEdit = Button(frameDatos,text="Edit",command=lambda:boton_editar(),bg=botonBG) ; botonEdit.grid(row=8,column=1)
botonOK = Button(frameDatos,text="OK",command=lambda:boton_ok(),bg=botonBG) ; botonOK.grid(row=8,column=2)

                 
#--- Boton "Start" que empieza el analisis
botonStart = Button(frameDatos,text="Start",command=lambda:ventana_resultados(),bg=botonBG,width=10,height=2) ; botonStart.grid(row=10,column=10,padx=4,pady=4)






#
#
#
#
#
raiz.mainloop()