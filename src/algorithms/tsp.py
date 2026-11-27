from typing import Dict, List, Tuple, Any

def calculate_tour_distance(tour: List[str], dist_matrix: Dict[str, Dict[str, float]]) -> float:
    cost = 0.0
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        c = dist_matrix.get(u, {}).get(v, float('inf'))
        if c == float('inf'):
            return float('inf')
        cost += c
    return round(cost, 2)

def nearest_neighbor_tsp(dist_matrix: Dict[str, Dict[str, float]], start_node: str = "Depot") -> Tuple[List[str], float]:
    unvisited = set(dist_matrix.keys())
    if start_node not in unvisited:
        return [start_node], 0.0

    tour = [start_node]
    unvisited.remove(start_node)
    curr = start_node
    total_cost = 0.0

    while unvisited:
        next_node = min(unvisited, key=lambda node: dist_matrix[curr].get(node, float('inf')))
        cost = dist_matrix[curr][next_node]
        if cost == float('inf'):
            break
        total_cost += cost
        tour.append(next_node)
        unvisited.remove(next_node)
        curr = next_node

    return_cost = dist_matrix[curr].get(start_node, 0.0)
    total_cost += return_cost
    tour.append(start_node)

    return tour, round(total_cost, 2)

def two_opt_tsp(dist_matrix: Dict[str, Dict[str, float]], start_node: str = "Depot", max_iterations: int = 500) -> Tuple[List[str], float]:
    tour, best_dist = nearest_neighbor_tsp(dist_matrix, start_node)
    if len(tour) <= 3:
        return tour, best_dist

    improved = True
    iterations = 0

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        n = len(tour)

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                a, b = tour[i - 1], tour[i]
                c, d = tour[j], tour[j + 1]

                current_edges = dist_matrix[a][b] + dist_matrix[c][d]
                new_edges = dist_matrix[a][c] + dist_matrix[b][d]

                if new_edges < current_edges - 1e-6:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
                    break
            if improved:
                break

    best_dist = calculate_tour_distance(tour, dist_matrix)
    return tour, best_dist

def compare_tsp_algorithms(dist_matrix: Dict[str, Dict[str, float]], start_node: str = "Depot") -> Dict[str, Any]:
    nn_tour, nn_cost = nearest_neighbor_tsp(dist_matrix, start_node)
    two_opt_tour, two_opt_cost = two_opt_tsp(dist_matrix, start_node)
    improvement = round(nn_cost - two_opt_cost, 2)
    improvement_pct = round((improvement / nn_cost) * 100, 2) if nn_cost > 0 else 0.0

    return {
        "nearest_neighbor": {"tour": nn_tour, "distance": nn_cost},
        "two_opt": {"tour": two_opt_tour, "distance": two_opt_cost},
        "distance_saved": max(0.0, improvement),
        "improvement_percent": max(0.0, improvement_pct)
    }
