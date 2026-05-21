import numpy as np
import  pandas  as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

print(" ==== Day 15: Random Forest ===")

df = pd.read_csv("titanic.csv")
df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

features = ["Pclass", "Sex", "Age", "Fare"]
X = df[features]
y = df["Survived"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_model = DecisionTreeClassifier(max_depth=3,random_state=42)
dt_model.fit(X_train, y_train)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)



print("Decision Tree: ")
print(f"    Train accuracy: {round(accuracy_score(y_train, dt_model.predict(X_train)), 2)}")
print(f"    Test accuracy : {round(accuracy_score(y_test, dt_model.predict(X_test)), 2)}")

print("Random Forest: ")
print(f"    Train accuracy: {round(accuracy_score(y_train, rf_model.predict(X_train)), 2)}")
print(f"    Test accuracy: {round(accuracy_score(y_test, rf_model.predict(X_test)), 2)}")

feature_importance = pd.DataFrame({
    "feature": features,
    "importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values("importance", ascending=True)

plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.title("Random forest Feature Importance")
plt.xlabel("Importance")
plt.show

n_trees = [1, 5, 10, 20, 50, 100, 200]
test_scores = []

for n in n_trees:
    model = RandomForestClassifier(n_estimators=n, random_state=42)
    model.fit(X_train, y_train)
    test_scores.append(accuracy_score(y_test, model.predict(X_test)))


plt.plot(n_trees, test_scores, marker="o")
plt.title("Number of Trees vs Accuracy")
plt.xlabel("Number of Trees")
plt.ylabel("Test Accuracy")
plt.show()

models = {
    "Decision Tree depth 3": DecisionTreeClassifier(max_depth=3, random_state=42),
    "Decision Tree depth 10": DecisionTreeClassifier(max_depth=10, random_state=42),
    "Random Forest 10 trees": RandomForestClassifier(n_estimators=10, random_state=42),
    "Random Forest 100 trees": RandomForestClassifier(n_estimators=100, random_state=42)
}

for name, model in models.time():
    scores = cross_val_score(model, X< y, cv=5)
    print(f"{name}")
    print(f"    Mean: {round(scores.mean(), 2)}")
    print(f"    Std: {round(scores.std(), 2)}")


