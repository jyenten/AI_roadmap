import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


print("==== Day 17: House Price Prediction ====")

script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, "kc_house_data.csv"))

print(df.shape)
print(df.head())
print(df.info())
print(df.describe())

print("\n=== Missing Values ===")
print(df.isnull().sum())

print(f"Min price: ${df['price'].min():,.0f}")
print(f"Max price: ${df['price'].max():,.0f}")
print(f"Mean price: ${df['price'].mean():,.0f}")
print(f"Median price: ${df['price'].median():,.0f}")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(df["price"], bins=50)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")

plt.subplot(1, 2, 2)
plt.hist(np.log(df["price"]), bins=50)
plt.title("Log price Distribution")
plt.xlabel("Log price")
plt.ylabel("Count")

plt.tight_layout()
plt.show


print("\n=== Feature Engineering ===")

df["house_age"] = 2024 - df["yr_built"] 
df["renovated"] = (df["yr_renovated"] > 0).astype(int)
df["price_per_sqft"] = df["price"] / df["sqft_living"]

features = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot",
    "floors", "waterfront", "view", "condition", "grade",
    "sqft_above", "sqft_basement", "house_age", "renovated"
]

X = df[features]
y = df["price"]

print(f"Features: {features}")
print(f"Shape: {X.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")


lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("\n=== Model Results ====")

for name, model in[("Linear Refression", lr_model), ("Random forest", rf_model)]:
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f"{name}:")
    print(f"    R2: {round(r2, 3)}")
    print(f"    RMSE: ${rmse:,.0f}")


y_pred_rf = rf_model.predict(X_test)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred_rf, alpha=0.3)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red")
plt.title("Actual vs Predicted price")
plt.xlabel("Actual Price")
plt.ylabel("Predicted price")

plt.subplot(1, 2, 2)
feature_importance = pd.DataFrame({
    "feature": features,
    "importance": rf_model.feature_importances_
}).sort_values("importance", ascending=True)

plt.barh(feature_importance["feature"], feature_importance["importance"])
plt.title("Feature Importance")
plt.xlabel("Importance")

plt.tight_layout()
plt.show()

print("\n === Predict New House ===")

new_house = pd.DataFrame({
    "bedrooms": [3],
    "bathrooms": [2],
    "sqft_living": [3000],
    "sqft_lot": [5000],
    "floors": [1],
    "waterfront": [1],
    "view": [4],
    "condition": [3],
    "grade": [10],
    "sqft_above": [1800],
    "sqft_basement": [0],
    "house_age": [20],
    "renovated": [0]
})

predicted_price = rf_model.predict(new_house)
print(f"Predicted price: ${predicted_price[0]:,.0f}")

print("\n=== Our New House vs Similar Test Houses ===")

new_house_price = rf_model.predict(new_house)[0]

similar = X_test.copy()
similar["actual_price"] = y_test.values
similar["predicted_price"] = rf_model.predict(X_test).round(0)

similar = similar[
   (similar["bedrooms"] == 3) &
   (similar["bathrooms"] == 2) &
   (similar["sqft_living"].between(1600, 2000))
]

print(f"Our house predicted price: ${new_house_price:,.0f}")
print(f"\nSimiliar houses in test data:")
print(similar[["bedrooms", "bathrooms", "sqft_living", "actual_price", "predicted_price"]].head(10))
print(f"\nAverage actual price of similar houses: ${similar['actual_price'].mean():,.0f}")



