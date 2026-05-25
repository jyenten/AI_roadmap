import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import os

print("=== Day 19: Neural Network Classification ===")

script_dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(os.path.join(script_dir, "titanic.csv"))

df["Age"] = df["Age"].fillna(df["Age"]).mean()
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})


features = ["Pclass", "Sex", "Age", "Fare",]
x = df[features].values.astype(np.float32)
y = df["Survived"].values.astype(np.float32)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")

X_train_tensor = torch.tensor(X_train)
X_test_tensor = torch.tensor(X_test)
y_train_tensor = torch.tensor(y_train).view(-1, 1)
y_test_tensor = torch.tensor(y_test).view(-1, 1)

print(f"X_train_tensor shape: {X_train_tensor.shape}")
print(f"y_train_tensor shape: {y_train_tensor.shape}")



class TitanicNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(4, 16)
        self.layer2 = nn.Linear(16, 8)
        self.layer3 = nn.Linear(8, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.layer3(x))
        return x
    
model = TitanicNetwork()
print(model)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

losses = []

for epoch in range(1000):
    optimizer.zero_grad()

    y_pred = model(X_train_tensor)

    loss = criterion(y_pred, y_train_tensor)

    loss.backward()

    optimizer.step()

    losses.append(loss.item())

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

model.eval()
with torch.no_grad():
    y_pred_proba = model(X_test_tensor)
    y_pred = (y_pred_proba >= 0.5).float()

accuracy = accuracy_score(y_test, y_pred.numpy())
print(f"\nNeural Network Accuracy: {round(accuracy, 2)}")
print(classification_report(y_test, y_pred.numpy()))



from sklearn.ensemble import RandomForestClassifier

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(losses)
plt.title("Trainig Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.subplot(1, 2, 2)
model.eval()
with torch.no_grad():
    y_pred_proba = model(X_test_tensor).numpy()

plt.hist(y_pred_proba[y_test == 0], bins=20, alpha=0.5, label="Did not survive")
plt.hist(y_pred_proba[y_test == 1], bins=20, alpha=0.5, label="Survived")
plt.title("Predicted Probabilities")
plt.xlabel("Probability of Survival")
plt.ylabel("Count")
plt.legend()

plt.tight_layout()
plt.show()


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test))


print(f"\n==== Comparison ===")
print(f"Neural Network: {round(accuracy, 2)}")
print(f"Random Forest: {round(rf_accuracy, 2)}")