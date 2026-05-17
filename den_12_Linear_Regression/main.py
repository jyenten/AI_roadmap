import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("==== Day 12: Linear Regression ====")

np.random.seed(42)

study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
exam_scores = np.array([35, 45, 50, 60, 65, 70, 75, 85, 90, 95])

plt.scatter(study_hours, exam_scores)
plt.title("Surdz Hhours vs Exam Score")
plt.xlabel("Study hours")
plt.ylabel("Exam score")
plt.show()


from sklearn.linear_model import LinearRegression as lr
from sklearn.model_selection import train_test_split as tss

x = study_hours.reshape(-1, 1)
y = exam_scores

x_train, x_test, y_train, y_test = tss(x, y, test_size=0.2, random_state=42)

print(f"Training samples: {len(x_train)}")
print(f"Test samples: {len(x_test)}")

model = lr()
model.fit(x_train, y_train)

print(f"Coefficient: {round(model.coef_[0], 2)}")
print(f"Intercept: {round(model.intercept_, 2)}")

y_pred = model.predict(x_test)

print("Actual scores:", y_test)
print("Predicted scores:", y_pred.round(1))

from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {round(mse, 2)}")
print(f"R2 Score: {round(r2, 2)}")

X_line = np.linspace(1, 10, 100).reshape(-1, 1)
y_line = model.predict(X_line)

plt.scatter(study_hours, exam_scores, color="blue", label="Actual data")
plt.plot(X_line, y_line, color="red", label="Model prediction")
plt.title("Linear Regression")
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.legend()
plt.show()

new_student_hours = np.array([[7.5]])
predicted_score = model.predict(new_student_hours)

print(f"Student who studied 7.5 hours will score: {round(predicted_score[0], 1)}")