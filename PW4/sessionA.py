import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import os
from sklearn.inspection import permutation_importance

df = pd.read_csv("data/concrete.csv")

X = df.drop(columns="strength")
y = df["strength"]


print(df.head())
print("\nDataset shape:", df.shape)
print("\nColumn names:", df.columns.tolist())

print("Number of duplicates:", df.duplicated().sum())

print("\nMissing values:")
print(df.isna().sum())

df = df.dropna()
df = df.drop_duplicates().reset_index(drop=True)

X = df.drop(columns="strength")
y = df["strength"]


print("\nDataset statistics:")
print(df.describe())


plt.scatter(df["cement"], df["strength"])
plt.xlabel("Cement (kg/m³)")
plt.ylabel("Strength (MPa)")
plt.title("Concrete Strength vs Cement")
plt.show()


plt.scatter(df["age"], df["strength"])
plt.xlabel("Age (days)")
plt.ylabel("Strength (MPa)")
plt.title("Concrete Strength vs Age")
plt.show()

# A3

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

print("\nTraining target size:", y_train.shape)
print("Testing target size:", y_test.shape)


# A4

model = LinearRegression()
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

test_mae = mean_absolute_error(y_test, y_test_pred)

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

n = len(X_train)
p = X_train.shape[1]

train_adj_r2 = 1 - (1 - train_r2) * (n - 1) / (n - p - 1)

print("\nLinear Regression Results:")
print("Train RMSE:", train_rmse)
print("Test RMSE:", test_rmse)
print("Test MAE:", test_mae)
print("Train R2:", train_r2)
print("Train Adjusted R2:", train_adj_r2)
print("Test R2:", test_r2)

print("\nIntercept:", model.intercept_)

for name, coef in zip(X.columns, model.coef_):
    print(name, "coefficient:", coef)


residuals = y_test - y_test_pred

plt.scatter(X_test["age"], residuals)
plt.xlabel("Age (days)")
plt.ylabel("Residuals (MPa)")
plt.title("Test Residuals vs Age")
plt.xscale("log")
plt.axhline(y=0, linestyle="--")
plt.show()


# A5

results = []

for degree in [1, 2, 3, 4]:

    poly = make_pipeline(
        PolynomialFeatures(degree=degree, include_bias=False),
        StandardScaler(),
        LinearRegression()
    )
    poly.fit(X_train, y_train)

    y_train_pred = poly.predict(X_train)
    y_test_pred = poly.predict(X_test)

    p = poly[0].n_output_features_

    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    n = len(X_train)
    train_adj_r2 = 1 - (1 - train_r2) * (n - 1) / (n - p - 1)

    results.append({
        "Degree": degree,
        "Features (p)": p,
        "Train RMSE": train_rmse,
        "Test RMSE": test_rmse,
        "Train R2": train_r2,
        "Train Adjusted R2": train_adj_r2,
        "Test R2": test_r2
    })

results_df = pd.DataFrame(results)

print("\nPolynomial Regression Results:")
print(results_df.to_string(index=False))

# A6 — Classification

y_class = (df["strength"] >= 40).astype(int)

print("\nClass proportions:")
print(y_class.value_counts(normalize=True))

Xc_train, Xc_test, c_train, c_test = train_test_split(
    X, y_class,
    test_size=0.2,
    random_state=42,
    stratify=y_class
)

# KNN: test different values of K

K_values = [1, 3, 5, 7, 15, 25, 51, 101]

knn_results = []

for K in K_values:
    knn = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=K)
    )

    knn.fit(Xc_train, c_train)

    train_accuracy = knn.score(Xc_train, c_train)
    test_accuracy = knn.score(Xc_test, c_test)

    knn_results.append({
        "K": K,
        "Train Accuracy": train_accuracy,
        "Test Accuracy": test_accuracy
    })

knn_results_df = pd.DataFrame(knn_results)

print("\nKNN Results:")
print(knn_results_df.to_string(index=False))

# Plot accuracies
plt.plot(K_values, knn_results_df["Train Accuracy"],
         marker="o", label="Train Accuracy")
plt.plot(K_values, knn_results_df["Test Accuracy"],
         marker="o", label="Test Accuracy")

