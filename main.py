import sys
import argparse
from src.planner import CourierPlanner
from src.algorithms.knapsack import print_dp_table

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Mini-Courier Planner - Scaled DAA Capstone Prototype",
        add_help=True
    )
    parser.add_argument("pos_capacity", nargs="?", type=int, default=None, help="Truck capacity in kg (positional)")
    parser.add_argument("-c", "--capacity", type=int, default=15, help="Truck capacity in kg (default: 15)")
    parser.add_argument("-d", "--dataset", type=str, default="sample", help="Dataset to load: 'sample', 'large', or path to JSON")
    parser.add_argument("-g", "--graph", type=str, default="data/city_graph.json", help="Path to road network graph JSON")
    parser.add_argument("-s", "--sort", type=str, choices=["deadline", "value", "ratio", "weight"], default="deadline", help="Prioritization key")
    parser.add_argument("--no-2opt", action="store_true", help="Disable 2-Opt route optimization (use plain Nearest Neighbor)")
    return parser.parse_args()

def main():
    args = parse_arguments()
    capacity = args.pos_capacity if args.pos_capacity is not None else args.capacity

    if args.dataset == "sample":
        parcels_file = "data/sample_parcels.json"
    elif args.dataset == "large":
        parcels_file = "data/large_dataset.json"
    else:
        parcels_file = args.dataset

    graph_file = args.graph

    print("=" * 72)
    print("         MINI-COURIER PLANNER - SCALED DAA CAPSTONE PROTOTYPE           ")
    print("=" * 72)

    planner = CourierPlanner(parcels_file, graph_file)
    print(f"[Phase 1] Loaded {len(planner.parcels)} parcels from '{parcels_file}'")
    print(f"[Phase 1] Road network: {len(planner.graph.get_nodes())} hubs, {planner.graph.edge_count()} road segments")
    print(f"[Phase 1] Truck Payload Limit: {capacity} kg | Sorting Strategy: '{args.sort}'\n")

    result = planner.plan(truck_capacity=capacity, sort_key=args.sort, use_2opt=not args.no_2opt)

    # 1. Prioritization
    print(f"[Phase 2] Prioritized Parcels (Ordered by '{args.sort}'):")
    print(f"  {'ID':<6}{'Deadline':<12}{'Weight':<10}{'Value':<8}{'Ratio':<8}{'Tier':<10}{'Destination'}")
    print("  " + "-" * 66)
    for p in result["sorted_parcels"][:12]:
        print(f"  {p.id:<6}{str(p.deadline) + 'm':<12}{str(p.weight) + 'kg':<10}{p.value:<8}{p.ratio:<8}{p.urgency_tier:<10}{p.destination}")
    if len(result["sorted_parcels"]) > 12:
        print(f"  ... and {len(result['sorted_parcels']) - 12} additional parcels")

    # 2. Knapsack Packing
    print(f"\n[Phase 2] Knapsack Optimal Box Packing (Capacity: {capacity} kg):")
    print(f"  Payload Packed       : {result['total_weight']} kg / {capacity} kg ({result['capacity_utilization']}%)")
    print(f"  Total Priority Value : {result['total_value']}")
    print(f"  Selected Packages    : {len(result['packed_parcels'])} loaded, {len(result['unpacked_parcels'])} postponed")
    print("  Manifest:")
    for p in result["packed_parcels"]:
        print(f"    * {p.id:<4} [Dest: {p.destination:<4}] W: {p.weight}kg, Val: {p.value}, Deadline: {p.deadline}m, Tier: {p.urgency_tier}")

    # 3. DP Table Evidence
    print("\n[Phase 2 Evidence] Dynamic Programming (0/1 Knapsack) State Matrix:")
    print_dp_table(result["dp_table"], result["sorted_parcels"], capacity)

    # 4. Dijkstra Shortest Paths
    print("\n[Phase 3] Road Network Submatrix - Dijkstra Shortest Paths (km):")
    targets = ["Depot"] + result["destinations"]
    header = f"  {'Node':<8}" + "".join(f"{t:>8}" for t in targets)
    print(header)
    for u in targets:
        row = f"  {u:<8}" + "".join(f"{result['dist_matrix'][u][v]:>8.1f}" for v in targets)
        print(row)

    # 5. Route Maker & 2-Opt comparison
    comp = result["tsp_comparison"]
    print("\n[Phase 3] Delivery Route Optimization (TSP):")
    print(f"  Nearest-Neighbor Tour : {' -> '.join(comp['nearest_neighbor']['tour'])} ({comp['nearest_neighbor']['distance']:.2f} km)")
    print(f"  2-Opt Refined Tour    : {' -> '.join(comp['two_opt']['tour'])} ({comp['two_opt']['distance']:.2f} km)")
    if comp["distance_saved"] > 0:
        print(f"  [Optimization Gain]   : 2-Opt saved {comp['distance_saved']:.2f} km ({comp['improvement_percent']}%) over pure greedy!")

    print(f"\n  Final Dispatched Tour : {' -> '.join(result['route'])}")
    print(f"  Total Tour Distance   : {result['total_distance']:.2f} km")

    # Detailed Road Itinerary
    print("\n[Phase 3] Step-by-Step Road Navigation Itinerary:")
    for idx, seg in enumerate(result["navigation_segments"], 1):
        via = " -> ".join(seg["road_nodes"])
        print(f"  Leg {idx}: {seg['from']} -> {seg['to']} ({seg['distance']:.1f} km via {via})")

    # Runtime metrics
    print("\n[Phase 4] Execution Performance Metrics:")
    for step, t in result["timing"].items():
        print(f"  - {step.replace('_', ' ').title():<22} : {t * 1000:.3f} ms")
    print("=" * 72)

if __name__ == "__main__":
    main()
