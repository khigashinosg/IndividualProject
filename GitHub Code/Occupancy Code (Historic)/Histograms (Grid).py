import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as stats
scaler = MinMaxScaler()

data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Main Library Pre-processed.xlsx', # Main Library (Term 1) but contains SC and SL data
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Main Library Pre-processed.xlsx', # Main Library (Term 2) but contains SC and SL data
]
area_names = [ # for naming plot figures
    'Main Library',
    'Student Centre',
    'Science Library',
    'Main Library',
    'Student Centre',
    'Science Library',
]

term_names = [
    'Term 1',
    'Term 2'
]

# Customisable options
fs = 12         # fontsize
figsizex = 8.2  # figure width
figsizey = 8.2  # figure length
dotsize = 1.5     # dot size for scatterplots
plot_data = []

for term_select in [0,1]: # this loops code for specific datasets according to 'area_names'
    # Import and data
    import_data = pd.read_excel(data_path[term_select]) # any data path works
    import_data = import_data.rename(columns={'Counter':'Main Library'})
    
    # need to remove all the irrelevant data according to the opening hours
    for area_select in [0,1,2]:
        if area_select == 0: # select data only for ML opening hours
            relevant_data = import_data[['Occurrence Time',area_names[area_select]]][import_data['Occurrence Time'].dt.time >= pd.Timestamp('08:30:00').time()]
        elif area_select == 1: # select data only for SC opening hours
            relevant_data = import_data[['Occurrence Time',area_names[area_select]]]
        elif area_select == 2: # select data only for SL opening hours
            # Create a mask to select all times except for Sat 21:00 to Sun 11:00 
            mask1 = ~((import_data['Occurrence Time'].dt.weekday == 5) & (import_data['Occurrence Time'].dt.hour >= 21) & (import_data['Occurrence Time'].dt.hour < 24) | (import_data['Occurrence Time'].dt.weekday == 6) & (import_data['Occurrence Time'].dt.hour >= 0) & (import_data['Occurrence Time'].dt.hour < 11))
            # Create a mask to select all times except for Sun 21:00 to Mon 08:45 
            mask2 = ~((import_data['Occurrence Time'].dt.weekday == 6) & (import_data['Occurrence Time'].dt.hour >= 21) & (import_data['Occurrence Time'].dt.hour < 24) | (import_data['Occurrence Time'].dt.weekday == 0) & (import_data['Occurrence Time'].dt.hour >= 0) & (import_data['Occurrence Time'].dt.hour < 8) & (import_data['Occurrence Time'].dt.minute < 45))
            # Apply the masks to the DataFrame to select all times except for the specified periods
            relevant_data = import_data[['Occurrence Time',area_names[area_select]]].loc[mask1 & mask2]
        
        plot_data.append(relevant_data[area_names[area_select]])


n = 0 # counts how many loops the subplot function has been through
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(figsizex,figsizey)) # establish subplot grid
for j in [0,1]: # loop through the terms
    for i in [0,1,2]: # loop through the areas
        axs[i,j].hist(plot_data[n],bins=20)
        axs[0,j].set_title(f"{term_names[j]}", fontsize=14, fontweight='bold', loc='center')
        axs[i,j].tick_params(axis='y', labelright=True, labelleft=False, left= False, right=True)
        axs[i,j].grid(True)
        n = n + 1

fig.text(0.085, 0.77, 'Main Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.497, 'Student Centre', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.22, 'Science Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)

fig.text(0.5, 0.06, 'Occupancy (Absolute)', ha='center', fontsize=fs)
fig.text(0.955, 0.5, 'Frequency', va='center', rotation='vertical',fontsize=fs)

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy Histograms/AllAreasAndTerms (Grid).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
fig.clf()

