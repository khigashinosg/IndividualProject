import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
from scipy import stats 

data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Main Library Pre-processed.xlsx', # Main Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Student Centre Pre-processed.xlsx', # Student Centre (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Science Library Pre-processed.xlsx', # Science Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Main Library Pre-processed.xlsx', # Main Library (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Student Centre Pre-processed.xlsx', # Student Centre (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Science Library Pre-processed.xlsx', # Science Library (Term 2)
    ]

area_names = [ # for naming plot figures
    'Main Library',
    'Student Centre',
    'Science Library',
    'Main Library',
    'Student Centre',
    'Science Library',
]

results = {'Feature': [0,0,0,0,0,0,0],
        'Correlation Coefficient': [0,0,0,0,0,0,0],
        'P Value': [0,0,0,0,0,0,0]}
results = pd.DataFrame(results)

for area_select in [0,1,2,3,4,5]: # 0 = ML, 1 = SC, 2 = SL
    data = pd.read_excel(data_path[area_select])
    
    plt.plot(data['Counter'])
    plt.show()
    
    if area_select in [0,1,2]:
        ob = [0,1,2]
    elif area_select in [3,4,5]:
        ob = [3,4,5]
    ob.remove(area_select) # containing ID numbers of the other buildings (hence 'ob'), not building of interest
    
    feature_names = [
        'TimeOfDay',
        'DayOfWeek',
        'WeekOfTerm',
        'ReadingWeek',
        'InductionWeek',
        f'{area_names[ob[0]]}',
        f'{area_names[ob[1]]}'
    ]
    
    results['Feature'] = feature_names
    
    for i in range(len(feature_names)):
        corr, p_val = stats.spearmanr(data[feature_names[i]], data['Counter'])
        results['Correlation Coefficient'][i] = corr
        results['P Value'][i] = p_val
    
    print(results)