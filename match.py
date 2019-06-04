## Dictionary of all villages currently Agrostar is cuurently working on, indexed by District
import csv
import pandas as pd
import numpy as np
from array import *
df = pd.read_csv('villages.csv')
dist = df['District']
dist = [x.strip(' ') for x in dist]
dist = np.array(dist)
dist = np.unique(dist).tolist()
dist1 = df['District'].tolist()
dist1 = [x.strip(' ') for x in dist1]
vill = df['Village Name'].tolist()
list = []
dict = {}
count=0
for var in dist:
    ind=dist1.index(var)
    list.insert(count,ind)
    count=count+1
for i in range(len(dist)-1):
    dict[dist[i]]=[list[i],list[i+1]-1]
dict['Yavatmal'] = [2715, 2832]
for key in dict.keys():
    dict[key] = vill[dict[key][0]:dict[key][1]]

dist.remove('Raigarh')
dist.remove('Sangli')


for district in dist:
         df1 = pd.read_csv(district + '.csv')
         a=df1['--SELECT--'].tolist()
         b=df1['--SELECT--.1'].tolist()
         vil = dict[district]
         vil = [x.strip(' ') for x in vil]
         village=[]
         mandal=[]
         i=0
         for var1 in vil:
             for var in a:
                 if (var == var1):
                     ind = a.index(var)
                     village.insert(i,var)
                     mandal.insert(i,b[ind])
                     i=i+1
         filename = district + '1.csv'
         with open(filename, 'w+') as csvfile:
             csvwriter = csv.writer(csvfile)
             csvwriter.writerow(['Mandal', 'Village'])
             for i,j in zip(mandal, village):
                 csvwriter.writerow([i, j])
