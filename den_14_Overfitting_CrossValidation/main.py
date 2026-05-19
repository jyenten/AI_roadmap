
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

print(" === Day 14: Overfitting and Cross-validation === ")

df = pd.read_csv("titanic.csv")
df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

features = ["Pclass", "Sex", "Age", "Fare"]
x = df[features]
y = df["Survived"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

simple_model = DecisionTreeClassifier(max_depth=3)
simple_model.fit(x_train, y_train)

complex_model = DecisionTreeClassifier(max_depth=20)
complex_model.fit(x_train, y_train)

print("Simple model:")
print(f"Train accuracy: {round(accuracy_score(y_train, simple_model.predict(x_train)), 2)}")
print(f"Test accuracy:  {round(accuracy_score(y_test, simple_model.predict(x_test)), 2)}")


print("Complex model: ")
print(f"Train accuracy: {round(accuracy_score(y_train, complex_model.predict(x_train)), 2)}")
print(f"Test accuracy: {round(accuracy_score(y_test, complex_model.predict(x_test)), 2)}")


train_scores = []
test_scores = []
depths = range(1, 20)

for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth)
    model.fit(x_train, y_train)
    train_scores.append(accuracy_score(y_train, model.predict(x_train)))
    test_scores.append(accuracy_score(y_test, model.predict(x_test)))

plt.plot(depths, train_scores, label="Train accuracy")
plt.plot(depths, test_scores, label="Test accuracy")
plt.title("Overfitting visulization")
plt.xlabel("Tree Depth")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

model = DecisionTreeClassifier(max_depth=3)

cv_scores = cross_val_score(model, x, y, cv=5)

print(f"Cv scores: {cv_scores.round(2)}")
print(f"Mean CV score: {round(cv_scores.mean(), 2)}")
print(f"Std CV score:  {round(cv_scores.std(), 2)}")

models = {

    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree depth 3": DecisionTreeClassifier(max_depth=3),
    "Decision Tree depth 10": DecisionTreeClassifier(max_depth=10),
    "Decision Tree depth 20": DecisionTreeClassifier(max_depth=20) 
}

for name in models.items():
    scores = cross_val_score(model, x, y, cv=5)
    print(f"{name}: {round(scores.mean(), 2)} (+/- {round(scores.std(), 2)})")


