import csv
import config as cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
import time
catalog = {'artworks': None,
               "medium": None,
               "nationality": None}
catalog['artworks'] = lt.newList()            
catalog['artists'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0)


booksfile = cf.data_dir + 'MoMA/Artists-utf8-20pct.csv'
input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
for artist in input_file:
    mp.put(catalog["artists"], artist["ConstituentID"], artist)


start_time = time.process_time()
a = mp.valueSet(catalog["artists"])
stop_time = time.process_time()
elapsed_time_mseg = (stop_time - start_time)*1000
print(elapsed_time_mseg)


