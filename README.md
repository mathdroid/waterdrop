# waterdrop

An Intelligent Water Drops (IWD) metaheuristic for the **open shop scheduling
problem**, written in 2015 and revised in 2026.

The main script is `newiwd.py`. Everything else in the repo is earlier
experiments and per-instance copies kept for history (see "Repository layout").

## The problem: open shop scheduling

There are `J` jobs and `I` machines. Every job must be processed exactly once
on every machine, and `T[j, i]` is how long job `j` takes on machine `i`.
Unlike a flow shop or job shop, **the order in which a job visits the machines
is free**. The rules are:

- a machine works on at most one job at a time;
- a job is on at most one machine at a time;
- an operation, once started, runs to completion.

The goal is to minimise the **makespan**: the time at which the last operation
finishes.

A simple lower bound is the largest total workload of any single job or any
single machine. Neither can finish sooner than its own total work. The two
built-in instances (7x7 and 10x10, from the Taillard and Gueret-Prins
benchmark families) are built so that every job and every machine has exactly
1000 units of work. That makes them hard: many paths through the schedule are
critical at the same time.

## The algorithm: Intelligent Water Drops

IWD (Shah-Hosseini, 2007/2009) is a swarm metaheuristic inspired by rivers.
Water drops flowing downhill erode the ground they pass over, and paths that
many drops use become deeper and easier to follow. Over time, good routes
emerge. It is closely related to Ant Colony Optimisation, with "soil" playing
the role of (inverse) pheromone.

### How it maps onto scheduling

1. **Graph.** Every operation `(job, machine)` is a node. A water drop builds
   a solution by visiting every node exactly once. The order it visits them in
   is a priority list of operations.
2. **Soil.** Every directed edge `a -> b` carries an amount of soil. **Low soil
   means attractive.** "After scheduling `a`, scheduling `b` next has worked
   well before."
3. **Choosing the next operation.** From the current node, the drop picks the
   next unvisited operation at random, with weight
   `HUD(op)^beta / (epsilon + soil(edge))^alpha`.
   `HUD` is a heuristic that favours longer operations first (longest
   processing time first), which tends to pack schedules more tightly.
4. **Decoding to a schedule.** The priority list is turned into an actual
   timetable by taking operations in order and putting each into the
   **earliest time gap where both its job and its machine are free**. This
   always produces a valid schedule with no overlaps.
5. **Soil updates.**
   - *Local:* when a drop crosses an edge, it deposits a little soil there.
     This makes the other drops in the same iteration explore different
     routes instead of all copying the first one.
   - *Global:* after every iteration, all soil evaporates back towards its
     upper bound. Then soil is eroded along the edges of the iteration's best
     sequence and the all-time best sequence, making those routes more likely
     next time.
   - Soil is kept between a lower and an upper bound, so no edge ever becomes
     certain or impossible.
   - If the best result hasn't improved for `stagmax` iterations, all soil is
     reset to restart exploration (the best solution found is kept).
6. **Local search.** Each iteration, the best sequence is refined by moving
   operations that lie on the critical path (the chain of operations that
   determines the makespan) to just before or just after their critical
   neighbours, keeping moves that do not make the schedule worse.
7. The loop stops after `itermax` iterations, or earlier if the makespan
   reaches `lower_bound`.

## Running it

```
python3 newiwd.py
```

It needs only the Python 3 standard library. The instance and all parameters
are module-level variables near the top of the file:

| Variable | Meaning |
|---|---|
| `sampleT`, `J`, `I` | The instance (durations keyed `(job, machine)`) and its size. To switch instances, uncomment another `sampleT` line and set `J`/`I` in the initialisation section. |
| `lower_bound` | Stop early once this makespan is reached. |
| `N`, `itermax` | Water drops per iteration, and maximum iterations. |
| `initsoil`, `soilratio` | Soil upper bound, and the ratio between the upper and lower bound. |
| `alpha`, `beta` | How much soil, and how much the heuristic, influence each choice. |
| `rhon`, `rhoiwd`, `tbweight` | Local update rate, global update rate, and how the global reinforcement is split between the all-time best and the iteration best. |
| `stagmax` | Iterations without improvement before soil is reset. |
| `LS_BUDGET`, `TB_SHARE`, `sideways` | Local search effort per iteration (as a multiple of `N`; `0` turns it off), how much of it polishes the all-time best, and the chance of accepting an equal-makespan move. |

