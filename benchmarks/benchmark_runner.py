import os
import time
import random
import matplotlib.pyplot as plt
from src.models import Parcel, RoadGraph
from src.algorithms.sorting import merge_sort_parcels, quick_sort_parcels
from src.algorithms.knapsack import knapsack_01
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.tsp import nearest_neighbor_tsp, two_opt_tsp

def benchmark_sorting():
    sizes = [100, 500, 1000, 2500, 5000, 10000]
    merge_times = []
    quick_times = []

    print("\n--- Benchmarking Sorting (Merge Sort vs Quick Sort) ---")
    print(f"{'Size (N)':<12}{'Merge Sort (s)':<18}{'Quick Sort (s)':<18}")
    for s in sizes:
        parcels = [
            Parcel(f"P{i}", random.randint(1, 20), random.randint(1, 50), random.randint(10, 500), f"C{i % 14}")
            for i in range(s)
        ]

        t0 = time.perf_counter()
        merge_sort_parcels(parcels, key="deadline")
        t_merge = time.perf_counter() - t0
        merge_times.append(t_merge)

        t0 = time.perf_counter()
        quick_sort_parcels(parcels, key="deadline")
        t_quick = time.perf_counter() - t0
        quick_times.append(t_quick)

        print(f"{s:<12}{t_merge:<18.6f}{t_quick:<18.6f}")

    return sizes, merge_times, quick_times

def benchmark_knapsack():
    sizes = [20, 50, 100, 200, 350, 500]
    knapsack_times = []
    capacity = 150

    print("\n--- Benchmarking 0/1 Knapsack DP (Capacity W=150) ---")
    print(f"{'Parcels (N)':<15}{'Runtime (s)':<18}")
    for s in sizes:
        parcels = [
            Parcel(f"P{i}", random.randint(1, 15), random.randint(1, 30), 60, "C1")
            for i in range(s)
        ]

        t0 = time.perf_counter()
        knapsack_01(parcels, capacity)
        t_knap = time.perf_counter() - t0
        knapsack_times.append(t_knap)
        print(f"{s:<15}{t_knap:<18.6f}")

    return sizes, knapsack_times

def benchmark_dijkstra():
    sizes = [20, 50, 100, 200, 400]
    dijkstra_times = []

    print("\n--- Benchmarking Dijkstra Shortest Path ---")
    print(f"{'Vertices (V)':<15}{'Runtime (s)':<18}")
    for s in sizes:
        g = RoadGraph()
        nodes = [f"N{i}" for i in range(s)]
        for i in range(s):
            for _ in range(5):
                target = random.choice(nodes)
                if target != nodes[i]:
                    g.add_edge(nodes[i], target, random.uniform(1.0, 15.0))

        t0 = time.perf_counter()
        dijkstra_shortest_path(g, nodes[0])
        t_dijkstra = time.perf_counter() - t0
        dijkstra_times.append(t_dijkstra)
        print(f"{s:<15}{t_dijkstra:<18.6f}")

    return sizes, dijkstra_times

def benchmark_tsp():
    stops = [5, 10, 15, 20, 25, 30]
    nn_times = []
    two_opt_times = []
    dist_improvements = []

    print("\n--- Benchmarking Route Optimization (Nearest Neighbor vs 2-Opt) ---")
    print(f"{'Stops (K)':<12}{'NN Time (s)':<16}{'2-Opt Time (s)':<16}{'Dist Saved (%)':<16}")

    for k in stops:
        nodes = ["Depot"] + [f"C{i}" for i in range(1, k)]
        dist_matrix = {u: {} for u in nodes}
        for i, u in enumerate(nodes):
            dist_matrix[u][u] = 0.0
            for j in range(i + 1, len(nodes)):
                v = nodes[j]
                d = round(random.uniform(2.0, 30.0), 1)
                dist_matrix[u][v] = d
                dist_matrix[v][u] = d

        t0 = time.perf_counter()
        _, nn_dist = nearest_neighbor_tsp(dist_matrix, "Depot")
        t_nn = time.perf_counter() - t0
        nn_times.append(t_nn)

        t0 = time.perf_counter()
        _, opt_dist = two_opt_tsp(dist_matrix, "Depot")
        t_opt = time.perf_counter() - t0
        two_opt_times.append(t_opt)

        pct = round(((nn_dist - opt_dist) / nn_dist) * 100, 1) if nn_dist > 0 else 0.0
        dist_improvements.append(pct)
        print(f"{k:<12}{t_nn:<16.6f}{t_opt:<16.6f}{pct:<16.1f}")

    return stops, nn_times, two_opt_times, dist_improvements

