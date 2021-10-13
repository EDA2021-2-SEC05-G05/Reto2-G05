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
from DISClib.Algorithms.Sorting import mergesort as mr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'artworks': None,
               "medium": None,
               "nationalities": None}
    catalog['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksIds)
    catalog['artists'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareIds)
    catalog["medium"] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMedium)
    catalog["nationalities"] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareNationality)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    addArtworkMedium(catalog, artwork)
    artwork = addArtists(catalog, artwork)
    lt.addLast(catalog['artworks'], artwork)
    
    

def addArtist(catalog, artist):
    id = artist["ConstituentID"]
    mp.put(catalog['artists'], id, artist)


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

def addArtists(catalog, artwork):
    artwork["AWartists"] = lt.newList()
    artistsID = artwork['ConstituentID'][1:-1]
    artistsID = artistsID.split(",")
    for artistID in artistsID:
        id = artistID.strip()
        artist = mp.get(catalog["artists"], id)
        v = me.getValue(artist)
        lt.addLast(artwork["AWartists"], v)
    return artwork

def Nationalities(catalog):
    artworks = catalog["artworks"]
    for artwork in lt.iterator(artworks):
        for artist in lt.iterator(artwork["AWartists"]):
            n = artist["Nationality"]
            if n == "":
                n = "Unknown"
            existn = mp.contains(catalog["nationalities"], n)
            if existn:
                entry = mp.get(catalog["nationalities"], n)
                m = me.getValue(entry)
            else:
                m = newNationality(n)
                mp.put(catalog["nationalities"], n, m)
            lt.addLast(m['artworks'], artwork)

def newNationality(n):
    entry = {'Nationality': "", "artworks": None}
    entry['Nationality'] = n
    entry['artworks'] = lt.newList('SINGLE_LINKED', compareArtworksIds)
    return entry
# Funciones para creacion de datos

# Funciones de consulta

def getArtworksByMedium(catalog, medio):
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
def compareNationality(keyN, nationality):
    authentry = me.getKey(nationality)
    if (keyN == authentry):
        return 0
    elif (keyN > authentry):
        return 1
    else:
        return -1
def compareIds(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1
# Funciones de ordenamiento
def SortByDate(list):
    return mr.sort(list, cmpArtworkByDate)
def cmpArtworkByDate(artwork1, artwork2):
    if artwork1["Date"] == "":
        return 0
    else:
        return (artwork1["Date"]<artwork2["Date"])

def SortNationalities(catalog):
    nat = catalog["nationalities"]
    sort = lt.newList()
    keys = mp.keySet(nat)
    for key in lt.iterator(keys):
        n = mp.get(nat, key)
        v = me.getValue(n)
        lt.addLast(sort, v)
    return mr.sort(sort, cmpBySize)
    
def cmpBySize(n1, n2):
    return (lt.size(n1["artworks"])>lt.size(n2["artworks"]))    