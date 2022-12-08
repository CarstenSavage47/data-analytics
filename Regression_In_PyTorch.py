import inputs as inputs
import torch

# Define the input data
x = torch.tensor([[1], [2], [3], [4], [5]])
y = torch.tensor([[1], [2], [1.3], [3.75], [2.25]])

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
x_test = torch.tensor([[6]])
y_test = model(x_test)
print(f'Predicted value for test input: {y_test.item():.4f}')
