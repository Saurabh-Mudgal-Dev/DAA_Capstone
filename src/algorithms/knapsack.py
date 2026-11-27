from typing import List, Tuple
from ..models import Parcel

def knapsack_01(parcels: List[Parcel], capacity: int) -> Tuple[int, List[Parcel], List[List[int]]]:
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        p = parcels[i - 1]
        for w in range(capacity + 1):
            if p.weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - p.weight] + p.value)
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1].weight

    selected.reverse()
    max_value = dp[n][capacity]
    return max_value, selected, dp

def knapsack_01_space_optimized(parcels: List[Parcel], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for p in parcels:
        for w in range(capacity, p.weight - 1, -1):
            dp[w] = max(dp[w], dp[w - p.weight] + p.value)
    return dp[capacity]

def fractional_knapsack_greedy(parcels: List[Parcel], capacity: int) -> Tuple[float, List[Tuple[Parcel, float]]]:
    sorted_by_ratio = sorted(parcels, key=lambda p: p.ratio, reverse=True)
    total_val = 0.0
    remaining_w = capacity
    selected = []

    for p in sorted_by_ratio:
        if remaining_w <= 0:
            break
        if p.weight <= remaining_w:
            selected.append((p, 1.0))
            total_val += p.value
            remaining_w -= p.weight
        else:
            fraction = remaining_w / p.weight
            selected.append((p, round(fraction, 2)))
            total_val += p.value * fraction
            remaining_w = 0

    return round(total_val, 2), selected

def print_dp_table(dp: List[List[int]], parcels: List[Parcel], capacity: int, max_cols: int = 16):
    cols = list(range(capacity + 1))
    if capacity + 1 > max_cols:
        disp_cols = cols[:8] + cols[-5:]
        has_ellipsis = True
    else:
        disp_cols = cols
        has_ellipsis = False

    header = f"{'Item / W':<12}"
    if has_ellipsis:
        header += "".join(f"{w:>4}" for w in disp_cols[:8]) + " ..." + "".join(f"{w:>4}" for w in disp_cols[8:])
    else:
        header += "".join(f"{w:>4}" for w in disp_cols)

    print(header)
    print("-" * len(header))

    for i in range(len(dp)):
        label = "0 (init)" if i == 0 else f"{parcels[i - 1].id} (w={parcels[i - 1].weight})"
        row_str = f"{label:<12}"
        if has_ellipsis:
            row_str += "".join(f"{dp[i][w]:>4}" for w in disp_cols[:8]) + " ..." + "".join(f"{dp[i][w]:>4}" for w in disp_cols[8:])
        else:
            row_str += "".join(f"{dp[i][w]:>4}" for w in disp_cols)
        print(row_str)
