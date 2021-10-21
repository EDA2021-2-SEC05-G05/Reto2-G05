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
    print("2- Artistas cronológicamente")
    print("3- Adquisiciones cronológicamente")
    print("4- Clasificar obras de un artista por técnica")
    print("5- Nacionalidades por cantidad de obras")
    print("0- Salir")

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
def printArtists(list):
    size = lt.size(list)
    pri = 1
    while pri<=3:
        l = lt.getElement(list, pri)
        print("Nombre: ", l["DisplayName"], " | Año de nacimiento: " ,l["BeginDate"], " | Año de fallecimiento: ",l["EndDate"], " | Nacionalidad: ", l["Nationality"], " | Genero: ", l["Gender"], "\n" )
        pri+=1
    print("-\n"*3)
    ult = 2
    while ult>=0:
        l = lt.getElement(list, int(size)-ult)
        print("Nombre: ", l["DisplayName"], " | Año de nacimiento: " ,l["BeginDate"], " | Año de fallecimiento: ",l["EndDate"], " | Nacionalidad: ", l["Nationality"], " | Genero: ", l["Gender"], "\n" )
        ult-=1

def printNResults(nat):
    #for n in lt.iterator(nat):
        #print("Nacionalidad: ", n["Nationality"], "| Cantidad de obras: ", lt.size(n["artworks"]), "\n")
    i = 1
    while i <= 10:
        n = lt.getElement(nat, i)
        print("Nacionalidad: ", n["Nationality"], "| Cantidad de obras: ", lt.size(n["artworks"]), "\n")
        i+=1
    a = lt.getElement(nat, 1)
    Results3(a["artworks"])

def Results3Artworks(list):
    i = 0
    while i<=2:
        print("Título: ", list[i]["Title"], " | Fecha de la obra: ",list[i]["Date"], " | Medio: ", list[i]["Medium"], " | Dimensiones: ", list[i]["Dimensions"], "\n" )
        i+=1
    j = 1
    while j<=3:
        print("Título: ", list[-j]["Title"], " | Fecha de la obra: ",list[-j]["Date"], " | Medio: ", list[-j]["Medium"], " | Dimensiones: ", list[-j]["Dimensions"], "\n" )
        j+=1


def Results3(list):
    size = lt.size(list)
    pri = 0
    i = 1
    while i<=size:
        l = lt.getElement(list, i)
        next = lt.getElement(list, i+1)
        artists = ""
        if l == next:
            i+=1
        else:
            for artist in lt.iterator(l["AWartists"]):
                artists = artists + artist["DisplayName"]+ ", "
            print("Título: ", l["Title"], " | Artista(s): " ,artists[:-2], " | Fecha de la obra: ",l["Date"], "| Fecha de adquisición: ", l["DateAcquired"], "| Medio: ", l["Medium"], " | Dimensiones: ", l["Dimensions"], "\n" )
            pri+=1
            i+=1
            if pri ==3:
                break
    print("-\n"*3)
    ult = 0
    n = 0
    last = lt.newList()
    while n<=size:
        l = lt.getElement(list, size-n)
        next = lt.getElement(list, size-(n+1))
        if l == next:
            n+=1
        else:
            lt.addFirst(last, l)
            ult+=1
            n+=1
            if ult ==3:
                for artwork in lt.iterator(last):
                    artists = ""
                    for artist in lt.iterator(artwork["AWartists"]):
                        artists = artists + artist["DisplayName"]+ ", "
                    print ("Título: ", artwork["Title"], " | Artista(s): " ,artists[:-2], " | Fecha de la obra: ",artwork["Date"], "| Fecha de adquisición: ", l["DateAcquired"], " | Medio: ", artwork["Medium"], " | Dimensiones: ", artwork["Dimensions"], "\n")
                break


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
        date0 = input("Ingrese la fecha inicial en formato YYYY: ")
        dateF = input("Ingrese la fecha final en formato YYYY: ")
        list = controller.ArtistsByBD(catalog, date0, dateF)
        printArtists(list)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        date0 = input("Ingrese la fecha inicial en formato YYYY-MM-DD: ")
        dateF = input("Ingrese la fecha final en formato YYYY-MM-DD: ")
        r = controller.ArtworksByDA(catalog, date0, dateF)
        print("El número de obras compradas es de :", r[1])
        #sort = controller.sortDA(r[0])
        Results3(r[0])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 4:
        start_time = time.process_time()
        print("Cargando... ")
        artistName = input("Ingrese el nombre del Artista: ")
        #artistName = 'Louise Bourgeois'
        id = controller.getArtistIdByName(catalog, artistName)
        count = controller.countArtworksByArtist(catalog, id)[0]
        print("{name} with MoMA {id} has {count} pieces in his/her name at the museum.".format(name = artistName, id = id, count = count))
        tecniques = controller.countArtworksByArtist(catalog, id)[1]
        print("There are {tecniques} different mediums/techniques in his/her work.".format(tecniques = tecniques))
        most_tecnique = controller.countArtworksByArtist(catalog, id)[2]
        count_most_tecnique = controller.countArtworksByArtist(catalog, id)[3]
        print("Her/His most used Medium/Technique is: {most_tecnique} with {count_most_tecnique} pieces.".format(most_tecnique = most_tecnique, count_most_tecnique=count_most_tecnique))
        artworks = controller.getArtworksByTecnique(catalog, id, most_tecnique)
        print("A sample of 3 {most_tecnique} from the collection are:".format(most_tecnique=most_tecnique))
        Results3Artworks(artworks)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
    elif int(inputs[0]) == 5:
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
