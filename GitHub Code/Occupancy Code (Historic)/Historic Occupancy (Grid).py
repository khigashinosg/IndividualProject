import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
import matplotlib.dates as mdates

time = 'Occurrence Time'
uid = 'Unique Cardholder ID'
data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Main Library (Term 1) (Occupancy).xlsx', # Main Library (final dataset)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Student Centre (Term 1) (Occupancy).xlsx', # Student Centre (final dataset)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Science Library (Term 1) (Occupancy).xlsx', # Science Library (final dataset)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Main Library (Term 2) (Occupancy).xlsx', # Main Library (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Student Centre (Term 2) (Occupancy).xlsx', # Student Centre (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Science Library (Term 2) (Occupancy).xlsx', # Science Library (Term 2)
             ]

# for area_select, 0 = ML, 1 = SC, 2 = SL
fs = 12
area_names = [ 
    'Main Library (Term 1)',
    'Student Centre (Term 1)',
    'Science Library (Term 1)',
    'Main Library (Term 2)',
    'Student Centre (Term 2)',
    'Science Library (Term 2)',
]

term_names = [
    'Term 1',
    'Term 2'
]

plot_data = []

fs = 12         # fontsize
figsizex = 11.6  # figure width
figsizey = 7.55  # figure length

for area_select in [0,1,2,3,4,5]:
    data = pd.read_excel(data_path[area_select]) # import excel sheet containing basic occupancy numbers
    # Occupancy for any timeframe 
    if area_select in [0,1,2]:
        time_select = ['2022-09-26','2022-12-16'] # [start, end (inclusive)]
    elif area_select in [3,4,5]:
        time_select = ['2023-01-09','2023-03-05'] # [start, end (inclusive)]
    
    timeframe  = data.set_index(time)[time_select[0]:time_select[1]]
    fig, ax = plt.subplots()
    ax.plot(timeframe['Counter'])
    plt.xlabel('Date and Time (Month-Day Hour)',fontsize=fs)
    plt.ylabel('Occupancy (people)',fontsize=fs)
    fig.set_size_inches(10, 3.3)
    plt.grid(True)
    #plt.show()
    if area_select in [0,1,2]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/Term 1/{area_names[area_select]}.png',bbox_inches='tight')
    elif area_select in [3,4,5]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/Term 2/{area_names[area_select]}.png',bbox_inches='tight')
    plt.close()
    plot_data.append(timeframe['Counter'])


n = 0 # counts how many loops the subplot function has been through
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(figsizex,figsizey)) # establish subplot grid
fig.subplots_adjust(hspace=0.2,wspace=0.12)  # Adjust vertical space between subplots
for j in [0,1]: # loop through the terms
    for i in [0,1,2]: # loop through the areas
        axs[i,j].plot(plot_data[n])
        axs[0,j].set_title(f"{term_names[j]}", fontsize=14, fontweight='bold', loc='center')
        axs[i,j].tick_params(axis='y', labelright=True, labelleft=False, left= False, right=True)
        axs[i,j].grid(True)
        axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        if j==0:
            locator = mdates.DayLocator(interval=12)
        elif j ==1:
            locator = mdates.DayLocator(interval=8)
        axs[i,j].xaxis.set_major_locator(locator)
        n = n + 1

fig.text(0.09, 0.77, 'Main Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.09, 0.497, 'Student Centre', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.09, 0.22, 'Science Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)

fig.text(0.5, 0.05, 'Date (MM-DD)', ha='center', fontsize=fs)
fig.text(0.95, 0.5, 'Occupancy (Absolute)', va='center', rotation='vertical',fontsize=fs)

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/AllAreasAndTerms (Grid).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
fig.clf()