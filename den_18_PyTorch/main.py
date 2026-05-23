import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

print("=== Day 18: Neural network with PyTorch ====")

x = torch.tensor([1.0, 2.0, 3.0, 3.0, 4.0, 5.0])

print(x)
print(x.dtype)
print(x.shape)

a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([4.0, 5.0, 6.0])

print(a + b)
print(a * b)
print(torch.dot(a, b))

matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(matrix)
print(matrix.shape)

class SimpleNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(1, 16)
        self.layer2 = nn.Linear(16, 8)
        self.layer3 = nn.Linear(8,1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.layer3(x)
        return x
    
model = SimpleNetwork()
print(model)

np.random.seed(42)
x_train = np.linspace(0, 10, 100).reshape(-1, 1).astype(np.float32)
y_train = 2 * x_train + 1 + np.random.randn(100, 1).astype(np.float32)

X_tensor = torch.tensor(x_train)
y_tensor = torch.tensor(y_train)
y_tensor = y_tensor.view(-1, 1)

plt.scatter(x_train, y_train, alpha=0.5)
plt.title("Training Data")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

losses = []


for epoch in range(1000):
    optimizer.zero_grad()

    y_pred = model(X_tensor)

    loss = criterion(y_pred, y_tensor)

    loss.backward()

    optimizer.step()

    losses.append(loss.item())

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")


plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(losses)
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
    
plt.subplot(1, 2, 2)
model.eval()
with torch.no_grad():
    y_pred = model(X_tensor)

plt.scatter(x_train, y_train, alpha=0.5, label="Actual Data")
plt.plot(x_train, y_pred.numpy(), color="red", label="Model prediction")
plt.title("Neural Network Prediction")
plt.xlabel("X")
plt.ylabel("Y")

plt.tight_layout()
plt.show()
