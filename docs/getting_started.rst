===============
 Getting Started 
===============

El codigo esta optimizado para que funcione en linux(50 veces mas rapido que en windows),
para ello el metodo mas sencillo es instalar WSL en windows y utilizarlo con Visual Studio Code

    -https://pbpython.com/wsl-python.html

Hay va un link que os explicara como hacerlo todo 

Instalacion
++++++++++++++++

He incluido dos ficheros:
    - requirements.txt
    - environment.yml 
ambos sirven para crear un environment con conda o con pip con los archivos 
necesarios para que funcione (y alguno mas, no hice limpieza sorry)
 
Si quieres utilizar el primero
.. code-block:: python
    pip install -r requirements.txt

ó

.. code-block:: python
    conda install -r requirements.txt

para el environment.yml 
.. code-block:: python
    conda env create -f environment.yml

Uso 
++++++++++++++++
Para utilizar el modelo es bastante facil solo es necesario el uso de *SatelliteV4.py* 
todos lo necesario esta explicado en el archivo tambien esta inlcuido el visual.ypnb que permite
ver la imagen del satelite CAD con los ejes.
