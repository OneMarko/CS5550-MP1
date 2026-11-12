# AI use disclosure

Tool: Claude (Anthropic), used through the claude.ai chat interface.

## What I used it for

| Area | What Claude did | Roughly how much |
|------|-----------------|------------------|
| Project explanation | Explained what the assignment asks, what a search problem is, and what each part is for. Used Claude AI to brain storm majorly by  breaking down the project tasks| Moderate |
| Part 1 (`vacuum_world.py`) | Described in words what each method should do. I wrote the code myself | Moderate |
| Part 3 (`heuristics.py`) | Reviewed the code I wrote and pointed out the leftover `raise NotImplementedError` lines. I wrote the functions. Also helped debug the code when I couldn't figure out the errors in my code | Moderate  |
| Part 2 (`search.py`) | Reviewed my DFS, A*, and IDA*. Found the misplaced `return None` in A*, the wrong method name in IDA*, and the missing path tracking in IDA*. Gave short code snippets showing the fixes for the IDA* path tracking and for the expanded-node counter in A*. I applied them | Small |
| Part 4 (`plots.py`) | Wrote the plotting and table script that reads `results.csv` | One file |
| Report | Edited grammar and wording of text I wrote, and flagged statements to check | One pass |
| Documentation | Provided a guide and helped draft the README.md file|

## What I wrote myself

- The `VacuumWorld` implementation.
- `manhattan`, `h0`, `h1`, `h2`.
- The DFS and A* implementations, and the IDA* implementation apart from the snippets listed above.
- The admissibility arguments, the discussion answers, and the reflection in the report.
- Wrote the README.md and AI_USE.md documentations.


## What I checked

I read and ran everything Claude wrote and can explain it. `plots.py`.

## Not used for

Generating the heuristics, the admissibility arguments, the experimental analysis, or the reflection.
