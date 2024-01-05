import matplotlib.pyplot as plt
import pandas as pd

data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Main Library (Term 1) (Occupancy).xlsx', # Main Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Student Centre (Term 1) (Occupancy).xlsx', # Student Centre (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 1/Science Library (Term 1) (Occupancy).xlsx', # Science Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Main Library (Term 2) (Occupancy).xlsx', # ML (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Student Centre (Term 2) (Occupancy).xlsx', # SC (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Final Occupancy Data/Term 2/Science Library (Term 2) (Occupancy).xlsx' # SL (Term 2)
]

area_select = 0 # for area_select, 0 = ML, 1 = SC, 2 = SL
area_names = [ # for naming the columns for the other buildings in b_data_10mins below
    'Main Library',
    'Student Centre',
    'Science Library',
    'Main Library',
    'Student Centre',
    'Science Library',
]

for area_select in [0,1,2,3,4,5]:  # this loops code for specific datasets according to 'area_names'
    b_data = pd.read_excel(data_path[area_select]) # import data for building of interest ('b_data' is short for 'building_data')
    b_data.set_index(b_data.columns[0],inplace=True) # set index to be time-based instead of order-based

    if area_select in [0,1,2]:
        ob = [0,1,2]
    elif area_select in [3,4,5]:
        ob = [3,4,5]

    ob.remove(area_select) # containing ID numbers of the other buildings (hence 'ob'), not building of interest
    ob1_data = pd.read_excel(data_path[ob[0]]) # import data for 'OtherBuilding1'
    ob1_data.set_index(ob1_data.columns[0],inplace=True)
    ob2_data = pd.read_excel(data_path[ob[1]]) # import data for 'OtherBuilding2'
    ob2_data.set_index(ob2_data.columns[0],inplace=True)

    b_data_10min = b_data.resample('10T').mean().ffill() # downsample counter data to be averages of 10 min intervals
    ob1_data_10min = ob1_data.resample('10T').mean().ffill()
    ob2_data_10min = ob2_data.resample('10T').mean().ffill()

    feature_names = [
        'TimeOfDay',
        'DayOfWeek',
        'WeekOfTerm',
        'ReadingWeek',
        'InductionWeek',
        f'{area_names[ob[0]]}',
        f'{area_names[ob[1]]}'
    ]

    for i in feature_names: # sets up matrix for data filling (optimising code)
        b_data_10min[i] = 0

    b_data_10min[feature_names[5]] = ob1_data.resample('10T').mean().ffill() # other building 1's occupancy
    b_data_10min[feature_names[6]] = ob2_data.resample('10T').mean().ffill() # other building 2's occupancy
    b_data_10min.reset_index(inplace=True) # use numeric index for the following calculations
    b_data_10min[feature_names[0]] = b_data_10min[b_data_10min.columns[0]].dt.minute/10 + b_data_10min[b_data_10min.columns[0]].dt.hour * 6
    b_data_10min[feature_names[1]] = b_data_10min[b_data_10min.columns[0]].dt.weekday
    if area_select in [0,1,2]:
        b_data_10min[feature_names[2]] = b_data_10min[b_data_10min.columns[0]].dt.week - 39 # Offset to count Induction Week as Week 0
    elif area_select in [3,4,5]:
        b_data_10min[feature_names[2]] = b_data_10min[b_data_10min.columns[0]].dt.week - 1 # Offset to count first week of Term 2 as Week 1
    for i in range(len(b_data_10min)):
        if b_data_10min[b_data_10min.columns[0]][i].week in [45,7]: # Term 1's RW is Week 45 and Term 2's RW is Week 7
            b_data_10min[feature_names[3]][i] = 1
        if b_data_10min[b_data_10min.columns[0]][i].week == 39: # Induction Week is Week 39
            b_data_10min[feature_names[4]][i] = 1

    b_data_10min = b_data_10min.fillna(0,limit=1) # makes the first NaN value for building occupancy (if NaN values are present, they will be at the beginning)
    b_data_10min = b_data_10min.fillna(method='ffill') # forward fills and NaN occupancy values

    #b_data_10min.rename(columns = {b_data_10min.columns[0]:feature_names[0]}, inplace= True) # renaming the "Time" column
    if area_select in [0,1,2]:
        b_data_10min.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/{area_names[area_select]} Pre-processed.xlsx', index=False)
    elif area_select in [3,4,5]:
        b_data_10min.to_excel(f'/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/{area_names[area_select]} Pre-processed.xlsx', index=False)
    
