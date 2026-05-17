import pandas as pd
import matplotlib.pyplot as plt

print("===== Day 11: Matplotlib =====")

categories = ["Jan", "Anna", "Petr", "Lucie", ]
grades = [1, 2, 4, 3]

plt.bar(categories, grades)
plt.title("Student Grade")
plt.xlabel("Student")
plt.ylabel("Grade")
#plt.show()

plt.bar(categories, grades, color=["green", "green", "red", "orange", ])
plt.title("Student Grades by Color")
plt.xlabel("Grade")
plt.ylim(0, 5)
#plt.show()

months = [1, 2, 3, 4, 5, 6]
scores = [60, 65, 70, 68, 75, 80]

plt.plot(months, scores)
plt.title("Student progress")
plt.xlabel("Month")
plt.ylabel("Score")
plt.grid(True)
#plt.show()

ages = [20, 21, 19, 22, 20, 23, 21, 19, 24, 20, 22, 21]

plt.hist(ages, bins=5)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
#plt.show()


study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
exam_scores = [40, 50, 55, 65, 70, 75, 85, 90]

plt.scatter(study_hours, exam_scores)
plt.title("Study hours vs Exam Score")
plt.xlabel("Study hours")
plt.ylabel("Exam scores")
#plt.show()

fig, axes = plt.subplots(2, 2, figsize =(10, 8))

axes[0, 0].bar(categories, grades)
axes[0, 0].set_title("Grades")

axes[0, 1].plot(months, scores)
axes[0, 1].set_title("Progress")

axes[1, 0].hist(ages, bins=5)
axes[1, 0].set_title("Age of Distribution")

axes[1, 1].scatter(study_hours, exam_scores)
axes[1, 1].set_title("Study vs Score")

#plt.tight_layout()
#plt.show()


df = pd.read_csv("titanic.csv")
df["Age"] = df["Age"].fillna(df["Age"].mean())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

survival_counts = df["Survived"].value_counts()
axes[0].bar(["Did not survive", "Survived"], survival_counts.values)
axes[0].set_title("Survival Count")
axes[0].set_ylabel("Count")


axes[1].hist(df["Age"], bins=20)
axes[1].set_title("Age Distribution")
axes[1].set_xlabel("Age")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.show()

survival_by_sex = df.groupby("Sex")["Survived"].mean()

plt.bar(survival_by_sex.index, survival_by_sex.values)
plt.title("Survival Rate by Gender")
plt.xlabel("Gender")
plt.ylabel("Survival Rate")
plt.ylim(0, 1)
plt.show()

