import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)

# B1
wine = load_wine(as_frame=True)
X = wine.data.copy()
cultivar = wine.target.copy() 

print("\nB1: DATASET DESCRIPTION")
print(wine.DESCR)
print("\nShape:", X.shape)
print("\nDescriptive statistics:")
print(X.describe().round(3))
X.describe().to_csv("results/B descriptive statistics.csv")

ranges = X.max() - X.min()
stds = X.std()
scale_table = pd.DataFrame({"range": ranges, "standard_deviation": stds})
print("\nRanges and standard deviations:")
print(scale_table.sort_values("range", ascending=False).round(3))
scale_table.to_csv("results/B feature scales.csv")

# B2
pca_raw = PCA()
pca_raw.fit(X)

raw_ratio = pca_raw.explained_variance_ratio_
raw_pc1_loadings = pd.Series(
    pca_raw.components_[0], index=X.columns, name="PC1_loading_raw"
).sort_values(key=abs, ascending=False)

print("\nB2: RAW PCA")
print("PC1 explained variance ratio:", raw_ratio[0])
print("Raw PC1 loadings, sorted by absolute magnitude:")
print(raw_pc1_loadings.round(4))
raw_pc1_loadings.to_csv("results/B raw PC1 loadings.csv")

# B3
scaler = StandardScaler()
Z = scaler.fit_transform(X)

print("\nScaled means (approximately 0):")
print(pd.Series(Z.mean(axis=0), index=X.columns).round(6))
print("\nScaled standard deviations (approximately 1):")
print(pd.Series(Z.std(axis=0), index=X.columns).round(6))

pca = PCA()
scores = pca.fit_transform(Z)
ratios = pca.explained_variance_ratio_
cumulative = np.cumsum(ratios)

variance_table = pd.DataFrame({
    "component": [f"PC{i}" for i in range(1, len(ratios) + 1)],
    "explained_variance_ratio": ratios,
    "cumulative_variance": cumulative
})
print("\nB3: SCALED PCA VARIANCE")
print(variance_table.round(4).to_string(index=False))
variance_table.to_csv("results/B PCA variance.csv", index=False)

n_90 = int(np.argmax(cumulative >= 0.90) + 1)
pc12_variance = cumulative[1]
print("\nNumber of components needed for 90% variance:", n_90)
print("Variance retained by PC1-PC2 plane:", pc12_variance)

fig, ax = plt.subplots()
component_numbers = np.arange(1, len(ratios) + 1)
ax.bar(component_numbers, ratios, label="Individual variance")
ax.plot(component_numbers, cumulative, marker="o",
        label="Cumulative variance")
ax.axhline(0.90, linestyle="--", label="90%")
ax.set_xlabel("Principal component")
ax.set_ylabel("Explained variance ratio")
ax.set_title("PCA scree plot (scaled wine data)")
ax.legend()
fig.tight_layout()
fig.savefig("figures/B scree plot.png", dpi=150)
plt.close(fig)

loadings = pd.DataFrame(
    pca.components_[:2].T,
    index=X.columns,
    columns=["PC1", "PC2"]
)
pc1_sorted = loadings["PC1"].reindex(
    loadings["PC1"].abs().sort_values(ascending=False).index
)
pc2_sorted = loadings["PC2"].reindex(
    loadings["PC2"].abs().sort_values(ascending=False).index
)
print("\nPC1 loadings sorted by absolute magnitude:")
print(pc1_sorted.round(4))
print("\nPC2 loadings sorted by absolute magnitude:")
print(pc2_sorted.round(4))
loadings.to_csv("results/B PCA loadings.csv")

fig, ax = plt.subplots()
ax.scatter(scores[:, 0], scores[:, 1], alpha=0.8)
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("Wine samples on PC1-PC2 plane (unlabelled)")
fig.tight_layout()
fig.savefig("figures/B PCA scatter unlabelled.png", dpi=150)
plt.close(fig)

# B4
seed_rows = []
for seed in range(8):
    km_seed = KMeans(
        n_clusters=3, init="k-means++", n_init=1,
        max_iter=300, random_state=seed
    )
    km_seed.fit(Z)
    seed_rows.append({
        "random_state": seed,
        "inertia": km_seed.inertia_,
        "iterations": km_seed.n_iter_
    })

