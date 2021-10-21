"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    sortByBD(catalog)
    SortByDA(catalog)


def loadArtworks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'MoMA/Artworks-utf8-5pct.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)

def loadArtists(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'MoMA/Artists-utf8-5pct.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

# Funciones de ordenamiento

def sortByBD(catalog):
    return model.sortByBD(catalog)
def SortByDA(catalog):
    return model.sortByDA(catalog)

# Funciones de consulta sobre el catálogo
def ArtistsByBD(catalog, date0, dateF):
    list = model.ArtistsByBD(catalog, date0, dateF)
    return model.sortArtistsBD(list)
def ArtworksByDA(catalog, date0, dateF):
    return model.ArtworksByDA(catalog, date0, dateF)
def ArtworksByMedium(catalog, medio):
    r = model.getArtworksByMedium(catalog, medio)
    return SortByDate(r)
def Nationalities(catalog):
    model.addArtworkNationality(catalog)
    return model.SortNationalities(catalog)
def getArtistIdByName(catalog, artistName):
    return model.getArtistIdByName(catalog, artistName)
def countArtworksByArtist(catalog, artistId):
    return model.countArtworksByArtist(catalog, artistId)
def getArtworksByTecnique(catalog, artistId, tecnique):
    return model.getArtworksByTecnique(catalog, artistId, tecnique)
def sortBiggestN(list):
    return model.sortNlist(list)
def sortName(list):
    return model.SortName(list)

def CostDepa(catalog, depa):
    return model.CostDepa(catalog, depa)
def sortD(list):
    return model.sortArtWorksD(list)
def sortCost(list):
    return model.sortArtWorksCost(list)