plt.xscale("log")
plt.xlabel("K")
plt.ylabel("Accuracy")
plt.title("KNN Accuracy for Different K Values")
plt.legend()
plt.grid()
plt.show()

chosen_K = int(
    knn_results_df.loc[
        knn_results_df["Test Accuracy"].idxmax(), "K"
    ]
)

knn_scaled = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=chosen_K)
)

knn_scaled.fit(Xc_train, c_train)
scaled_accuracy = knn_scaled.score(Xc_test, c_test)

knn_unscaled = KNeighborsClassifier(n_neighbors=chosen_K)
knn_unscaled.fit(Xc_train, c_train)
unscaled_accuracy = knn_unscaled.score(Xc_test, c_test)

print("\nKNN Scaling Comparison:")
print("With scaling:", scaled_accuracy)
print("Without scaling:", unscaled_accuracy)


split_accuracies = []

for random_state in range(5):
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
        X, y_class,
        test_size=0.2,
        random_state=random_state,
        stratify=y_class
    )

    knn = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=chosen_K)
    )

    knn.fit(X_train_split, y_train_split)
    accuracy = knn.score(X_test_split, y_test_split)

    split_accuracies.append(accuracy)

print("\nKNN Accuracy for Five Splits:")
print(split_accuracies)
print("Minimum:", min(split_accuracies))
print("Maximum:", max(split_accuracies))
print("Spread:", max(split_accuracies) - min(split_accuracies))


depth_values = [1, 2, 3, 4, 5, 6, 8, None]

tree_results = []

for depth in depth_values:
    tree = DecisionTreeClassifier(
        criterion="entropy",
        max_depth=depth,
        min_samples_leaf=1,
        random_state=0
    )

    tree.fit(Xc_train, c_train)

    train_accuracy = tree.score(Xc_train, c_train)
    test_accuracy = tree.score(Xc_test, c_test)

    tree_results.append({
        "Depth": str(depth),
        "Leaves": tree.get_n_leaves(),
        "Train Accuracy": train_accuracy,
        "Test Accuracy": test_accuracy
    })

tree_results_df = pd.DataFrame(tree_results)

print("\nDecision Tree Results:")
print(tree_results_df.to_string(index=False))

positions = range(len(depth_values))

plt.plot(positions, tree_results_df["Train Accuracy"],
         marker="o", label="Train Accuracy")
plt.plot(positions, tree_results_df["Test Accuracy"],
         marker="o", label="Test Accuracy")

plt.xticks(positions, [str(d) for d in depth_values])
plt.xlabel("Maximum Depth")
plt.ylabel("Accuracy")
plt.title("Decision Tree Accuracy for Different Depths")
plt.legend()
plt.grid()
plt.show()



final_tree = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=chosen_depth,
    min_samples_leaf=1,
    random_state=0
)

final_tree.fit(Xc_train, c_train)

print("\nChosen Tree:")
print("Depth:", final_tree.get_depth())
print("Number of leaves:", final_tree.get_n_leaves())
print("Train accuracy:", final_tree.score(Xc_train, c_train))
print("Test accuracy:", final_tree.score(Xc_test, c_test))

print("\nTop Two Levels of the Tree:")
print(export_text(
    final_tree,
    feature_names=list(X.columns),
    max_depth=2
))


# A7

knn_pred = knn_scaled.predict(Xc_test)
tree_pred = final_tree.predict(Xc_test)
models = {
    "KNN": knn_pred,
    "Decision Tree": tree_pred
}

metrics_results = []

for name, predictions in models.items():

    tn, fp, fn, tp = confusion_matrix(
        c_test, predictions, labels=[0, 1]
    ).ravel()

    metrics_results.append({
        "Model": name,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "Accuracy": accuracy_score(c_test, predictions),
        "Precision": precision_score(c_test, predictions, zero_division=0),
        "Recall": recall_score(c_test, predictions, zero_division=0),
        "F1": f1_score(c_test, predictions, zero_division=0)
    })

metrics_df = pd.DataFrame(metrics_results)

print("\nA7 — Classification Metrics:")
print(metrics_df.to_string(index=False))

os.makedirs("results", exist_ok=True)
metrics_df.to_csv("results/A metrics.csv", index=False)

print("\nMetrics saved to results/A metrics.csv")

probabilities = knn_scaled.predict_proba(Xc_test)[:, 1]

