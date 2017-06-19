
# coding: utf-8

# <h3> Documentation for Thread Files : </h3>
# 1. 8 threads running the simulation (agents) parallel. Each thread would write into it's own file (thread_i.txt) where i>=0 && i<8.
# 
# 2. The first line contains the total number of agents and ratio of Milli seconds to frames.  (Ex: 8501, 0.05). So in this example 1 frame = 20 milliseconds.
# 
# 3. The format of the other lines is: sec, agent_id, agent_type, has_luggage, is_disabled, X, Y, Z, velocity, queue_id, lookUp_X, lookUp_Y. (lookUp_X, lookUp_Y - gives the next position of the agent)
# 
# 4. Regarding the heights: For floor f, the Z = 3 * ( f -1 ) + 1. So for the first floor, Z=1, second Z= 4, third Z= 7 etc.
# 
# 

# <h3> Major Things to Do </h3>
# 
# - Map Entrance/Exit data onto Agent Data?

# In[10]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml # For reading building.yaml as a Python dict
import ast

from Buildings_Exploratory import df as entry_exit_points


# Matplotlib Config
get_ipython().magic('matplotlib inline')
plt.style.use('fivethirtyeight')


# In[ ]:




# In[11]:

print(pd.__version__) # Should be 0.20.1
print(np.__version__) # Should be 1.12.1
print(yaml.__version__) # Should be 3.12 - If you don't have this use 'pip install pyyaml' into your command line/terminal


# In[ ]:




# In[12]:

### Read thread_x file and convert to a PANDAS dataframe (and one CSV)
### Column Names for our dataframe

col_names = ['sec', 
             'agent_id',
             'agent_type',
             'has_luggage',
             'is_disabled',
             'X', 
             'Y',
             'Z',
             'velocity',
             'queue_id',
             'lookUp_X',
             'lookUp_Y']

# Convert the file into a Pandas DF. Ignore first line (header=0) and use col_names as headers instead.
# Play around with this df and generalize the outcomes for the other 7 files

df = pd.read_csv('Files/Agents/thread_0.txt', header=0, names=col_names)


# In[ ]:




# In[13]:

# Code for merging all 8 files into one big dataframe - Don't think this approach is correct
# as each file (probably?) represents a seperate simulation.

file_number = list(range(0,8))
main_df = pd.DataFrame()

### Iterate over the 8 files and add each individual files dataframe to one large df called main_df

for i in file_number:
    df_thread = pd.read_csv('Files/Agents/thread_' + str(i) + '.txt',header=0,names=col_names)
    main_df = main_df.append(df_thread,ignore_index=True)


# In[14]:

# Sort dataframe by Agent_ID and TimeStamp
#df = df.sort_values(by=['agent_id','sec'])
#df.head(20)

# Plot one agent
#df[df['agent_id'] == 0].plot.scatter(x='X',y='Y',figsize=(10,10))


# In[15]:

# Convert Z values to floors (don't know if useful or not)

# Function to convert Z value to floor
def z_to_floor(z_value):
    return (z_value + 2) / 3

#df['Z'] = df['Z'].map(lambda x : z_to_floor(x))
#print(df['Z'].value_counts())

# Not all Z values are integers. Are these agents between floors? On Elevators or Stairs or something?
# If we use floor division instead of float division in the conversion function (i.e. use // instead of /), we'd
# end up with integers but not sure how accurate that would be as it rounds down


# In[16]:



# Code for merging all 8 files into one big dataframe - Don't think this approach is correct
# as each file (probably?) represents a seperate simulation.

file_number = list(range(0,8))
entry_df = pd.DataFrame()

from scipy.spatial import distance

### Iterate over the 8 files and add each individual files dataframe to one large df called main_df

for i in file_number:
    
    df_thread = pd.read_csv('Files/Agents/thread_' + str(i) + '.txt',header=0,names=col_names)
    df = df_thread.sort_values("sec").groupby("agent_id", as_index=False).first() 
    df_list = []
    dist = 100

    #calculating euclidean distance
    for i in df.iterrows(): #each agent going into the loop
        starting_point = (i[1]['X'],i[1]['Y'],(i[1]['Z']-1)) #there is a -1 on Z value to make it in unison with building Z values
        for j in entry_exit_points.iterrows(): #each exit going into the loop
            for k in j[1]['triangles']: #each triangle going into the loop
                d = distance.euclidean(k,starting_point) #distance from each triangle to starting point of agent
                if d < dist:
                    dist = d
                    entrance = j[1]['name']
                    triangle = k

        data = {'agent_id' : i[1]['agent_id'],
                'entry_time' : i[1]['sec'],
                'agent_type' : i[1]['agent_type'],
                'has_luggage' :  i[1]['has_luggage'],
                'is_disabled' : i[1]['is_disabled'],
                'starting_point' : starting_point,
                'entrance' : entrance,
                'dist' : dist,
                'triangle' : triangle}
        df_list.append(data)

    entrances = pd.DataFrame(df_list)
    
    entry_df = entry_df.append(entrances,ignore_index=True)


# In[ ]:

# Code for merging all 8 files into one big dataframe - Don't think this approach is correct
# as each file (probably?) represents a seperate simulation.

file_number = list(range(0,8))

exit_df = pd.DataFrame()

from scipy.spatial import distance

### Iterate over the 8 files and add each individual files dataframe to one large df called main_df

for i in file_number:
    
    df_thread = pd.read_csv('Files/Agents/thread_' + str(i) + '.txt',header=0,names=col_names)
    
    df = df_thread.sort_values("sec").groupby("agent_id", as_index=False).last() 
    df_list = []
    dist = 100

    #calculating euclidean distance
    for i in df.iterrows(): #each agent going into the loop
        
        starting_point = (i[1]['X'],i[1]['Y'],(i[1]['Z']-1)) #there is a -1 on Z value to make it in unison with building Z values
        
        for j in entry_exit_points.iterrows(): #each exit going into the loop
            for k in j[1]['triangles']: #each triangle going into the loop
                d = distance.euclidean(k,starting_point) #distance from each triangle to starting point of agent
                if d < dist:
                    dist = d
                    exit = j[1]['name']
                    triangle = k

        data = {'agent_id' : i[1]['agent_id'],
                'entry_time' : i[1]['sec'],
                'agent_type' : i[1]['agent_type'],
                'has_luggage' :  i[1]['has_luggage'],
                'is_disabled' : i[1]['is_disabled'],
                'starting_point' : starting_point,
                'exit' : exit,
                'dist' : dist,
                'triangle' : triangle}
        
        df_list.append(data)

    exits = pd.DataFrame(df_list)
    
    exit_df = exit_df.append(exits,ignore_index=True)


# In[ ]:




# In[ ]:




# In[ ]:

#get_ipython().system('jupyter nbconvert --to script Agent_Data_First_Look.ipynb')


# In[ ]:



