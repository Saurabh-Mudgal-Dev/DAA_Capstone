import json
import random
import argparse
from typing import List, Dict, Any

def generate_parcels(count: int, destinations: List[str], seed: int = 42) -> List[Dict[str, Any]]:
    random.seed(seed)
    parcels = []
    for i in range(1, count + 1):
        parcels.append({
            "id": f"P{i:03d}" if count >= 100 else f"P{i:02d}",
            "weight": random.randint(1, 10),
            "value": random.randint(5, 30),
            "deadline": random.choice([15, 20, 30, 45, 60, 75, 90, 120]),
            "destination": random.choice(destinations)
        })
    return parcels

def generate_city_graph(num_nodes: int, edge_density: float = 0.35, seed: int = 42) -> Dict[str, Any]:
    random.seed(seed)
    nodes = ["Depot"] + [f"C{i}" for i in range(1, num_nodes)]
    edges = []
    existing = set()

    # Backbone spanning tree to ensure connectivity
    for i in range(1, len(nodes)):
        parent = random.randint(0, i - 1)
        u, v = nodes[parent], nodes[i]
        w = round(random.uniform(1.5, 6.0), 1)
        edges.append([u, v, w])
        existing.add((u, v))
        existing.add((v, u))

    # Additional cross edges
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if (nodes[i], nodes[j]) not in existing and random.random() < edge_density:
                w = round(random.uniform(2.0, 9.0), 1)
                edges.append([nodes[i], nodes[j], w])
                existing.add((nodes[i], nodes[j]))
                existing.add((nodes[j], nodes[i]))

    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic dataset generator for Mini-Courier Planner")
    parser.add_argument("--parcels", type=int, default=50, help="Number of parcels to generate")
    parser.add_argument("--nodes", type=int, default=15, help="Number of graph nodes (including Depot)")
    parser.add_argument("--out-parcels", type=str, default="data/generated_parcels.json")
    parser.add_argument("--out-graph", type=str, default="data/generated_graph.json")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    graph = generate_city_graph(args.nodes, seed=args.seed)
    destinations = [n for n in graph["nodes"] if n != "Depot"]
    parcels = generate_parcels(args.parcels, destinations, seed=args.seed)

    with open(args.out_graph, "w") as f:
        json.dump(graph, f, indent=2)
    with open(args.out_parcels, "w") as f:
        json.dump(parcels, f, indent=2)

    print(f"Generated {len(parcels)} parcels -> {args.out_parcels}")
    print(f"Generated graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges -> {args.out_graph}")
