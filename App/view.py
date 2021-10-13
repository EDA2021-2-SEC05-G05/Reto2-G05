"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Obras más antiguas para un medio específico")
    print("3- Nacionalidades por cantidad de obras")

def printArtworksbyMedium(artworks, n):
    if(artworks):
        print('Se encontraron: ' + str(lt.size(artworks)) + ' Libros')
        print("\n")
        i = 1
        while i <= n:
            artwork = lt.getElement(artworks, i)
            print(artwork['Title']+" | "+artwork["Date"])
            i +=1
    else:
        print("No se encontraron libros.\n")

def printNResults(nat):
    for n in lt.iterator(nat):
        print("Nacionalidad: ", n["Nationality"], "| Cantidad de obras: ", lt.size(n["artworks"]), "\n")

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadData(catalog)
    elif int(inputs[0]) == 2:
        start_time = time.process_time()
        medio = input("Ingrese el medio que desea consultar: ")
        n = input("Ingrese el número de obras que desea ver: ")
        r = controller.ArtworksByMedium(catalog, medio)
        printArtworksbyMedium(r, int(n))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        print("Cargando... ")
        nat = controller.Nationalities(catalog)
        printNResults(nat)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    else:
        sys.exit(0)
sys.exit(0)