def generate_plots():
    os.makedirs("benchmarks/plots", exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))

    # 1. Sorting
    s_sizes, m_times, q_times = benchmark_sorting()
    axes[0, 0].plot(s_sizes, m_times, marker="o", color="#1f77b4", linewidth=2, label="Merge Sort (O(N log N))")
    axes[0, 0].plot(s_sizes, q_times, marker="s", color="#d62728", linewidth=2, label="Quick Sort (O(N log N))")
    axes[0, 0].set_title("1. Sorting Runtime Scaling", fontsize=13, fontweight="bold")
    axes[0, 0].set_xlabel("Number of Parcels (N)", fontsize=11)
    axes[0, 0].set_ylabel("Execution Time (seconds)", fontsize=11)
    axes[0, 0].grid(True, linestyle="--", alpha=0.6)
    axes[0, 0].legend()

    # 2. Knapsack DP
    k_sizes, k_times = benchmark_knapsack()
    axes[0, 1].plot(k_sizes, k_times, marker="^", color="#ff7f0e", linewidth=2, label="0/1 Knapsack (O(N * W))")
    axes[0, 1].set_title("2. Knapsack DP Scaling (W=150)", fontsize=13, fontweight="bold")
    axes[0, 1].set_xlabel("Number of Parcels (N)", fontsize=11)
    axes[0, 1].set_ylabel("Execution Time (seconds)", fontsize=11)
    axes[0, 1].grid(True, linestyle="--", alpha=0.6)
    axes[0, 1].legend()

    # 3. Dijkstra
    d_sizes, d_times = benchmark_dijkstra()
    axes[1, 0].plot(d_sizes, d_times, marker="d", color="#2ca02c", linewidth=2, label="Dijkstra (O((V+E) log V))")
    axes[1, 0].set_title("3. Dijkstra Shortest Path Scaling", fontsize=13, fontweight="bold")
    axes[1, 0].set_xlabel("Number of Vertices (V)", fontsize=11)
    axes[1, 0].set_ylabel("Execution Time (seconds)", fontsize=11)
    axes[1, 0].grid(True, linestyle="--", alpha=0.6)
    axes[1, 0].legend()

    # 4. TSP Optimization
    k_stops, nn_times, opt_times, saved = benchmark_tsp()
    axes[1, 1].plot(k_stops, nn_times, marker="o", color="#9467bd", linewidth=2, label="Nearest Neighbor (O(K^2))")
    axes[1, 1].plot(k_stops, opt_times, marker="x", color="#8c564b", linewidth=2, label="2-Opt Refinement")
    axes[1, 1].set_title("4. Route Planning Optimization (TSP)", fontsize=13, fontweight="bold")
    axes[1, 1].set_xlabel("Delivery Stops (K)", fontsize=11)
    axes[1, 1].set_ylabel("Execution Time (seconds)", fontsize=11)
    axes[1, 1].grid(True, linestyle="--", alpha=0.6)
    axes[1, 1].legend()

    plt.tight_layout()
    output_path = "benchmarks/plots/runtime_analysis.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[SUCCESS] Scaled runtime analysis plot saved to '{output_path}'")

if __name__ == "__main__":
    generate_plots()
