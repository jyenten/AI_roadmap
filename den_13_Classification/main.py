import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split as tts






print("==== Day 13: Classfication ====")

df = pd.read_csv("titanic.csv")

df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Sex"] = df["Sex"].map({"male" : 0, "female" : 1})

features = ["Pclass" , "Sex", "Age", "Fare"]
x = df[features]
y = df["Survived"]

print(x.head())
print(f"Shape: {x.shape}")


from sklearn.linear_model import LogisticRegression  as lr
from sklearn.metrics import accuracy_score, classification_report

x_train, x_test, y_train, y_test = tts(x, y, test_size=0.2, random_state=42)

model = lr(max_iter=1000)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print(f"Accuracy: {round(accuracy_score(y_test, y_pred), 2)}")
print(classification_report(y_test, y_pred))

new_passenger = pd.DataFrame ({

    "Pclass" : [1],
    "Sex" : [1],
    "Age" : [30],
    "Fare" : [100]
})

prediction = model.predict(new_passenger)
probability = model.predict_proba(new_passenger)

print(f"Prediction: {'Survived' if prediction[0] == 1 else 'Did not survive'}")
print(f"Survival probability: {round(probability[0][1] * 100, 1)}%")

coefficients = pd.DataFrame({
    "feature": features,
    "coefficient": model.coef_[0]
})

coefficients = coefficients.sort_values("coefficient")

plt.barh(coefficients["feature"], coefficients["coefficient"])
plt.title("Feature Importance")
plt.xlabel("Coefficient")
plt.axvline(x=0, color="red", linestyle="--")
plt.show()