seed_table = pd.DataFrame(seed_rows)
print("\nB4(a): K=3, N_INIT=1, DIFFERENT RANDOM STATES")
print(seed_table.round(4).to_string(index=False))
seed_table.to_csv("results/B KMeans random seeds.csv", index=False)

inertias = []
for k in range(1, 11):
    km_k = KMeans(
        n_clusters=k, init="k-means++", n_init=10,
        max_iter=300, random_state=0
    )
    km_k.fit(Z)
    inertias.append(km_k.inertia_)

elbow_table = pd.DataFrame({"k": range(1, 11), "inertia": inertias})
print("\nB4(b): ELBOW TABLE")
print(elbow_table.round(4).to_string(index=False))
elbow_table.to_csv("results/B KMeans elbow.csv", index=False)

fig, ax = plt.subplots()
ax.plot(elbow_table["k"], elbow_table["inertia"], marker="o")
ax.set_xlabel("Number of clusters (k)")
ax.set_ylabel("Inertia")
ax.set_title("K-Means elbow method")
fig.tight_layout()
fig.savefig("figures/B KMeans elbow.png", dpi=150)
plt.close(fig)

chosen_k = 3
km = KMeans(
    n_clusters=chosen_k, init="k-means++", n_init=10,
    max_iter=300, random_state=0
)
km.fit(Z)
labels = km.labels_

# B5
cluster_sizes = pd.Series(
    np.bincount(labels), index=[f"Cluster {i}" for i in range(chosen_k)],
    name="number_of_wines"
)
centres_real = pd.DataFrame(
    scaler.inverse_transform(km.cluster_centers_),
    columns=X.columns,
    index=[f"Cluster {i}" for i in range(chosen_k)]
)

print("\nB5: CLUSTER SIZES")
print(cluster_sizes)
print("\nCluster centres in original measurement units:")
print(centres_real.round(3))
cluster_sizes.to_csv("results/B cluster sizes.csv")
centres_real.to_csv("results/B cluster centres.csv")

fig, ax = plt.subplots()
scatter = ax.scatter(scores[:, 0], scores[:, 1], c=labels, cmap="viridis")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_title("Wine samples on PC1-PC2 plane, coloured by K-Means cluster")
fig.colorbar(scatter, ax=ax, label="Cluster")
fig.tight_layout()
fig.savefig("figures/B PCA scatter by cluster.png", dpi=150)
plt.close(fig)

# B6

def agreement_score(true_labels, cluster_labels):
    table = pd.crosstab(true_labels, cluster_labels)
    return table.max(axis=0).sum() / len(true_labels), table

km_scaled = KMeans(
    n_clusters=3, init="k-means++", n_init=10,
    max_iter=300, random_state=0
).fit(Z)
agreement_scaled, crosstab_scaled = agreement_score(cultivar, km_scaled.labels_)

km_raw = KMeans(
    n_clusters=3, init="k-means++", n_init=10,
    max_iter=300, random_state=0
).fit(X)
agreement_raw, crosstab_raw = agreement_score(cultivar, km_raw.labels_)

pc12 = scores[:, :2]
km_pc12 = KMeans(
    n_clusters=3, init="k-means++", n_init=10,
    max_iter=300, random_state=0
).fit(pc12)
agreement_pc12, crosstab_pc12 = agreement_score(cultivar, km_pc12.labels_)

agreement_table = pd.DataFrame({
    "data_used": [
        "Scaled 13 measurements",
        "Raw 13 measurements",
        "First two scaled PCs"
    ],
    "agreement": [
        agreement_scaled,
        agreement_raw,
        agreement_pc12
    ]
})
print("\nB6: CULTIVAR VS CLUSTER — SCALED DATA")
print(crosstab_scaled)
print("\nCULTIVAR VS CLUSTER — RAW DATA")
print(crosstab_raw)
print("\nCULTIVAR VS CLUSTER — FIRST TWO PCs")
print(crosstab_pc12)
print("\nAGREEMENT COMPARISON")
print(agreement_table.round(4).to_string(index=False))

agreement_table.to_csv("results/B agreement.csv", index=False)
crosstab_scaled.to_csv("results/B crosstab scaled.csv")
crosstab_raw.to_csv("results/B crosstab raw.csv")
crosstab_pc12.to_csv("results/B crosstab PC1 PC2.csv")

print("\nSESSION B COMPLETE. Tables are in results/ and plots are in figures/.")
