import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

print("==== Day 16: Feature Engineering ===")


df = pd.read_csv("titanic.csv")

print(df.head())
print(df.columns.tolist())

df["Age"] = df["Age"].fillna(df["Age"].mean())
df["Sex"] = df["Sex"].map({"male" : 0, "female": 1})

feature_baseline = ["Pclass", "Sex", "Age", "Fare",]
X_baseline = df[feature_baseline]
y = df["Survived"]

baseline_model = RandomForestClassifier(n_estimators=100, random_state=42)
baseline_scores = cross_val_score(baseline_model, X_baseline, y, cv=5)

print(f"Baseline score: {round(baseline_scores.mean(), 2)} (+/- {round(baseline_scores.std(), 2)})")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

print(df[["Name", "SibSp", "Parch", "FamilySize"]].head(10))

df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

print(df[["Name", "FamilySize", "IsAlone"]].head(10))
print(df.groupby("IsAlone")["Survived"].mean())

df["Title"] = df["Name"].str.extract(r" ([A-Za-z]+)\.")

print(df["Title"].value_counts())


tittle_mapping = {
    "Mr": "Mr",
    "Miss": "Miss",
    "Mrs": "Mrs",
    "Master": "Master"
}

df["Title"] = df["Title"].map(tittle_mapping).fillna("Other")

print(df["Title"].value_counts())
print(df.groupby("Title")["Survived"].mean())

title_encoding = {
    "Mr": 0,
    "Miss": 1,
    "Mrs": 2,
    "Master": 3,
    "Other": 4
}

df["Title"] = df["Title"].map(title_encoding)

print(df["Title"].value_counts())

features_new = ["Pclass", "Sex", "Age", "Fare", "FamilySize", "IsAlone", "Title"]
X_new = df[features_new]

new_model = RandomForestClassifier(n_estimators=100, random_state=42)
new_scores = cross_val_score(new_model, X_new, y, cv=5)

print(f"Baseline score: {round(baseline_scores.mean(), 2)} (+/- {round(baseline_scores.std(), 2)})")
print(f"New score: {round(new_scores.mean(), 2)} (+?/-{round(new_scores.std(), 2)})")




