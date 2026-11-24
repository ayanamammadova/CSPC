import os
from ucimlrepo import fetch_ucirepo

os.makedirs("data", exist_ok=True)
concrete = fetch_ucirepo(id=165) # 165 = this dataset’s UCI id

X = concrete.data.features
y = concrete.data.targets

print("METADATA:")
print(concrete.metadata)

print("\nVARIABLES:")
print(concrete.variables)


# A2

X = X.copy()
X.columns = [
    "cement", "slag", "ash", "water",
    "superplastic", "coarse_agg", "fine_agg", "age"
]

y = y.iloc[:, 0].rename("strength")

print("\nNEW COLUMN NAMES:")
print(X.columns.tolist())

print("\nORIGINAL VARIABLE ORDER:")
print(concrete.variables["name"].tolist())

X.assign(strength=y).to_csv("data/concrete.csv", index=False)

print("\nDataset saved successfully!")