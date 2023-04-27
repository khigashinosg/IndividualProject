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

for area_select in [0]:
    data = pd.read_excel(data_path[area_select]) # import excel sheet containing basic occupancy numbers
    # Occupancy for any timeframe 
    if area_select in [0,1,2]:
        time_select = ['2022-11-09','2022-11-30'] # [start, end (inclusive)]
    elif area_select in [3,4,5]:
        time_select = ['2023-01-09','2023-03-05'] # [start, end (inclusive)]
    
    timeframe  = data.set_index(time)[time_select[0]:time_select[1]]
    fig, ax = plt.subplots()
    ax.plot(timeframe['Counter'],linewidth=2)
    plt.xlabel('Day-Month',fontsize=fs)
    plt.ylabel('Occupancy',fontsize=fs)
    fig.set_size_inches(4, 3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    locator = mdates.DayLocator(interval=5)
    ax.xaxis.set_major_locator(locator)
    plt.grid(True)
    #plt.show()
    if area_select in [0,1,2]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Mobile App/{area_names[area_select]}historic.png',bbox_inches='tight',dpi=200)
    elif area_select in [3,4,5]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Occupancy/Term 2/{area_names[area_select]}.png',bbox_inches='tight')
    plt.close()


    # Average occupancy by day within timeframe
    day_names = [ # Naming conventions for days of the week (Monday must be first, etc)
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
        ]
    day_data = {} # sorts all data by day of the week 
    day_avg = {} # average occupancy by day (per hour)

    timeframe = timeframe.reset_index(drop=False)

    for i in day_names:
        day_data[i] = timeframe[timeframe[time].dt.weekday == indexOf(day_names,i)]
        day_avg[i] = day_data[i].groupby(day_data[i][time].dt.hour)['Counter'].mean()
    
    # Plotting
    plt.figure(figsize=(4,3))
    for i in [0,1,2,3,4,5,6]: # input specific days via their respective number (Mon = 1, etc)
        day_avg[day_names[i]].plot(kind='line',x=None,y='time',use_index=True,label = f'{day_names[i]}') 
    plt.xlabel('Time (24 hr)',fontsize=fs)
    plt.ylabel('Occupancy',fontsize=fs)
    plt.legend(fontsize=fs-2)
    plt.grid(True)
    #plt.show()
    if area_select in [0,1,2]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Mobile App/{area_names[area_select]} Daily Averages (historic).png',bbox_inches='tight', dpi=200)
        #day_data.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Daily Averages Data/Term 1/{area_names[area_select]} Day Data.xlsx', index=False)

    elif area_select in [3,4,5]:
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Daily Averages/Term 2/{area_names[area_select]} Daily Averages.png',bbox_inches='tight')
        #day_data.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Daily Averages Data/Term 2/{area_names[area_select]} Day Data.xlsx', index=False)
    plt.close()
