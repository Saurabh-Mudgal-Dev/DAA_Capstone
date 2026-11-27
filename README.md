# Mini-Courier Planner: Scaled Intelligent Delivery & Packing Optimization
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**Institution:** K.R. Mangalam University, Gurugram, Haryana  
**Faculty In-Charge:** Dr. Shweta Agarwal  
**Student Name:** Saurabh  
**Roll No.:** 2501010045  
**Submission Mode:** GitHub / Zosima  

---

## 1. Project Overview & Problem Statement

The **Mini-Courier Planner** is a scalable, end-to-end algorithmic system simulating intelligent logistics dispatch. Designed as a capstone project for the *Design & Analysis of Algorithms* curriculum, the application integrates five algorithmic paradigms to solve practical courier challenges:
1. **Divide-and-Conquer Sorting:** Prioritizes delivery parcels by deadline urgency, revenue value, or density ratio in $\Theta(N \log N)$ time.
2. **Dynamic Programming (0/1 Knapsack):** Optimizes vehicle payload utilization under discrete weight capacities ($W$) using a recurrence state matrix and backtracing ($\Theta(N \cdot W)$).
3. **Graph Processing (Dijkstra's Algorithm):** Computes single-source and all-pairs shortest paths across a city road network with a min-heap priority queue ($O((V + E) \log V)$).
4. **Approximation & Local Search (TSP & 2-Opt):** Generates closed delivery routes starting and ending at the central depot using the Nearest-Neighbor heuristic ($O(K^2)$) and refines the tour with **2-Opt Local Search** edge swaps.
5. **Empirical Benchmarking & Scalability Analysis:** Measures wall-clock performance scaling across input sizes up to $N = 10,000$ parcels and $V = 400$ vertices, verified against theoretical asymptotic bounds.

---

## 2. University Rubric & Phase Compliance Matrix (100 Marks)

| Phase | Marks | Prescribed Task | Implementation & Deliverables | Status |
|---|:---:|---|---|:---:|
| **Phase 1: Problem Design & Planning** | 20 | Define parcel attributes, graph format, pipeline integration, data schemas. | `src/models.py`, `data/sample_parcels.json`, `data/city_graph.json`, `data/generate_datasets.py` | Completed |
| **Phase 2: Prioritization & Box Packing** | 20 | Sort parcels by deadline/priority; apply 0/1 Knapsack DP with state table evidence. | `src/algorithms/sorting.py`, `src/algorithms/knapsack.py`, DP table printout, $O(W)$ space-optimized DP | Completed |
| **Phase 3: Route Maker & Graph Processing** | 20 | City road graph, Dijkstra shortest paths, Nearest-Neighbor TSP + 2-Opt refinement. | `src/algorithms/dijkstra.py`, `src/algorithms/tsp.py`, distance submatrix, turn-by-turn navigation | Completed |
| **Phase 4: Performance Testing & Optimization** | 20 | Benchmark with multiple input sizes, plot runtime charts, optimization analysis. | `benchmarks/benchmark_runner.py`, `runtime_analysis.png` (4 panels), `data/large_dataset.json` | Completed |
| **Phase 5: Final Report & Demonstration** | 20 | Integrated CLI, output traces, documentation quality, viva defense answers. | `main.py`, `src/planner.py`, `README.md` | Completed |

---

## 3. Scaled System Architecture & Workflow

```
[Parcels Dataset (JSON)]         [City Road Graph (JSON)]
           │                                 │
           └───────────────┬─────────────────┘
                           │ (Phase 1)
           ▼ [Data Modeling: Parcel & RoadGraph]
             • Properties: ratio (value/weight), urgency_tier
             • Edge validation (non-negative weights)
                           │
                           │ (Phase 2)
           ▼ [Prioritization via Divide-and-Conquer]
             • Merge Sort (Guaranteed O(N log N))
             • 3-Way Median-of-Three Quick Sort
                           │
                           │ (Phase 2)
           ▼ [0/1 Knapsack Dynamic Programming]
             • Full (N+1) x (W+1) DP Table Matrix
             • Backtracking to identify loaded parcels
             • Space-Optimized O(W) Rolling Array
                           │
                           │ (Phase 3)
           ▼ [Dijkstra's Algorithm (Min-Heap)]
             • All-pairs distance submatrix for loaded destinations
             • Turn-by-turn physical street junction reconstruction
                           │
                           │ (Phase 3)
           ▼ [Route Construction & Local Search (TSP)]
             • Nearest-Neighbor Greedy Tour (O(K^2))
             • 2-Opt Local Search (Uncrossing edge swaps)
                           │
                           │ (Phase 4 & 5)
           ▼ [Execution Output & Scaled Benchmarking]
             • CLI Manifest & Step-by-Step Navigation
             • 4-Panel Performance Scaling Plots
```

---

## 4. Project Directory Structure

```text
DAA_Capstone/
├── data/
│   ├── sample_parcels.json            # 6 sample parcels for default quick demonstration
│   ├── city_graph.json               # Scaled city road network (15 hubs, 30 bidirectional edges)
│   ├── large_dataset.json            # Scaled dataset of 50 parcels across 14 delivery hubs
│   └── generate_datasets.py          # Synthetic dataset generator for testing arbitrary input scales
├── src/
│   ├── __init__.py
│   ├── models.py                     # Parcel & RoadGraph dataclasses with ratio, tier, and graph helpers
│   ├── planner.py                    # Modular pipeline orchestrator with turn-by-turn navigation
│   └── algorithms/
│       ├── __init__.py
│       ├── sorting.py                # Stable Merge Sort & 3-way partition Quick Sort
│       ├── knapsack.py               # 0/1 Knapsack DP, space-optimized DP, and windowed table formatter
│       ├── dijkstra.py               # Min-heap Dijkstra shortest paths & path reconstruction matrix
│       └── tsp.py                    # Nearest-Neighbor TSP + 2-Opt local search refinement
├── benchmarks/
│   ├── __init__.py
│   ├── benchmark_runner.py           # Empirical performance profiler (N up to 10,000)
│   └── plots/
│       └── runtime_analysis.png      # High-resolution 4-panel runtime scaling visualization
├── main.py                           # Flexible CLI driver supporting default, scaled, and custom inputs
├── requirements.txt                  # Python dependencies (matplotlib)
├── IMPLEMENTATION_GUIDE.md           # Commit guide and development blueprint
└── README.md                         # Complete project documentation and viva defense
```

---

## 5. Algorithmic Implementation & Scaled Enhancements

### 5.1. Parcel Prioritization (Merge Sort & 3-Way Quick Sort)
- **File:** `src/algorithms/sorting.py`
- **Merge Sort:** Divide-and-conquer strategy recursively splitting parcels and merging with an in-order short-circuit optimization (`left[-1] <= right[0]`). Guarantees worst-case $\Theta(N \log N)$ and preserves stability.
- **3-Way Partition Quick Sort:** Employs median-of-three pivot selection to prevent $O(N^2)$ degradation on sorted inputs and Dutch National Flag 3-way partitioning (`< pivot`, `== pivot`, `> pivot`). This handles large batches of parcels with identical deadlines in linear $O(N)$ time.

### 5.2. Vehicle Box Packing (0/1 Knapsack Dynamic Programming)
- **File:** `src/algorithms/knapsack.py`
- Courier trucks operate under fixed payload constraints $W$. Parcels are indivisible (0/1).
- **Recurrence Relation:**
  $$\text{dp}[i][w] = \begin{cases} \text{dp}[i-1][w] & \text{if } w_i > w \\ \max(\text{dp}[i-1][w],\; \text{dp}[i-1][w - w_i] + v_i) & \text{if } w_i \le w \end{cases}$$
- **Enhancement:** Includes both 2D table reconstruction ($O(N \cdot W)$) for viva evidence and an $O(W)$ space-optimized 1D rolling array (`knapsack_01_space_optimized`).
- **Greedy Comparison Helper:** Includes `fractional_knapsack_greedy` to directly prove in viva why Greedy fails on 0/1 indivisible parcels.

### 5.3. Road Network Shortest Paths (Dijkstra's Algorithm)
- **File:** `src/algorithms/dijkstra.py`
- Non-negative edge weights ($w(u, v) \ge 0$) evaluated using a binary min-heap priority queue (`heapq`).
- Predecessors are tracked to reconstruct exact street junctions traversed between consecutive delivery stops, feeding turn-by-turn navigation into `main.py`.

### 5.4. Route Maker & 2-Opt Optimization (TSP Heuristic)
- **File:** `src/algorithms/tsp.py`
- **Nearest-Neighbor:** Greedily picks the closest unvisited customer from the current location in $O(K^2)$ time.
- **2-Opt Local Search:** Post-processes the tour by iteratively testing pairs of non-adjacent edges $(a, b)$ and $(c, d)$. If replacing them with $(a, c)$ and $(b, d)$ decreases total driving distance, the sub-route `tour[i:j+1]` is reversed. This un-crosses overlapping routes and delivers 5%–25% distance savings.

---

## 6. How to Install and Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Main Planner
```bash
# 1. Default Demonstration (15 kg capacity on sample parcels)
python main.py

# 2. Positional capacity argument (e.g., 20 kg)
python main.py 20

# 3. Scaled Dataset (50 parcels across 15 city hubs, 40 kg capacity)
python main.py -d large -c 40

# 4. Custom sorting strategy (by value-to-weight ratio instead of deadline)
python main.py -d large -c 40 --sort ratio
```

### Step 3: Generate Dynamic Datasets (Unseen Viva Testing)
```bash
# Generate 100 random parcels across 20 nodes
python data/generate_datasets.py --parcels 100 --nodes 20

# Run planner on the generated dataset
python main.py -d data/generated_parcels.json -g data/generated_graph.json -c 50
```

### Step 4: Run the Scaled Benchmark Suite
```bash
python -m benchmarks.benchmark_runner
```
*Generates empirical scaling tables and saves the 4-panel chart to `benchmarks/plots/runtime_analysis.png`.*

---

## 7. Execution Output Traces

### 7.1. Baseline Demonstration (`python main.py`)
```text
========================================================================
         MINI-COURIER PLANNER - SCALED DAA CAPSTONE PROTOTYPE           
========================================================================
[Phase 1] Loaded 6 parcels from 'data/sample_parcels.json'
[Phase 1] Road network: 15 hubs, 30 road segments
[Phase 1] Truck Payload Limit: 15 kg | Sorting Strategy: 'deadline'

[Phase 2] Prioritized Parcels (Ordered by 'deadline'):
  ID    Deadline    Weight    Value   Ratio   Tier      Destination
  ------------------------------------------------------------------
  P5    20m         4kg       9       2.25    Urgent    C1
  P2    30m         8kg       15      1.88    Urgent    C2
  P3    45m         3kg       7       2.33    High      C3
  P1    60m         5kg       10      2.0     High      C1
  P6    75m         7kg       14      2.0     Standard  C5
  P4    90m         6kg       12      2.0     Standard  C4

[Phase 2] Knapsack Optimal Box Packing (Capacity: 15 kg):
  Payload Packed       : 15 kg / 15 kg (100.0%)
  Total Priority Value : 31
  Selected Packages    : 3 loaded, 3 postponed
  Manifest:
    * P5   [Dest: C1  ] W: 4kg, Val: 9, Deadline: 20m, Tier: Urgent
    * P2   [Dest: C2  ] W: 8kg, Val: 15, Deadline: 30m, Tier: Urgent
    * P3   [Dest: C3  ] W: 3kg, Val: 7, Deadline: 45m, Tier: High

[Phase 2 Evidence] Dynamic Programming (0/1 Knapsack) State Matrix:
Item / W       0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
----------------------------------------------------------------------------
0 (init)       0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
P5 (w=4)       0   0   0   0   9   9   9   9   9   9   9   9   9   9   9   9
P2 (w=8)       0   0   0   0   9   9   9   9  15  15  15  15  24  24  24  24
P3 (w=3)       0   0   0   7   9   9   9  16  16  16  16  22  24  24  24  31
P1 (w=5)       0   0   0   7   9  10  10  16  17  19  19  22  26  26  26  31
P6 (w=7)       0   0   0   7   9  10  10  16  17  19  21  23  26  26  30  31
P4 (w=6)       0   0   0   7   9  10  12  16  17  19  21  23  26  28  30  31

[Phase 3] Road Network Submatrix - Dijkstra Shortest Paths (km):
  Node       Depot      C1      C2      C3
  Depot        0.0     3.5     2.0     8.5
  C1           3.5     0.0     1.5     5.0
  C2           2.0     1.5     0.0     6.5
  C3           8.5     5.0     6.5     0.0

[Phase 3] Delivery Route Optimization (TSP):
  Nearest-Neighbor Tour : Depot -> C2 -> C1 -> C3 -> Depot (17.00 km)
  2-Opt Refined Tour    : Depot -> C2 -> C1 -> C3 -> Depot (17.00 km)

  Final Dispatched Tour : Depot -> C2 -> C1 -> C3 -> Depot
  Total Tour Distance   : 17.00 km

[Phase 3] Step-by-Step Road Navigation Itinerary:
  Leg 1: Depot -> C2 (2.0 km via Depot -> C2)
  Leg 2: C2 -> C1 (1.5 km via C2 -> C1)
  Leg 3: C1 -> C3 (5.0 km via C1 -> C3)
  Leg 4: C3 -> Depot (8.5 km via C3 -> C1 -> C2 -> Depot)

[Phase 4] Execution Performance Metrics:
  - Sorting Time           : 0.016 ms
  - Knapsack Time          : 0.023 ms
  - Dijkstra Time          : 0.181 ms
  - Tsp Time               : 0.491 ms
========================================================================
```

### 7.2. Scaled Dataset Demonstration (`python main.py -d large -c 40`)
- Loaded **50 parcels** across 15 road hubs.
- Packed **40 kg / 40 kg (100.0% utilization)** achieving **Priority Value = 120**.
- **TSP 2-Opt Optimization:**
  - Nearest Neighbor Tour: `Depot -> C2 -> C1 -> C8 -> C7 -> C6 -> C3 -> C4 -> C5 -> C11 -> Depot` (**48.50 km**)
  - 2-Opt Refined Tour: `Depot -> C6 -> C7 -> C8 -> C11 -> C5 -> C4 -> C3 -> C1 -> C2 -> Depot` (**37.40 km**)
  - **Result:** 2-Opt uncrossed overlapping legs, saving **11.10 km (22.89%)** of driving distance.

---

## 8. Theoretical vs. Empirical Complexity Analysis

| Algorithm | Paradigm | Best Case | Average Case | Worst Case | Space Complexity | Scaled Empirical Result ($N=10,000$) |
|---|---|:---:|:---:|:---:|:---:|---|
| **Merge Sort** | Divide & Conquer | $\Theta(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(N)$ | $0.0338\text{ s}$ at $N=10,000$. Stable and predictable. |
| **Quick Sort** | Divide & Conquer | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N^2)$ | $O(\log N)$ | $0.0157\text{ s}$ at $N=10,000$. 2.1x faster than Merge Sort due to cache locality and 3-way partition. |
| **0/1 Knapsack** | Dynamic Programming | $\Theta(N \cdot W)$ | $\Theta(N \cdot W)$ | $\Theta(N \cdot W)$ | $O(N \cdot W)$ | $0.0110\text{ s}$ at $N=500, W=150$. Strictly linear in $N$ for fixed capacity. |
| **Dijkstra** | Greedy / Graph | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O(V + E)$ | $0.0009\text{ s}$ at $V=400$ vertices using binary min-heap. |
| **Nearest Neighbor** | Approximation | $O(K^2)$ | $O(K^2)$ | $O(K^2)$ | $O(K)$ | $0.0002\text{ s}$ at $K=30$ stops. |
| **2-Opt Search** | Local Search | $O(K^2)$ | $O(K^2)$ | $O(K^3)$ | $O(K)$ | $0.0007\text{ s}$ at $K=30$ stops, reducing route distance by up to $22.9\%$. |

---

## 9. Future Optimization Suggestions (Phase 4 Rubric)

1. **Space-Optimized Knapsack:** Reduces auxiliary memory from $O(N \cdot W)$ to $O(W)$ using 1D rolling array backward traversal.
2. **2-Opt Edge Exchanges:** Successfully implemented in Phase 3/4, removing path crossings and saving up to 22.9% tour distance.
3. **Multi-Vehicle Fleet Dispatch (VRP):** Clustering delivery destinations using K-Means or Clarke-Wright Savings algorithm to partition parcels across multiple delivery vans.
4. **Contraction Hierarchies for Dijkstra:** Precomputing shortcut edges across regional arterial roads to achieve sub-microsecond shortest-path queries on continental road networks.

---

## 10. Viva / Demonstration Defense Guide

### Q1: Why can't we use a Greedy algorithm for parcel box packing?
> **Answer:** Greedy by value-to-weight ratio only works for the **Fractional Knapsack** problem. For discrete 0/1 parcels, taking an item with a high ratio can leave an awkward residual capacity that prevents packing two slightly lower-ratio items whose combined value is greater. Dynamic Programming evaluates all sub-capacities, guaranteeing mathematical optimality.

### Q2: Why choose Dijkstra over Bellman-Ford or Floyd-Warshall?
> **Answer:** Physical road distances between street intersections are strictly positive ($w > 0$). Dijkstra runs in $O((V + E) \log V)$ with a min-heap, whereas Bellman-Ford takes $O(V \cdot E)$ (necessary only if negative weight edges exist) and Floyd-Warshall takes $O(V^3)$ (intractable for large city road graphs).

### Q3: What is the 2-Opt algorithm and how does it improve upon Nearest Neighbor?
> **Answer:** Nearest-Neighbor is a greedy heuristic that can get trapped in suboptimal loops, frequently producing crisscrossing paths. 2-Opt is a local search algorithm that iteratively cuts two non-adjacent edges $(u_1, v_1)$ and $(u_2, v_2)$ and reconnects them as $(u_1, u_2)$ and $(v_1, v_2)$ by reversing the intermediate path. If the new distance is shorter, the swap is kept. In our scaled testing, 2-Opt saved 22.89% travel distance over greedy Nearest Neighbor.

### Q4: How does the system handle an unseen dataset during evaluation?
> **Answer:** The system is completely dynamic. By running `python main.py -d <path_to_parcels.json> -g <path_to_graph.json>`, or generating test files with `python data/generate_datasets.py --parcels 100 --nodes 20`, all algorithms parse, sort, pack, route, and report automatically.
