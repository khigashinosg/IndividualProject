import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
from datetime import datetime, timedelta

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
method_names = [ # for naming plot figures
    'MLR',
    'RF',
    'SVR'
]
method_colours = [ # for colouring plot figures by regression method used
    '#8B0000',
    '#1f77b4',
    '#006400'
]

# Import ML packages
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

train_dates = [
    [10,2],
    [10,9],
    [10,16],
    [10,23],
    [10,30],
    [11,6],
    [11,13],
    [11,20],
    [11,27],
    [12,4],
    [12,11],
]

train_dates2 = [
    [11,11],
    [11,18],
    [11,25],
    [12,2],
    [12,9],
]

fs = 12         # fontsize
figsizex = 8.2  # figure width
figsizey = 11.1  # figure length
dotsize = 1.5     # dot size for scatterplots
train_select = 0  # 0 to 4

testset_y = [] # establish list for true occupancy sets
predicted_y = [] # establish list for predicted occupancy sets

for area_select in [0,1,2]: # 0 = ML, 1 = SC, 2 = SL 
    for train_select in [0]:
        data = pd.read_excel(data_path[area_select])
        train_end = datetime(2022,train_dates2[train_select][0],train_dates2[train_select][1]) # change date to end of training period
        test_start = train_end + timedelta(days=1) # test period is 1 day after train period ends
        for method_select in [0,1,2]: # 0 = Multiple Regression, 1 = Random Forest, 2 = Support Vector Regression
            
            # Split the dataset into training and testing sets
            x_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,1:]
            x_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,1:]
            y_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,0]
            y_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,0]

            # Initialize the regressor according to selected method
            if method_select == 0:
                regressor = LinearRegression()
            elif method_select == 1:
                regressor = RandomForestRegressor(n_estimators=100, random_state=0)
            elif method_select == 2:
                regressor = SVR(kernel='rbf')

            # Fit the model on the training data
            regressor.fit(x_train, y_train)

            # Predict the target variable on the testing data
            y_pred = regressor.predict(x_test)

            # Evaluate the model performance
            from sklearn.metrics import r2_score
            from sklearn.metrics import mean_squared_error
            from sklearn.preprocessing import MinMaxScaler

            # create an instance of MinMaxScaler
            scaler = MinMaxScaler()

            # fit and transform your data
            y_test_n = scaler.fit_transform(np.array(y_test).reshape(-1,1))
            y_pred_n = scaler.fit_transform(y_pred.reshape(-1,1))
            
            testset_y.append(y_test_n)
            predicted_y.append(y_pred_n)

    
n = 0 # counts how many loops the subplot function has been through
fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(figsizex,figsizey)) # establish subplot grid
for i in [0,1,2]: # loop through the areas
    for j in [0,1,2]: # loop through the regression methods
        axs[i,j].scatter(testset_y[n], predicted_y[n],s=dotsize,c=method_colours[j])
        axs[i,j].plot([0,1],[0,1],c='red',label = 'Line of perfect\nprediction')
        axs[i,j].tick_params(axis='y', labelright=True, labelleft=False, left= False, right=True)
        if i == 0:
            axs[i,j].text(0.07, 0.9, f'R^2: {round(r2_score(testset_y[n], predicted_y[n]),3)}', ha='left', va='center', fontsize=8, fontweight='bold', transform=axs[i,j].transAxes)
            axs[i,j].text(0.07, 0.83, f'RSME: {round(np.sqrt(mean_squared_error(testset_y[n], predicted_y[n])),3)}', ha='left', va='center', fontsize=8, fontweight='bold', transform=axs[i,j].transAxes)
            axs[i,j].legend(loc='lower right',fontsize=8)
        elif i == 1:
            axs[i,j].text(0.07, 0.8, f'R^2: {round(r2_score(testset_y[n], predicted_y[n]),3)}', ha='left', va='center', fontsize=8, fontweight='bold', transform=axs[i,j].transAxes)
            axs[i,j].text(0.07, 0.72, f'RSME: {round(np.sqrt(mean_squared_error(testset_y[n], predicted_y[n])),3)}', ha='left', va='center', fontsize=8, fontweight='bold', transform=axs[i,j].transAxes)
            axs[i,j].legend(loc='upper left',fontsize=8)
        elif i == 2:
            axs[i,j].text(0.98, 0.22, f'R^2: {round(r2_score(testset_y[n], predicted_y[n]),3)}', ha='right', va='center', fontsize=8, fontweight='bold')
            axs[i,j].text(0.98, 0.15, f'RSME: {round(np.sqrt(mean_squared_error(testset_y[n], predicted_y[n])),3)}', ha='right', va='center', fontsize=8, fontweight='bold')
            axs[i,j].legend(loc='lower right',fontsize=8)
        axs[0,j].set_title(f"{method_names[j]}", fontweight='bold', loc='center', fontsize=14,color=method_colours[j])
        axs[i,j].grid(True)
        n = n + 1

fig.text(0.085, 0.77, 'Main Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.497, 'Student Centre', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.22, 'Science Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)

fig.text(0.5, 0.065, 'True Occupancy (Normalised)', ha='center', fontsize=fs)
fig.text(0.95, 0.5, 'Predicted Occupancy (Normalised)', va='center', rotation='vertical',fontsize=fs)

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/ML Results/ML Methods Compare/tilNov11 (RelOcc).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
fig.clf()
    

