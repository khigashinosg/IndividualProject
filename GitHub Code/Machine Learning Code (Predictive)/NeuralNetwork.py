# Import libraries
import torch
import pandas as pd
from datetime import datetime, timedelta

# Data pathnames
data_path = [
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Main Library Pre-processed.xlsx', # Main Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Student Centre Pre-processed.xlsx', # Student Centre (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 1/Science Library Pre-processed.xlsx', # Science Library (Term 1)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Main Library Pre-processed.xlsx', # Main Library (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Student Centre Pre-processed.xlsx', # Student Centre (Term 2)
    '/Users/kyhi2018/Desktop/Individual Project/Pre-processed ML data/Term 2/Science Library Pre-processed.xlsx', # Science Library (Term 2)
    ]

# Define neural network
class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = torch.nn.Linear(5, 8)   # hidden layer
        self.linear2 = torch.nn.Linear(8, 8)
        self.linear3 = torch.nn.Linear(8, 8)
        self.output = torch.nn.Linear(8, 1)   # output layer

    def forward(self, x):
        for layer in self.children()[0:-1]:
            x = torch.relu(layer(x))
        x = self.output(x)
        return x
    
# Train the network
net = Net()
print(net)  # net architecture

# Define optimizer and loss function
optimizer = torch.optim.SGD(net.parameters(), lr=0.2)
loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss

# Start training
data = pd.read_excel(data_path[0])
train_end = datetime(2022,11,11) # change date to end of training period
test_start = train_end + timedelta(days=1) # test period is 1 day after train period ends

x_train = torch.Tensor(data.set_index('Occurrence Time')[:train_end.date()].iloc[:,1:-2])
x_test = torch.Tensor(data.set_index('Occurrence Time')[test_start.date():].iloc[:,1:-2])
y_train = torch.Tensor(data.set_index('Occurrence Time')[:train_end.date()].iloc[:,0])
y_test = torch.Tensor(data.set_index('Occurrence Time')[test_start.date():].iloc[:,0])

for t in range(100):
    prediction = net(x_train)     # input x and predict based on x

    loss = loss_func(prediction, y_train)     # must be (1. nn output, 2. target)

    optimizer.zero_grad()   # clear gradients for next train
    loss.backward()         # backpropagation, compute gradients
    optimizer.step()        # apply gradients
    
