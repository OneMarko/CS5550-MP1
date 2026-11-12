"""Table and plots from results.csv."""

import os

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results.csv")
df = df[df["status"] != "SKIP"].copy()
for col in ["cost", "nodes_expanded", "max_frontier", "iterations", "seconds"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

os.makedirs("figures", exist_ok=True)

# Table: one row per run, TIMEOUT rows kept.
table = df[["grid", "n_dirty", "algorithm", "heuristic", "status", "cost",
            "nodes_expanded", "max_frontier", "iterations", "seconds"]]
table = table.fillna("-")
table.to_csv("results_table.csv", index=False)
print(table.to_string(index=False))

# Plot 1: nodes expanded vs number of dirty cells.
fig, ax = plt.subplots(figsize=(7, 4.5))
lines = [("dfs", "-", "DFS"), ("astar", "h2", "A* (h2)"), ("idastar", "h2", "IDA* (h2)")]
for algorithm, heuristic, label in lines:
    sub = df[(df["algorithm"] == algorithm) & (df["heuristic"] == heuristic)]
    sub = sub.sort_values("n_dirty")
    ax.plot(sub["n_dirty"], sub["nodes_expanded"], marker="o", label=label)
ax.set_yscale("log")
ax.set_xlabel("Dirty cells")
ax.set_ylabel("Nodes expanded (log scale)")
ax.set_title("Nodes expanded vs dirty cells")
ax.legend()
fig.tight_layout()
fig.savefig("figures/nodes_vs_dirty.png", dpi=150)

# Plot 2: A* nodes expanded under h0, h1, h2, per grid.
astar = df[df["algorithm"] == "astar"]
pivot = astar.pivot(index="grid", columns="heuristic", values="nodes_expanded")
pivot = pivot[["h0", "h1", "h2"]]
ax = pivot.plot(kind="bar", figsize=(8, 4.5), logy=True)
ax.set_xlabel("Grid")
ax.set_ylabel("Nodes expanded (log scale)")
ax.set_title("A* nodes expanded by heuristic")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("figures/astar_heuristics.png", dpi=150)

# Plot 3: IDA* nodes expanded by heuristic. Timeouts show as gaps.
ida = df[df["algorithm"] == "idastar"]
pivot = ida.pivot(index="grid", columns="heuristic", values="nodes_expanded")
pivot = pivot[["h0", "h1", "h2"]]
ax = pivot.plot(kind="bar", figsize=(8, 4.5), logy=True)
ax.set_xlabel("Grid (missing bar = TIMEOUT)")
ax.set_ylabel("Nodes expanded (log scale)")
ax.set_title("IDA* nodes expanded by heuristic")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("figures/idastar_heuristics.png", dpi=150)

print("saved figures/ and results_table.csv")