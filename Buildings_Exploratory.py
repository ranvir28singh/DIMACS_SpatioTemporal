
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# For reading building.yaml as a Python dict
import yaml # If you don't have this package use 'pip install pyyaml' into commandline or terminal


# Matplotlib Config
get_ipython().magic('matplotlib inline')
plt.style.use('fivethirtyeight')


# In[2]:

# Turn 'building.yaml' file into a python dictionary using PyYAML 
with open('Files/building.yaml') as f:
    building_data = f.read()
    building_data = yaml.load(building_data)
    f.close()


# In[3]:

## See what keys exist in the dictionary
#print(building_data.keys())


# ## Further Exploration

# In[4]:

## There is only one key, which further has two keys - Type has one value 'obstacle' so we're interested in 'geometries'
#print(building_data['building1'].keys())
#print(building_data['building1']['type'])


## 'geometries' is a list with 6461 objects
#print(type(building_data['building1']['geometries']))
#print(type(building_data['building1']['geometries'][0]))
#print(len(building_data['building1']['geometries']))
#print(len(building_data['building1']['geometries'][0]))


# In[5]:

#this is how one element of geometries looks like

#building_data['building1']['geometries'][0]

#its a list of dictionaries  with 3 keys - collision_geometry, config and name
#collision


# In[6]:

## Print first ten elements of the list
#print(building_data['building1']['geometries'][:10])


# In[7]:

## 'type' seems interesting in the 'geometries' dictionary
## Iterate over the elements, add it to a list and use 'set' to get the unique 'types'

#type_list = []
#for i in building_data['building1']['geometries']:
#    type_list.append(i['collision_geometry']['type'])
    
## Set gives you the unique elements in a list
#print(set(type_list))


# In[8]:

## Look at items that are of type 'box'
#box_type = []
#for i in building_data['building1']['geometries']:
#    if i['collision_geometry']['type'] == 'box':
#        box_type.append(i['name'])

#len(box_type)
#print(box_type)
## Most of them are NoName objects so let's look at type == 'polygons'


# ### Set of Z values for type polygon

# In[9]:

## Let's try another approach where we print out all 'names' that are not 'NoName' to see what different type of
## objects exist.

#for i in range(0,len(building_data['building1']['geometries'])):
#    if 'NoName' not in str(building_data['building1']['geometries'][i]['name']):
#        print(building_data['building1']['geometries'][i]['name'])
        
## Pretty much the same result as the polygon/box differentiation.


# ## List of entrances/exits

# In[10]:

## For an initial run, let's look at objects that have the words 'exit' 'entry' 'entrance' in their name
## and add their info to a list.
## There could be more than these entrances/exits with other names?? - this is just for a starting point


# In[11]:

exit_entry_list = []

for i in range(0,len(building_data['building1']['geometries'])):
    for keyword in ['exit','entry','entrance']:
        if (keyword in str(building_data['building1']['geometries'][i]['name']).lower()):
            exit_entry_list.append(building_data['building1']['geometries'][i])

#print(len(exit_entry_list))


# In[12]:

## So we'd probably be interested in the triangle coordiantes - Still need to figure out how these work
## Lets take the first element of our entry_exit list as test


# ## Entrance/Exits with their coordinates

# In[13]:

# Convert list of Entrances/Exit to PANDAS Dataframe

df_list = []

# Iterate over the exit_entry_list to get 'names' and 'triangles' points
# Turn into dictionary and append to df_list for creation of dataframe

for i in exit_entry_list:
    xyz_list = []
    coordinates = i['collision_geometry']['triangles']
    for j in range(0,len(coordinates),3):
        xyz_list.append((coordinates[j],coordinates[j+1],coordinates[j+2]))
    x = coordinates[::3]
    y = coordinates[1::3]
    z = coordinates[2::3]
    data = {'name' : i['name'],
           'x' : x,
           'y' : y,
           'z' : z,
            'triangles' : xyz_list, #list of triples
            'no_of_triangles' : len(xyz_list),  #no. of triangles used to represent each entrance/exit varies
           }
    
    df_list.append(data)

# Create the dataframe
df = pd.DataFrame(df_list)
df.head(10)

# Because the way we look for 'exit' , 'entrance' and 'exit' in our list exit_entry_list, some elements appear twice 
# (those that have 2 of those words at the same time in their name)

df = df.drop_duplicates(subset='name',keep='first')
df.reset_index(drop=True,inplace=True)
df.head()


# In[14]:

#this process is to find out the total centroid of each entrance/exit
df['mean_x'] = df['x'].apply(np.mean)
df['mean_y'] = df['y'].apply(np.mean)
df['mean_z'] = df['z'].apply(np.mean)
df['centroid'] = df[['mean_x','mean_y','mean_z']].apply(tuple,axis=1)
df = df.drop(['mean_x','mean_y','mean_z'],axis=1)
df.head()


# In[ ]:




# In[15]:

# Convert to CSV for usage in other files
#df.to_csv('entrance_exit_points.csv',index=False)


# In[16]:

#Z value for type polygon ranges upto 24 whereas Z value of entrance/exits goes only upto 6.
#Are there no entrances/exits in the floors above that??????


# In[18]:

#get_ipython().system('jupyter nbconvert --to script Buildings_Exploratory.ipynb')


# In[ ]:



