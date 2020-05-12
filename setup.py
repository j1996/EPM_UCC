from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.5',
    description='Analisis de la potencia generada en un cubesat donde la superficie es limitada, calculando la sombra que se puede producir, incluyendo la posicion del satelite',
    url = 'https://github.com/j1996/EPM_UCC',
    author='Javier Martinez Martinez @Altran',
    author_email='javi.mtnez.mtnez@gmail.com',
    license='MIT',
    install_requires=['trimesh','poliastro','astropy'],
)
