import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np

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

fs = 12         # fontsize
figsizex = 8.2  # figure width
figsizey = 11.1  # figure length
dotsize = 1.5     # dot size for scatterplots

testset_y = [] # establish list for true occupancy sets
predicted_y = [] # establish list for predicted occupancy sets

for area_select in [0,1,2]: # 0 = ML, 1 = SC, 2 = SL
    data = pd.read_excel(data_path[area_select])
    data_t2 = pd.read_excel(data_path[area_select+3]) # +3 selects the term 2 equivalent
    for method_select in [0,1,2]: # 0 = Multiple Regression, 1 = Random Forest, 2 = Support Vector Regression

        # Select the features (input) and response variable (output)
        x = data.iloc[:,2:-2] # selects all features but last 2 features (relative occupancy)
        y = data.iloc[:,1] # selects 'counter' as response variable
        x_t2 = data_t2.iloc[:,2:-2]
        y_t2 = data_t2.iloc[:,1]

        # Initialize the regressor according to selected method
        if method_select == 0:
            regressor = LinearRegression()
        elif method_select == 1:
            regressor = RandomForestRegressor(n_estimators=100, random_state=0)
        elif method_select == 2:
            regressor = SVR(kernel='rbf')

        # Fit the model on the training data
        regressor.fit(x, y)

        # Predict the target variable on the testing data
        y_pred = regressor.predict(x_t2)

        # Evaluate the model performance
        from sklearn.metrics import r2_score
        from sklearn.metrics import mean_squared_error
        from sklearn.preprocessing import MinMaxScaler

        # create an instance of MinMaxScaler
        scaler = MinMaxScaler()

        # fit and transform your data
        y_test_n = scaler.fit_transform(np.array(y_t2).reshape(-1,1))
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
        axs[0,j].set_title(f"{method_names[j]}", fontweight='bold', loc='center', fontsize=14,color=method_colours[j])
        if j == 1:
            axs[i,j].text(0.07, 0.8, f'R^2: {round(r2_score(testset_y[n], predicted_y[n]),3)}', ha='left', va='center', fontsize=8, fontweight='bold')
            axs[i,j].text(0.07, 0.72, f'RSME: {round(np.sqrt(mean_squared_error(testset_y[n], predicted_y[n])),3)}', ha='left', va='center', fontsize=8, fontweight='bold')
            axs[i,j].legend(loc='upper left',fontsize=8)
        else:
            axs[i,j].text(0.98, 0.22, f'R^2: {round(r2_score(testset_y[n], predicted_y[n]),3)}', ha='right', va='center', fontsize=8, fontweight='bold')
            axs[i,j].text(0.98, 0.15, f'RSME: {round(np.sqrt(mean_squared_error(testset_y[n], predicted_y[n])),3)}', ha='right', va='center', fontsize=8, fontweight='bold')
            axs[i,j].legend(loc='lower right',fontsize=8)
        axs[i,j].grid(True)
        n = n + 1

fig.text(0.085, 0.77, 'Main Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.497, 'Student Centre', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.22, 'Science Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)

fig.text(0.5, 0.065, 'True Occupancy (Normalised)', ha='center', fontsize=fs)
fig.text(0.95, 0.5, 'Predicted Occupancy (Normalised)', va='center', rotation='vertical',fontsize=fs)

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/ML Results/ML Methods Compare/T1Train.png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
fig.clf()