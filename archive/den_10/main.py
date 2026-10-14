import pandas as pd

print("===== Day 10: Titanic Dataset Analysis ====")

df = pd.read_csv("titanic.csv")

print(df.shape)
print(df.head())
print(df.info())

print(df.columns.tolist())
print(df.describe())

print(df.isnull().sum())

print(df["Survived"].value_counts())
print(df["Survived"].mean())

print(df.groupby("Sex")["Survived"].mean())
print(df.groupby("Sex")["Survived"].count())


print(df.groupby("Pclass")["Survived"].mean())
print(df.groupby("Pclass")["Survived"].count())

print(df.groupby(["Sex", "Pclass"])["Survived"].count())

print(df.groupby("Survived")["Age"].mean())

df["Age"] = df["Age"].fillna(df["Age"].mean())

print(df["Age"].isnull().sum())
print(df["Age"].mean())

def age_category(age):
    if age < 18:
        return "child"
    elif age < 60:
        return "adult"
    else:
        return "senior"
    
df["age_category"] = df["Age"].apply(age_category)

print(df["age_category"].value_counts())

print(df.groupby(age_category)["Survived"].mean())


print("\n===== SUMMARY =====")
print(f"Total passengers: {len(df)}")
print(f"Survival rate: {round(df['Survived'].mean() * 100, 1)}%")
print(f"Female survival rate: {round(df[df['Sex'] == 'female']['Survived'].mean() * 100, 1)}%")
print(f"Male survival rate: {round(df[df['Sex'] == 'male']['Survived'].mean() * 100, 1)}%")
print(f"1st class survival rate: {round(df[df['Pclass'] == 1]['Survived'].mean() * 100, 1)}%")
print(f"3rd class survival rate: {round(df[df['Pclass'] == 3]['Survived'].mean() * 100, 1)}%")
print(f"Children survival rate: {round(df[df['age_category'] == 'child']['Survived'].mean() * 100, 1)}%")