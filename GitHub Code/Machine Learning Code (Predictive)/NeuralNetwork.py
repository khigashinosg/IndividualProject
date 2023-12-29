# Import libraries
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Data pathnames
data_path = [
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 1/Main Library Pre-processed.xlsx', # Main Library (Term 1)
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 1/Student Centre Pre-processed.xlsx', # Student Centre (Term 1)
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 1/Science Library Pre-processed.xlsx', # Science Library (Term 1)
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 2/Main Library Pre-processed.xlsx', # Main Library (Term 2)
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 2/Student Centre Pre-processed.xlsx', # Student Centre (Term 2)
    '/Users/kyhi2018/Desktop/IndividualProject/Pre-processed ML data/Term 2/Science Library Pre-processed.xlsx', # Science Library (Term 2)
    ]

# Define neural network
class Net(nn.Module):
    # Define the neural network architecture
    def __init__(self, nb_layers=9, nb_nodes=4):
        super().__init__()
        # Define the layers
        self.linear_layers = nn.ModuleList()
        for i in range(nb_layers):
            if i == 0: # first layer
                self.linear_layers.append(nn.Linear(5, nb_nodes))
            elif i == nb_layers - 1: # last layer
                self.linear_layers.append(nn.Linear(nb_nodes, 1))
            else: # hidden layers
                self.linear_layers.append(nn.Linear(nb_nodes, nb_nodes))

    def forward(self, x):
        # Every layer has a ReLU activation function, even the output layer
        for layer in self.linear_layers:
            x = nn.ReLU()(layer(x))
        return x

def preprocess_data(data):
    # Extract numerical columns for normalization
    numerical_columns = data.columns[2:7]

    # min-max standardise  each feature
    for column in numerical_columns:
        min_value = data[column].min()
        max_value = data[column].max()
        data[column] = (data[column] - min_value) / (max_value - min_value)

    return data

def train_test_split(data, train_end):
    # Select training and test periods
    train_end = datetime(2022,train_end[0],train_end[1]) # change date to end of training period
    test_start = train_end + timedelta(days=1) # test period is 1 day after train period ends

    # Split data into training and testing sets
    x_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,1:-2]
    x_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,1:-2]
    y_train = data.set_index('Occurrence Time')[:train_end.date()].iloc[:,0]
    y_test = data.set_index('Occurrence Time')[test_start.date():].iloc[:,0]
    
    # Convert to tensors
    x_train = torch.tensor(x_train.values).float()
    x_test = torch.tensor(x_test.values).float()
    y_train = torch.tensor(y_train.values).float()
    y_test = torch.tensor(y_test.values).float()
    
    return x_train, x_test, y_train, y_test

# Xavier/Glorot weight initialization
def init_weights_xavier(m):
    if type(m) == nn.Linear:
        nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)
        
# Random initialization function
def init_weights_random(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, mean=0.0, std=1.0)
        nn.init.normal_(m.bias, mean=0.0, std=1.0)

# Train the network
def train_net(model, x_train, y_train, optimiser = 'Adam', lr = 0.2, loss_func = 'MSE', steps = 1000):
    
    print(model)  # net architecture

    # Define optimizer and loss function
    if optimiser == 'Adam':
        optimizer = optim.Adam(model.parameters(), lr=lr)
    elif optimiser == 'SGD':
        optimizer = optim.SGD(model.parameters(), lr=lr)
    elif optimiser == 'RMSprop':
        optimizer = optim.RMSprop(model.parameters(), lr=lr)
        
    if loss_func == 'MSE':
        loss_func = nn.MSELoss() # this is for regression mean squared loss


    for t in range(steps):
        prediction = model(x_train)     # input x and predict based on x
        
        loss = loss_func(prediction.squeeze(), y_train)     # must be (1. nn output, 2. target)
        if t % 100 == 0:
            print(loss.item())

        optimizer.zero_grad()   # clear gradients for next train
        loss.backward()         # backpropagation, compute gradients
        optimizer.step()        # apply gradients
        
    print(f'Optimser: {optimiser}', f'learning rate: {lr}', f'Loss function: {loss_func}')
    
    return model, loss
    

if __name__ == '__main__':
    # Initialize the network
    model = Net()
    model.apply(init_weights_random) # initialize weights
    
    # Import data
    data = pd.read_excel(data_path[0])
    
    # Preprocess data
    data = preprocess_data(data)
    
    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data, train_end=(11,11))

    # Train the network
    model, loss = train_net(model, x_train, y_train, optimiser='Adam', lr=0.1, loss_func='MSE', steps=1000)
    print(loss.item())
    
    # Predict the target variable on the testing data
    model.eval()
    prediction = model(x_test)
    
    # Plot the results
    prediction = prediction.detach().numpy()
    y_test = y_test.detach().numpy()
    plt.scatter(prediction, y_test)
    #plt.show()
    
    print('Finished')
    
    
