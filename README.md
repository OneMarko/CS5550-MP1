# CS 5550 Mini-Project 1: search algorithms for a cleaning robot

A grid-world vacuum robot. Given a map, a start cell, and a set of dirty cells, the code finds a sequence of actions that cleans every dirty cell. It implements DFS, A*, and IDA*, and three heuristics (h0, h1, h2).

## Requirements

- Python 3.10 or newer
- matplotlib and pandas (plots and tables only; the search code uses the standard library)

```
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
pip install matplotlib pandas
```

## Files

| File | Purpose |
|------|---------|
| `vacuum_world.py` | `VacuumWorld` environment (Part 1) |
| `search.py` | `dfs_search`, `astar_search`, `idastar_search` (Part 2) |
| `heuristics.py` | `manhattan`, `h0`, `h1`, `h2`; `h3` is not implemented |
| `priority_queue.py` | Provided priority queue with decrease-key |
| `test_grids.py` | Provided test grids |
| `run_tests.py` | Provided smoke tests |
| `experiments.py` | Experiment harness (writes `results.csv`) |
| `plots.py` | Builds `results_table.csv` and the plots in `figures/` |
| `results.csv` | Raw measurements from the full run |
| `figures/` | Plots (`.png`) |
| `report.pdf` | Written report |
| `AI_USE.md` | AI tool disclosure |

## How to run

Run all commands from this folder.

Smoke tests (16 pass, 1 skips because h3 is not implemented):

```
python run_tests.py
```

Quick check of A* on the example grid (optimal cost 14):

```
python search.py
```

Experiments:

```
python experiments.py --quick       # three small grids
python experiments.py               # all six grids, 60 s timeout per run
python experiments.py --timeout 120
python experiments.py --grids g6_corridor
```

Plots and table, after `results.csv` exists:

```
python plots.py
```

## Notes

- Nodes expanded means nodes removed from the frontier whose successors were generated. A node that is popped and found to be the goal is not counted.
- A run that exceeds the timeout is recorded as `TIMEOUT` in `results.csv`.
- Three runs time out: IDA* with h0 on `g5_rooms`, and IDA* with h0 and h1 on `g6_corridor`.
- Runtimes depend on the machine. Compare node counts between algorithms.
