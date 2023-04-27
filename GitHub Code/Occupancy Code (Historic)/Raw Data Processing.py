import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
import statistics as stat
from datetime import datetime, timedelta

# Filenames and Data Column Names
data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 1/Main Library (Term 1).xlsx', # UCL Main Library (ML) pathname (must be first)
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 1/Student Centre (Term 1).xlsx', # Student Centre (SC) pathname (must be second)
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 1/Science Library (Term 1).xlsx', # Science Library (SL) pathname (must be third)
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 2/Main Library (Term 2).xlsx',
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 2/Student Centre (Term 2).xlsx',
    '/Users/kyhi2018/Desktop/Individual Project/InOut Data/Term 2/Science Library (Term 2).xlsx'
    ] 

area_select = 0         # 0 = ML (Term 1), 1 = SC, 2 = SL, 3 = ML (Term2), 4 = SC, 5 = SL
area_names = [ 
    'Main Library (Term 1)',
    'Student Centre (Term 1)',
    'Science Library (Term 1)',
    'Main Library (Term 2)',
    'Student Centre (Term 2)',
    'Science Library (Term 2)',
]
for area_select in [1,2]: # loops for all areas in terms 1 and 2
    # Import raw data
    data = pd.read_excel(data_path[area_select],usecols=[0,1]) #import excel sheet

    time = data.columns[0] # reads the name of the 'time' column in raw data (normally 1st column)
    entry_exit = data.columns[1] # reads the name of the 'entry or exit' column in raw data (normally 2nd column)

    # Correct for Random Error (for Main Library and Science Library)
    if area_select == 0:
        data = data.drop(np.arange(166269,166436,1).astype(int)) # fixes net influx error on 7/11/22, removing some data between 15:05->15:15
        data = data.drop(np.arange(164902,166269,2.1).astype(int)) # fixes net influx error on 7/11/22, removing some data between 08:00->8:10
        data = data.drop(np.arange(166436,166859,2.1).astype(int)) # fixes net influx error on 7/11/22, removing some data between 15:15->17:00
        data = data.drop(np.arange(189882,190077,1).astype(int)) # fixes net influx error on 15/11/22, removing some data between 12:19->12:30
        data = data.drop(np.arange(188870,189882,3).astype(int)) # fixes net influx error on 15/11/22, removing some data between 08:30->12:19
        data = data.drop(np.arange(190077,191703,3).astype(int)) # fixes net influx error on 15/11/22, removing some data between 12:30->15:00
        data = data.drop(np.arange(277501,277787,1).astype(int)) # fixes net influx error on 06/12/22, removing some data between 14:00->14:15
        data = data.drop(np.arange(275757,276247,3.1).astype(int)) # fixes net influx error on 15/11/22, removing some data between 08:30->12:19
        data = data.drop(np.arange(277787,278498,3.1).astype(int)) # fixes net influx error on 15/11/22, removing some data between 12:30->15:00
    elif area_select == 2:
        data = data.drop(np.arange(39617,44029,2.4).astype(int)) # fixes net influx error on 6/10/22, removing some data between 9:00-15:00


    # Occupancy for any time-span 
    data = data.set_index([time]) # set index to be time (DateTime), not in terms of order (1,2,3,4, etc)
    data = data.reset_index() # resets index (becomes 1,2,3,4,etc) (setting then resetting index ensures continuous indices)
    data.rename(columns = {entry_exit:'Counter'}, inplace= True)


    for i in range(0,len(data)):
        if i == 0: # if first data point, counter is just the +/-1 from 0 (initial counter)
            if area_select == 4:
                data['Counter'][i] = 210
            elif data['Counter'][i][-1] == 'y':
                data['Counter'][i] = 1
            elif data['Counter'][i][-1] == 't':
                data['Counter'][i] = -1
        elif area_select in [0,3] and data[time][i-1].date() != data[time][i].date() and data[time][i].dayofweek in [1,2,3,4,5]: # For Main Library, Mon-Fri 00:00 starts with a counter of 0
            data['Counter'][i] = 0
        elif area_select in [0,3] and data[time][i-1].hour <= 20 and data[time][i].hour >= 21 and data[time][i].dayofweek in [5,6]: # For Main Library, Sat-Sun 21:00 starts with a counter of 0
            data['Counter'][i] = 0
        elif area_select in [1,4] and data[time][i-1].hour <= 4 and data[time][i].hour >= 5: # For Student Centre, 5 am triggers a counter reset of 27
            data['Counter'][i] = 27
        elif area_select in [2,5] and data[time][i-1].hour <= 3 and data[time][i].hour >= 4 and data[time][i].dayofweek in [1,2,3,4,5]: # For Science Library, 4 am triggers a counter reset of 10
            data['Counter'][i] = 10
        elif area_select in [2,5] and data[time][i-1].hour <= 20 and data[time][i].hour >= 21 and data[time][i].dayofweek in [5,6]:
            data['Counter'][i] = 0
        else:
            if data['Counter'][i][-1] == 'y': # entry ends in 'y', hence use this +1 the occupancy counter
                data['Counter'][i] = data['Counter'][i-1]+1
            elif data['Counter'][i][-1] == 't': # exit ends in 't', hence use this -1 the occupancy counter
                data['Counter'][i] = data['Counter'][i-1]-1

    # Correct for Systematic Error (using daily minimums as reference, daily minimums should be close to 0)
    error_fix = [ # coefficients of 3rd order polynomial lines of best fit that represent daily minimums) (ML, SL, SC) 
        [0,0,0,0],
        [0, -0.0252, 5.6513, -27.225],
        [0.0057,-0.922, 68.435, -25.83]
    ]

    # Plot occupancy and save extracted data 
    data = data.set_index([time],drop=True)
    fig, ax = plt.subplots()
    ax.plot(data['Counter'])
    plt.ylabel('Occupancy (people)', fontsize=12)
    fig.set_size_inches(10, 3.3)
    plt.grid(True)
    if area_select in [0,1,2]:
        plt.xlabel('Time (Term 1)', fontsize=12)
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/Term 1/{area_names[area_select]} (Occupancy).png',bbox_inches='tight') # saves all figures in specified folder
        data.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/{area_names[area_select]} (Occupancy).xlsx')
    elif area_select in [3,4,5]:
        plt.xlabel('Time (Term 2)', fontsize=12)
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/Term 2/{area_names[area_select]} (Occupancy).png',bbox_inches='tight') # saves all figures in specified folder
        data.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/{area_names[area_select]} (Occupancy).xlsx')
    #plt.show()

