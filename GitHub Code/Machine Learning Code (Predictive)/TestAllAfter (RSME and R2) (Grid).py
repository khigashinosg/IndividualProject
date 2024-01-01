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

term_names = [
    'Term 1',
    'Term 2'
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
    [12,16]
]

train_dates2 = [
    [11,11],
    [11,18],
    [11,25],
    [12,2],
    [12,9],
]

n_factor = [ # Max Occupancy according to UCL website
    625, # ML
    641, # SC 
    918, # SL
]

fs = 12         # fontsize
figsizex = 8.2  # figure width
figsizey = 11.6  # figure length
dotsize = 1.5     # dot size for scatterplots

RMSE_alldata = []
R2_alldata = []

for area_select in [0,1,2]: # 0 = ML, 1 = SC, 2 = SL 

    testset_y = []
    predicted_y = []
    testset_y_t2 = []
    predicted_y_t2 = []

    for train_select in [0,1,2,3,4,5,6,7,8,9,10,11]:
        data = pd.read_excel(data_path[area_select])
        data_t2 = pd.read_excel(data_path[area_select+3]) # +3 selects the term 2 equivalent
        train_end = datetime(2022,train_dates[train_select][0],train_dates[train_select][1]) # change date to end of training period
        test_start = train_end + timedelta(days=1) # test period is 1 day after train period ends
        for method_select in [1]: # 0 = Multiple Regression, 1 = Random Forest, 2 = Support Vector Regression
            
            # Split the dataset into training and testing sets
            x_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,1:-2]
            x_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,1:-2]
            y_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,0]
            y_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,0]
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
            regressor.fit(x_train, y_train)

            # Predict the target variable on the testing data
            if train_select in range(0,11):
                y_pred = regressor.predict(x_test)
            y_pred_t2 = regressor.predict(x_t2)

            # Evaluate the model performance
            from sklearn.metrics import r2_score
            from sklearn.metrics import mean_squared_error
            from sklearn.preprocessing import MinMaxScaler

            # create an instance of MinMaxScaler
            scaler = MinMaxScaler()

            # normalise data according to UCL website occupancies
            if train_select in range(0,11):    
                y_test_n = np.array(y_test)/n_factor[area_select]
                y_pred_n = np.array(y_pred)/n_factor[area_select]
                testset_y.append(y_test_n)
                predicted_y.append(y_pred_n)
            
            y_test_t2_n = np.array(y_t2)/n_factor[area_select]
            y_pred_t2_n = np.array(y_pred_t2)/n_factor[area_select]
            testset_y_t2.append(y_test_t2_n)
            predicted_y_t2.append(y_pred_t2_n)
    
    
    testset = [ # set up for the plot for loop
        testset_y,
        testset_y_t2
    ]
    
    predicted = [ # set up for the plot for loop
        predicted_y,
        predicted_y_t2
    ]

    for k in [0,1]: # Loop through the terms
        n = 0
        RMSE_values = []
        R2_values = []
        
        # Scatterplots for all weeks
        fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(figsizex,figsizey)) # establish subplot grid
        fig.subplots_adjust(hspace=0.3, wspace = 0.22)  # Adjust vertical space between subplots
        for i in [0,1,2,3]: # Loop through rows after columns
            for j in [0,1,2]: # loop through columns first
                axs[i,j].scatter(testset[k][n], predicted[k][n],s=dotsize)
                axs[i,j].plot([0,2],[0,2],c='red',label = 'Line of perfect\nprediction')
                if i == 0 and j == 0:
                    axs[i,j].text(0.02, 0.75, f'R^2: {round(r2_score(testset[k][n], predicted[k][n]),3)}', transform=axs[i,j].transAxes, ha='left', va='center',fontsize=7,fontweight='bold')
                    axs[i,j].text(0.02, 0.67, f'RSME: {round(np.sqrt(mean_squared_error(testset[k][n], predicted[k][n])),3)}', transform=axs[i,j].transAxes, ha='left', va='center',fontsize=7,fontweight='bold')
                    axs[i,j].legend(loc='upper left',fontsize=8)  
                else:
                    if area_select in [0,2] and i in [2,3] and k==1:
                        axs[i,j].text(0.02, 0.75, f'R^2: {round(r2_score(testset[k][n], predicted[k][n]),3)}', transform=axs[i,j].transAxes, ha='left', va='center',fontsize=7,fontweight='bold')
                        axs[i,j].text(0.02, 0.67, f'RSME: {round(np.sqrt(mean_squared_error(testset[k][n], predicted[k][n])),3)}', transform=axs[i,j].transAxes, ha='left', va='center',fontsize=7,fontweight='bold')
                        axs[i,j].legend(loc='upper left',fontsize=8)       
                    else:             
                        axs[i,j].text(0.98, 0.31, f'R^2: {round(r2_score(testset[k][n], predicted[k][n]),3)}', transform=axs[i,j].transAxes, ha='right', va='center',fontsize=7,fontweight = 'bold')
                        axs[i,j].text(0.98, 0.23, f'RSME: {round(np.sqrt(mean_squared_error(testset[k][n], predicted[k][n])),3)}', transform=axs[i,j].transAxes, ha='right', va='center',fontsize=7,fontweight='bold')
                        axs[i,j].legend(loc='lower right',fontsize=8)
                if k == 0:
                    if n == 0:
                        axs[i,j].set_title(f"Wk 1 Train, {n+2}-12 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                    elif n == 10:
                        axs[i,j].set_title(f"Wks 1-{n+1} Train, 12 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                    else:
                        axs[i,j].set_title(f"Wks 1-{n+1} Train, {n+2}-12 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                elif k == 1:
                    if n == 0:
                        axs[i,j].set_title(f"Wk 1 Train, {n+2}-13 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                    elif n == 11:
                        axs[i,j].set_title(f"Wks 1-{n+1} Train, 13 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                    else:
                        axs[i,j].set_title(f"Wks 1-{n+1} Train, {n+2}-13 Test", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                ax_lim = max([max(predicted[k][n]),max(testset[k][n])])
                axs[i,j].set_ylim([0,ax_lim])
                axs[i,j].set_xlim([0,ax_lim])
                axs[i,j].grid(True)
                R2_values.append(round(r2_score(testset[k][n], predicted[k][n]),3))
                RMSE_values.append(round(np.sqrt(mean_squared_error(testset[k][n], predicted[k][n])),3))
                n = n + 1
                if k == 0 and n == 11:
                    axs[3,2].set_title(f"N/A", fontsize=10, fontweight='bold', loc='center', y=-0.24)
                    fig.text(0.788, 0.172, 'Trained on all T1 data\n\nNo T1 data left for testing', ha='center',fontsize=10)
                    break
        fig.text(0.5, 0.06, 'True Occupancy (Normalised)', ha='center',fontsize=fs)
        fig.text(0.04, 0.5, 'Predicted Occupancy (Normalised)', va='center', rotation='vertical',fontsize=fs)
        plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/ML Results/Test Rest/Scatterplots (Grid)/{area_names[area_select]} (Term{k+1}) (Grid).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
        fig.clf()
        

        R2_alldata.append(R2_values)
        RMSE_alldata.append(RMSE_values)

# RMSE and R2 Scores grid plots
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(8.2,7.5))
fig.subplots_adjust(hspace=0.2, wspace=0.35)  # Adjust vertical space between subplots
n = 0
for i in [0,1,2]: # loop through the areas after terms have been looped
    for j in [0,1]: # loop through the terms for each area first
        ax1 = axs[i,j]
        ax1.plot(list(range(1,len(R2_alldata[n])+1)),R2_alldata[n],label='R^2',color='purple')
        ax2 = ax1.twinx()
        ax2.plot(list(range(1,len(RMSE_alldata[n])+1)),RMSE_alldata[n], label='RMSE',color='red')
        ax1.axvspan(7,12,alpha=0.2,color = 'orange')
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        if j == 1:
            ax1.set_xlim(1,12)
        elif j == 0:
            ax1.set_xlim(1,11)
        ax2.legend(lines + lines2, labels + labels2, loc='lower center',bbox_to_anchor=(0.44,0.4))
        axs[0,j].set_title(f"{term_names[j]} Test Set", fontsize=14, fontweight='bold', loc='center')
        ax1.grid(True)
        n = n+1
        
fig.text(0, 0.77, 'Main Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0, 0.497, 'Student Centre', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0, 0.22, 'Science Library', va='center', rotation='vertical', fontweight='bold', fontsize=14)

fig.text(0.5, 0.056, 'Weeks Trained (1 to x)', ha='center', fontsize=14)
fig.text(0.975, 0.5, 'RSME Score', va='center', rotation='vertical',fontsize=14)
fig.text(0.04, 0.5, 'R^2 Score', va='center', rotation='vertical',fontsize=14)

fig.text(0.83,0.765,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')
fig.text(0.83,0.49,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')
fig.text(0.83,0.225,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')

fig.text(0.38,0.765,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')
fig.text(0.38,0.51,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')
fig.text(0.38,0.225,"'Reading\nWeek'\nincluded",fontsize=10,ha='center',va='center',color='#d46402')

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/ML Results/Test Rest/Scores/RMSE and R2 Scores (Grid).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
