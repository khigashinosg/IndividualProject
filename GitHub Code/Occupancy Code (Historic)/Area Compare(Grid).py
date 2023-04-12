import matplotlib.pyplot as plt
import pandas as pd
from operator import indexOf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

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
    'Main Library'
]

term_names = [
    'Term 1',
    'Term 2'
]

# Customisable options
fs = 12         # fontsize
figsizex = 8.2  # figure width
figsizey = 11.1  # figure length
dotsize = 2     # dot size for scatterplots
plot_data = []

for area_select in [0,1,2,3,4,5]: # this loops code for specific datasets according to 'area_names'
    # Import and data
    import_data = pd.read_excel(data_path[area_select]) # any data path works
    import_data = import_data.rename(columns={'Counter':area_names[area_select]})
    all_data = import_data[['Occurrence Time','Main Library','Student Centre','Science Library']]
    
    if area_select in [0,3,2,5]: # select data only for ML opening hours
        relevant_data = all_data[['Occurrence Time','Main Library','Student Centre','Science Library']][all_data['Occurrence Time'].dt.time >= pd.Timestamp('08:30:00').time()]
    elif area_select in []: # select data only for SC opening hours
        relevant_data = all_data[['Occurrence Time','Main Library','Student Centre','Science Library']]
    elif area_select in [1,4]: # select data only for SL opening hours
        # Create a mask to select all times except for Sat 21:00 to Sun 11:00 
        mask1 = ~((all_data['Occurrence Time'].dt.weekday == 5) & (all_data['Occurrence Time'].dt.hour >= 21) & (all_data['Occurrence Time'].dt.hour < 24) | (all_data['Occurrence Time'].dt.weekday == 6) & (all_data['Occurrence Time'].dt.hour >= 0) & (all_data['Occurrence Time'].dt.hour < 11))
        # Create a mask to select all times except for Sun 21:00 to Mon 08:45 
        mask2 = ~((all_data['Occurrence Time'].dt.weekday == 6) & (all_data['Occurrence Time'].dt.hour >= 21) & (all_data['Occurrence Time'].dt.hour < 24) | (all_data['Occurrence Time'].dt.weekday == 0) & (all_data['Occurrence Time'].dt.hour >= 0) & (all_data['Occurrence Time'].dt.hour < 8) & (all_data['Occurrence Time'].dt.minute < 45))
        # Apply the masks to the DataFrame to select all times except for the specified periods
        relevant_data = all_data[['Occurrence Time','Main Library','Student Centre','Science Library']].loc[mask1 & mask2]
    
    # Normalise data
    norm_data = scaler.fit_transform(np.array(relevant_data[['Main Library','Student Centre','Science Library']]))
    norm_data = pd.DataFrame(norm_data)
    norm_data = norm_data.rename(columns={0:relevant_data.columns[1],1:relevant_data.columns[2],2:relevant_data.columns[3]}) 
    
    plot_data.append(norm_data)
    
n = 0 # counts how many loops the subplot function has been through
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(figsizex,figsizey)) # establish subplot grid
fig.subplots_adjust(hspace=0.28, wspace=0.28)

for j in [0,1]: # loop through the terms
    for i in [0,1,2]: # loop through the areas
        # Line of perfect correlation
        axs[i,j].plot([0,1],[0,1],c='red',label = 'Line of perfect\ncorrelation')
        
        # Occupancy Data
        axs[i,j].scatter(plot_data[n][area_names[n]],plot_data[n][area_names[n+1]],s=dotsize)
        print([area_names[n]],[area_names[n+1]])
        
        # Line of best fit
        p1 = np.polyfit(plot_data[n][area_names[n]],plot_data[n][area_names[n+1]],2)
        x= np.linspace(0,1,100)
        y= p1[0]*x**2+p1[1]*x+p1[2]
        axs[i,j].plot(x,y,color='orange',label = 'line of best fit',linewidth=3)
        
        # Outliers
        residuals = plot_data[n][area_names[n+1]] - np.polyval(p1,plot_data[n][area_names[n]])
        outlier_threshold = 2.5 * np.std(residuals)
        axs[i,j].scatter(plot_data[n][area_names[n]][np.abs(residuals) > outlier_threshold], plot_data[n][area_names[n+1]][np.abs(residuals) > outlier_threshold], color='#02f543', label='Outliers',s=dotsize)
        
        axs[0,j].set_title(f"{term_names[j]}", fontsize=14, fontweight='bold', loc='center')
        axs[i,j].set_xlabel(f'{area_names[n]} (Normalised)')
        axs[i,j].tick_params(axis='y', labelright=True, labelleft=False, left= False, right=True)
        axs[i,j].set_ylabel(f'{area_names[n+1]} (Normalised)')
        axs[i,j].yaxis.set_label_position("right")
        axs[i,j].grid(True)
        axs[i,j].set_ylim(0,1)
        if i == 1:
            axs[i,j].legend([ 'Line of perfect\ncorrelation','Inliers','Line of best fit','Outliers'],loc='upper left',fontsize=8)
        else:
            axs[i,j].legend([ 'Line of perfect\ncorrelation','Inliers','Line of best fit','Outliers'],loc='lower right',fontsize=8)
        n = n + 1
        

fig.text(0.085, 0.77, 'ML vs SC', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.497, 'SC vs SL', va='center', rotation='vertical', fontweight='bold', fontsize=14)
fig.text(0.085, 0.22, 'SL vs ML', va='center', rotation='vertical', fontweight='bold', fontsize=14)

plt.savefig(f'/Users/kyhi2018/Desktop/Individual Project/Python Plots/Relative Occupancy Comparison/AllAreasAndTerms (Grid).png',bbox_inches='tight',dpi=200) # saves all figures in specified folder
fig.clf()
