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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'artworks': None,
               "medium": None,}
    catalog['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksIds)
    catalog["medium"] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMedium)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog['artworks'], artwork)
    addArtworkMedium(catalog, artwork)

def addArtworkMedium(catalog, artwork):
    mediums = catalog["medium"]
    if (artwork['Medium'] != ''):
        med = artwork["Medium"]
    else:
        med = "Unknown"
    existmed = mp.contains(mediums, med)
    if existmed:
        entry = mp.get(mediums, med)
        m = me.getValue(entry)
    else:
        m = newMedium(med)
        mp.put(mediums, med, m)
    lt.addLast(m['artworks'], artwork)

def newMedium(med):
    entry = {'Medium': "", "artworks": None}
    entry['Medium'] = med
    entry['artworks'] = lt.newList('SINGLE_LINKED', compareMedium)
    return entry
# Funciones para creacion de datos

# Funciones de consulta

def getArtworksByYear(catalog, medio):
    medio = mp.get(catalog['medium'], medio)
    if medio:
        return me.getValue(medio)['artworks']
    return None

# Funciones utilizadas para comparar elementos dentro de una lista
def compareArtworksIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
def compareMedium(keyM, medium):
    authentry = me.getKey(medium)
    if (keyM == authentry):
        return 0
    elif (keyM > authentry):
        return 1
    else:
        return -1
# Funciones de ordenamiento
def SortByDate(list):
    return sa.sort(list, cmpArtworkByDate)
def cmpArtworkByDate(artwork1, artwork2):
    return (artwork1["Date"]<artwork2["Date"])