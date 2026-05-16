print("==== Day 9: Pandas =====")

import pandas as pd

data = {
    "name": ["Jan", "Anna", "Petr", "Lucie"],
    "grade": [1, 2, 4, 3],
    "age": [20, 21,19, 22]
}

df = pd.DataFrame(data)


print(df)
print(df.shape)
print(df.head(2))
print(df["grade"])
print(type(df["grade"]))

print(df["grade"].mean())
print(df["grade"].min())
print(df["grade"].max())
print(df["grade"].sum())
print(df["grade"].value_counts())

print(df.describe())

good_students = df[df["grade"] <= 2]
print(good_students)

filtered = df[(df["grade"] <= 2) & (df["age"] >= 21)]
print(filtered)

df["passing"] = df["grade"] <= 3

print(df)

def grade_label(grade):
    if grade == 1:
        return "excellent"
    elif grade <= 3:
        return "good"
    else:
        return "poor"
    
df["label"] = df["grade"].apply(grade_label)

print(df)

sorted_df = df.sort_values("grade")
print(sorted_df)

sorted_df_desc = df.sort_values("grade", ascending=False)
print(sorted_df_desc)

grouped = df.groupby("passing")["grade"].mean()
print(grouped)

df.to_csv("student.csv", index=False)
print("CSV saved.")

df_loaded = pd.read_csv("student.csv")
print(df_loaded)

print(df_loaded.shape)
print(df_loaded.head())
print(df_loaded.info())

data_with_missing = {
    "name": ["Jan", "Anna", "Petr", "Lucie",],
    "grade": [1, None, 4, 3],
    "age" : [20, 21, None, 22]
}

df_missing = pd.DataFrame(data_with_missing)

print(df_missing)
print(df_missing.isnull())
print(df_missing.isnull().sum())

df_missing["grade"].fillna(df_missing["grade"].mean(), inplace=True)
df_missing["age"].fillna(0, inplace=True)





