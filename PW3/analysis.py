import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1
print("\nPart 1")
df = pd.read_csv("heart.csv")

print("shape: ", df.shape)
print("first rows: ")
print(df.head())

columns = ["age", "chol", "trestbps", "thalach"]
print(df[columns].describe())

# 2
print("Part 2")
fig, axes = plt.subplots(2,2,figsize=(10,8))

for i, column in zip(axes.flat, columns):
    i.hist(df[column].dropna(), bins=20, edgecolor= "black")
    i.set_title(column)
    i.set_xlabel(column)
    i.set_ylabel("frequency")
    i.grid(True, alpha=0.3)


plt.tight_layout()
plt.savefig("heart_distributions.png")
plt.show()

# 3
print("\nPart 3")
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

for ax, column in zip(axes.flat, columns):
    data = df[column].dropna()

    stats.probplot(data, dist="norm", plot=ax)
    ax.set_title(f"Q-Q plot of {column}")
    ax.grid(alpha=0.3)

    W, p = stats.shapiro(data)

    print(f"\n{column}:")
    print(f"W       = {W:.4f}")
    print(f"p-value = {p:.6f}")

    if p < 0.05:
        print("\nnot normally distributed")
    else:
        print("\ninsufficient evidence against normality")
    print("")

plt.tight_layout()
plt.savefig("qq_plots.png")
plt.show()


# 4
print("\nPart 4")
healthy = df[df["target"] == 0]["thalach"].dropna()
disease = df[df["target"] == 1]["thalach"].dropna()

W1, p1 = stats.shapiro(healthy)
W2, p2 = stats.shapiro(disease)

print("")
print("healthy p value: ", p1)
print("disease p value: ", p2)

# comparision
print("")
if p1 >= 0.05 and p2 >= 0.05:
    t, p = stats.ttest_ind(healthy, disease, equal_var= False)
    print("welch's t-test")
else:
    t, p = stats.mannwhitneyu(healthy, disease, alternative = "two-sided")
    print("Mann-Whiteney U test")
print("test statistic: ", t)
print("p-value:        ", p)

print("")

if p < 0.05:
    print("groups differ significantly")
else: 
    print("no enough evidence that the group differ")

groups = [healthy, disease]
labels = ["healthy", "heart disease"]

means = [g.mean() for g in groups]
errors = [g.std(ddof=1) / np.sqrt(len(g)) for g in groups]

print("")

for label, group, mean, error in zip(labels, groups, means, errors):
    print(f"{label}:")
    print(f"n     = {len(group)}")
    print(f"mean  = {mean}")
    print(f"SE    = {error}\n")

print("")
plt.figure(figsize=(7, 5))
plt.bar(labels, means, yerr=errors, capsize=8, color=["skyblue", "pink"])
plt.ylabel("maximum heart rate")
plt.title("mean maximum heart rate with standard error")
plt.tight_layout()
plt.savefig("heart_rate_comparison.png")
plt.show()


# 5
print("\nPart 5")
print("")

data = df[["age", "thalach"]].dropna()

r, p = stats.pearsonr(data["age"], data["thalach"])

print("pearson correlation: ", r)
print("p-value:             ", p)
print("")

plt.figure(figsize=(7, 5))
plt.scatter(data["age"], data["thalach"], alpha=0.6)

x = data["age"]
y = data["thalach"]

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b, color="red", label="regression line")
plt.legend()
plt.xlabel("age")
plt.ylabel("maximum heart rate")
plt.title("age vs maximum heart rate")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("age_thalach.png")
plt.show()

# 6
print("\nPart 6")

print("")

chem = pd.read_csv("chemicals_cancer.csv")

print(chem.shape)
print(chem.head())
print(chem.columns)
print(chem.describe())
print("")

# initial correlations
print("")
for chemical in ["benzene", "cadmium"]:
    data = chem[[chemical, "malignancy"]].dropna()
    r, p = stats.pearsonr(data[chemical], data["malignancy"])

    print(f"\n{chemical}")
    print("number of observations: ", len(data))
    print("correlation:            ", r)
    print("p-value:                ", p)

print("")

# 7
print("\nPart 7")

print("")

subset = chem[(chem["pollution_index"] > 40) & (chem["pollution_index"] < 60)]

for chemical in ["benzene", "cadmium"]:
    data = subset[[chemical, "malignancy"]].dropna()

    r, p = stats.pearsonr(data[chemical], data["malignancy"])

    print(f"\n{chemical} (pollution range 40–60)")
    print("number of patients: ", len(data))
    print("correlation:        ", r)
    print("p-value:            ", p)

print("")


# bonus, entropy of target

print("\nBonus part")
proportions = df["target"].value_counts(normalize=True)

entropy = -np.sum(proportions * np.log2(proportions))

print("target proportions:")
print(proportions)

print("")

print("entropy:", entropy, "bits")