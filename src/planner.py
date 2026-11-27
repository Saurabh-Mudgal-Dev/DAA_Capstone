import time
import json
from typing import Dict, Any, List
from .models import Parcel, RoadGraph
from .algorithms.sorting import merge_sort_parcels, quick_sort_parcels
from .algorithms.knapsack import knapsack_01
from .algorithms.dijkstra import build_distance_matrix, build_path_matrix
from .algorithms.tsp import nearest_neighbor_tsp, two_opt_tsp, compare_tsp_algorithms

class CourierPlanner:
    def __init__(self, parcels_path: str, graph_path: str):
        self.parcels = self._load_parcels(parcels_path)
        self.graph = self._load_graph(graph_path)

    def _load_parcels(self, path: str) -> List[Parcel]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Parcel.from_dict(p) for p in data]

    def _load_graph(self, path: str) -> RoadGraph:
        with open(path, "r") as f:
            data = json.load(f)
        graph = RoadGraph()
        for u, v, w in data["edges"]:
            graph.add_edge(u, v, float(w))
        return graph

    def plan(self, truck_capacity: int = 15, sort_key: str = "deadline", use_2opt: bool = True) -> Dict[str, Any]:
        timing = {}

        # Phase 2: Prioritization
        t0 = time.perf_counter()
        sorted_parcels = merge_sort_parcels(self.parcels, key=sort_key)
        timing["sorting_time"] = time.perf_counter() - t0

        # Phase 2: 0/1 Knapsack Packing
        t0 = time.perf_counter()
        max_value, packed_parcels, dp_table = knapsack_01(sorted_parcels, truck_capacity)
        timing["knapsack_time"] = time.perf_counter() - t0

        packed_ids = {p.id for p in packed_parcels}
        unpacked_parcels = [p for p in sorted_parcels if p.id not in packed_ids]
        total_weight = sum(p.weight for p in packed_parcels)
        utilization = round((total_weight / truck_capacity) * 100, 1) if truck_capacity > 0 else 0.0

        # Phase 3: Road Network Dijkstra Shortest Paths
        t0 = time.perf_counter()
        destinations = sorted(list(set(p.destination for p in packed_parcels)))
        targets = ["Depot"] + destinations
        dist_matrix = build_distance_matrix(self.graph, targets)
        path_matrix = build_path_matrix(self.graph, targets)
        timing["dijkstra_time"] = time.perf_counter() - t0

        # Phase 3: TSP Route Optimization
        t0 = time.perf_counter()
        tsp_comparison = compare_tsp_algorithms(dist_matrix, start_node="Depot")
        if use_2opt:
            route = tsp_comparison["two_opt"]["tour"]
            total_distance = tsp_comparison["two_opt"]["distance"]
        else:
            route = tsp_comparison["nearest_neighbor"]["tour"]
            total_distance = tsp_comparison["nearest_neighbor"]["distance"]
        timing["tsp_time"] = time.perf_counter() - t0

        # Turn-by-turn street navigation segments
        navigation_segments = []
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            seg_path = path_matrix.get(u, {}).get(v, [u, v])
            seg_dist = dist_matrix.get(u, {}).get(v, 0.0)
            navigation_segments.append({
                "from": u,
                "to": v,
                "distance": seg_dist,
                "road_nodes": seg_path
            })

        return {
            "all_parcels": self.parcels,
            "sorted_parcels": sorted_parcels,
            "packed_parcels": packed_parcels,
            "unpacked_parcels": unpacked_parcels,
            "dp_table": dp_table,
            "total_value": max_value,
            "total_weight": total_weight,
            "capacity_utilization": utilization,
            "destinations": destinations,
            "dist_matrix": dist_matrix,
            "path_matrix": path_matrix,
            "route": route,
            "total_distance": total_distance,
            "navigation_segments": navigation_segments,
            "tsp_comparison": tsp_comparison,
            "timing": timing
        }
