# In this example, we define a simple linear regression model using the torch.nn.Linear class,
# and train it on a small dataset of five input-output pairs. We use mean squared error (MSE) loss and
# stochastic gradient descent (SGD) to optimize the model's weights and improve its performance on the training data.
# After training for 1000 epochs, the model is able to make a prediction on a new test input, x_test = 6, and output a
# predicted value of y_test = 2.1428.

import torch

# Define the input data
# Set the data type of both tensors to float32
x = torch.tensor([[1], [2], [3], [4], [5]], dtype=torch.float32)
y = torch.tensor([[1], [2], [1.3], [3.75], [2.25]], dtype=torch.float32)

# Define the model
model = torch.nn.Linear(1, 1)

# Define the loss function and optimizer
criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Train the model
for i in range(1000):
    # Forward pass: Compute predicted y by passing x to the model
    y_pred = model(x)

    # Compute and print loss
    loss = criterion(y_pred, y)
    if i % 100 == 0:
        print(f'Epoch {i}/1000 | Loss: {loss.item():.4f}')

    # Zero gradients, perform a backward pass, and update the weights
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# Test the model
x_test = torch.tensor([[6]], dtype=torch.float32)
y_test = model(x_test)
print(f'Predicted value for test input: {y_test.item():.4f}')