thresholds = [0.3, 0.5, 0.7, 0.9]

threshold_results = []

for threshold in thresholds:

    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        c_test, predictions, labels=[0, 1]
    ).ravel()

    precision = precision_score(
        c_test, predictions, zero_division=0
    )

    recall = recall_score(
        c_test, predictions, zero_division=0
    )

    threshold_results.append({
        "Threshold": threshold,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "Precision": precision,
        "Recall": recall
    })

threshold_df = pd.DataFrame(threshold_results)

print("\nKNN Threshold Comparison:")
print(threshold_df.to_string(index=False))


# A8

raw_coefficients = model.coef_

standard_model = make_pipeline(
    StandardScaler(),
    LinearRegression()
)

standard_model.fit(X_train, y_train)

standard_coefficients = standard_model[-1].coef_

tree_importances = final_tree.feature_importances_

knn_permutation = permutation_importance(
    knn_scaled,
    Xc_test,
    c_test,
    scoring="f1",
    n_repeats=20,
    random_state=0
)

tree_permutation = permutation_importance(
    final_tree,
    Xc_test,
    c_test,
    scoring="f1",
    n_repeats=20,
    random_state=0
)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Raw Coefficient": raw_coefficients,
    "Standardised Coefficient": standard_coefficients,
    "Tree Importance": tree_importances,
    "KNN Permutation": knn_permutation.importances_mean,
    "KNN Permutation Std": knn_permutation.importances_std,
    "Tree Permutation": tree_permutation.importances_mean,
    "Tree Permutation Std": tree_permutation.importances_std
})

print("\nA8 — Feature Importance:")
print(importance_df.to_string(index=False))

plt.figure(figsize=(10, 5))
plt.bar(importance_df["Feature"],
        importance_df["Standardised Coefficient"])

plt.xlabel("Feature")
plt.ylabel("Standardised Coefficient")
plt.title("Standardised Linear Regression Coefficients")
plt.xticks(rotation=45)
plt.axhline(y=0, linestyle="--")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
plt.bar(importance_df["Feature"],
        importance_df["Tree Importance"])

plt.xlabel("Feature")
plt.ylabel("Importance")
plt.title("Decision Tree Feature Importance")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

x_positions = np.arange(len(importance_df))
width = 0.35

plt.figure(figsize=(10, 5))

plt.bar(x_positions - width/2,
        importance_df["KNN Permutation"],
        width, label="KNN")

plt.bar(x_positions + width/2,
        importance_df["Tree Permutation"],
        width, label="Decision Tree")

plt.xlabel("Feature")
plt.ylabel("Mean F1 Score Decrease")
plt.title("Permutation Importance")
plt.xticks(x_positions, importance_df["Feature"], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


# Bonus

X_physics = X.copy()

X_physics["age"] = np.log(X_physics["age"])

X_physics["water_binder_ratio"] = (
    df["water"] /
    (df["cement"] + df["slag"] + df["ash"])
)

X_physics = X_physics.drop(columns="water")

Xp_train, Xp_test, yp_train, yp_test = train_test_split(
    X_physics, y,
    test_size=0.2,
    random_state=42
)

physics_model = LinearRegression()
physics_model.fit(Xp_train, yp_train)

yp_test_pred = physics_model.predict(Xp_test)

physics_test_r2 = r2_score(yp_test, yp_test_pred)

print("\nPhysics-Informed Linear Regression:")
print("Number of features:", X_physics.shape[1])
print("Test R2:", physics_test_r2)

comparison_df = results_df[["Degree", "Features (p)", "Test R2"]].copy()
comparison_df["Model"] = comparison_df["Degree"].apply(
    lambda d: f"Polynomial degree {d}"
)
comparison_df = comparison_df.rename(
    columns={"Features (p)": "Number of Features"}
)
comparison_df = comparison_df[["Model", "Number of Features", "Test R2"]]

physics_row = pd.DataFrame([{
    "Model": "Physics-informed Linear Regression",
    "Number of Features": X_physics.shape[1],
    "Test R2": physics_test_r2
}])

comparison_df = pd.concat(
    [comparison_df, physics_row],
    ignore_index=True
)

print("\nPolynomial vs Physics-Informed Regression:")
print(comparison_df.to_string(index=False))