The script prints the best makespan (`MSTB`), the best operation order
(`TB`), the start and finish time of every operation, and timing statistics.
With the defaults (`N = 100`, `itermax = 500`) the 7x7 instance reaches a
makespan of about 1070 in roughly 25 seconds.

## 2026 revision

The original 2015 version had a bug in the gap bookkeeping (a loop meant to
shift gap records, `range(e[j], w+2)`, never ran). Because of it, the
scheduler sometimes placed two operations on the same job or machine at the
same time. Many reported makespans, including "best" results, were invalid
schedules, so the numbers in the old `hasil*.txt` files should not be trusted.

The revision fixes that and reworks the search:

- a new, simpler and faster decoder (earliest-gap insertion);
- one-way soil per edge, with a virtual start node so the first operation is
  also learned;
- bounded soil, so selection is no longer almost deterministic;
- the heuristic actually influences choices (before, it was numerically
  inert);
- reinforcement of the all-time best sequence, plus a reset when the search
  stagnates;
- critical-path local search.

The old version is still available in git history.

### Results

Each version ran with 20 drops x 30 iterations over 10 random seeds. "Valid"
counts how many of the reported best schedules actually have no overlaps.

| Instance | Version | Best | Mean | Worst | Valid | Sec/run |
|---|---|---|---|---|---|---|
| 7x7 | 2015 original | 1214 | 1265.4 | 1314 | 6/10 | 0.89 |
| 7x7 | bug fixes only | 1232 | 1256.2 | 1279 | 10/10 | 1.03 |
| 7x7 | 2026 revision | **1063** | **1099.1** | **1136** | 10/10 | **0.31** |
| 10x10 | 2015 original | 1416 | 1509.1 | 1588 | 1/10 | 3.84 |
| 10x10 | bug fixes only | 1432 | 1468.8 | 1503 | 10/10 | 4.19 |
| 10x10 | 2026 revision | **1185** | **1208.6** | **1231** | 10/10 | **1.08** |

The revision does about 3x as many schedule evaluations per iteration
because of the local search, but it still runs 3-4x faster thanks to the new
decoder. With local search turned off (`LS_BUDGET = 0`), it averages 1152.6
(7x7) and 1260.6 (10x10), still well ahead of the bug-fix-only version.

## Repository layout

| File | What it is |
|---|---|
| `newiwd.py` | The current algorithm (see above). |
| `odi.py`, `ALGORITMA IWD.py` | Earlier versions of the same algorithm. |
| `GP 04-1.py`, `GP 05-1.py`, `GP 10-10.py`, `TAILLARD 4-1.py`, `TAILLARD 4-10.py`, `J7 10-2.py`, `Contoh kasus sederhana.py` | Older per-instance copies of the algorithm (Gueret-Prins, Taillard and other benchmark instances; "contoh kasus sederhana" = "simple example case"). |
| `makespan doang.py` | The schedule decoder on its own ("doang" = "only"). |
| `hasil*.txt`, `HASIL KASUS SEDERHANA.txt`, `4x4.txt` | Output logs from old runs ("hasil" = "results"). Produced by the buggy 2015 code. |
| `coba*.py`, `COBA*.py`, `BUAT BIKIN WAKTU.py`, `halo.py`, `minsoil.py`, `profile.py`, `setup.py` | Scratch experiments ("coba" = "try"). |

Comments and variable names in the older scripts are mostly Indonesian: `mesin` = machine,
`jadwal` = schedule, `ujung` = end, `gap mesin` / `gap job` = idle gaps on a
machine / job.
