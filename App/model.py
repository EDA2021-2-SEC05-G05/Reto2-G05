﻿"""
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
    catalog['artworks'] = mp.newMap(160000,
                                    maptype='PROBING',
                                    loadfactor=0.50,
                                    comparefunction=compareArtworksIds)
    catalog['artists'] = mp.newMap(16000,
                                   maptype='PROBING',
                                   loadfactor=0.50,
                                   comparefunction=compareIds)
    catalog["medium"] = mp.newMap(1000,
                                   maptype='PROBING',
                                   loadfactor=0.50,
                                   comparefunction=compareMedium)
    catalog["nationalities"] = mp.newMap(200,
                                   maptype='PROBING',
                                   loadfactor=0.50,
                                   comparefunction=compareNationality)
    catalog["DAs"] = mp.newMap(500,
                                   maptype='PROBING',
                                   loadfactor=0.50,
                                   comparefunction=compareDA)
    catalog["BDs"] = mp.newMap(1000,
                                   maptype='PROBING',
                                   loadfactor=0.50,
                                   comparefunction=compareDA)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    #addArtworkMedium(catalog, artwork)
    artwork = addArtists(catalog, artwork)
    #addArtworkNationality(catalog, artwork)
    addDA(catalog, artwork)
    id = artwork["ObjectID"]
    mp.put(catalog['artworks'], id, artwork)
    
    

def addArtist(catalog, artist):
    addBD(catalog, artist)
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

def addArtworkNationality(catalog):
    values = mp.valueSet(catalog["artworks"])
    for artwork in lt.iterator(values):
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

def addDA(catalog, artwork):
    DAmap = catalog["DAs"]
    DoA = artwork["DateAcquired"]
    if (artwork['DateAcquired'] == ''):
        DoA = "Unknown"
    existmed = mp.contains(DAmap, DoA)
    if existmed:
        entry = mp.get(DAmap, DoA)
        m = me.getValue(entry)
    else:
        m = newDA(DoA)
        mp.put(DAmap, DoA, m)
    lt.addLast(m['artworks'], artwork)

def newDA(DoA):
    entry = {'DA': "", "artworks": None}
    entry['DA'] = DoA
    entry['artworks'] = lt.newList('SINGLE_LINKED', compareMedium)
    return entry

def addBD(catalog, artist):
    BDmap = catalog["BDs"]
    bd = artist["BeginDate"]
    if (artist['BeginDate'] == ''):
        bd = "Unknown"
    existmed = mp.contains(BDmap, bd)
    if existmed:
        entry = mp.get(BDmap, bd)
        m = me.getValue(entry)
    else:
        m = newBD(bd)
        mp.put(BDmap, bd, m)
    lt.addLast(m['artists'], artist)

def newBD(DoA):
    entry = {'BD': "", "artists": None}
    entry['BD'] = DoA
    entry['artists'] = lt.newList('SINGLE_LINKED', compareMedium)
    return entry
# Funciones para creacion de datos

# Funciones de consulta
def ArtistsByBD(catalog, date0, dateF):
    values = catalog["valuesartists"]
    list = lt.newList()
    for value in lt.iterator(values):
        if value["BD"] >= date0:
            if value["BD"] <= dateF:
                value["artists"] = mr.sort(value["artists"], cmpDName)
                for artist in lt.iterator(value["artists"]):
                    lt.addLast(list, artist)
            else:
                return list
    return list

def ArtworksByDA (catalog, date0, datef):
    artworksbyDA = lt.newList()
    purchased = 0
    values = catalog["valuesartworks"]
    for value in lt.iterator(values):
        if value["DA"] >=date0:
            if value["DA"]<=datef:
                value["artworks"] = mr.sort(value["artworks"], cmpName)
                for artwork in lt.iterator(value["artworks"]):
                    lt.addLast(artworksbyDA, artwork)
                    if "Purchase" in artwork["CreditLine"] or "Purchased" in artwork["CreditLine"]:
                        purchased += 1
    return artworksbyDA, purchased
def getArtworksByMedium(catalog, medio):
    medio = mp.get(catalog['medium'], medio)
    if medio:
        return me.getValue(medio)['artworks']
    return None

# Funciones utilizadas para comparar elementos dentro de una lista
def compareArtworksIds(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
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
def compareDA(keyAD, AD):
    authentry = me.getKey(AD)
    if (keyAD == authentry):
        return 0
    elif (keyAD > authentry):
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
def sortArtistsBD(list):
    return mr.sort(list, cmpArtist)
def cmpArtist(artist1, artist2):
    return (artist1["BeginDate"]<artist2["BeginDate"])
def SortByDate(catalog):
    list = mp.keySet(catalog["artists"])
    s = mr.sort(list, cmpDate)
    catalog["keysartists"] = s
def cmpDate(date1, date2):
    return (date1<date2)
def cmpName(n1, n2):
    return n1["Title"]<n2["Title"]
def cmpDName(n1, n2):
    return n1["DisplayName"]<n2["DisplayName"]
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
def sortNlist(list):
    return mr.sort(list, cmpByTitle)
def cmpByTitle(n1, n2):
    return (n1["Date"]<n2["Date"]) 
def sortByDA(catalog):
    list = mp.valueSet(catalog["DAs"])
    catalog["valuesartworks"] = mr.sort(list, cmpByDA)
    
def cmpByDA(n1, n2):
    return (n1["DA"]<n2["DA"]) 

def sortByBD(catalog):
    list = mp.valueSet(catalog["BDs"])
    catalog["valuesartists"] = mr.sort(list, cmpByBD)
    
def cmpByBD(n1, n2):
    return (n1["BD"]<n2["BD"]) 
#def checkNotDuplicate(list, artwork):
    for i in lt.iterator(list):
        if i == artwork:
            return False
    return True
