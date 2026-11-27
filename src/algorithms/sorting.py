from typing import List
from ..models import Parcel

def merge_sort_parcels(parcels: List[Parcel], key: str = "deadline", reverse: bool = False) -> List[Parcel]:
    if len(parcels) <= 1:
        return list(parcels)

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid], key, reverse)
    right = merge_sort_parcels(parcels[mid:], key, reverse)

    val_l_last = getattr(left[-1], key)
    val_r_first = getattr(right[0], key)
    in_order = (val_l_last >= val_r_first) if reverse else (val_l_last <= val_r_first)
    if in_order:
        return left + right

    return _merge(left, right, key, reverse)

def _merge(left: List[Parcel], right: List[Parcel], key: str, reverse: bool) -> List[Parcel]:
    merged = []
    i = j = 0
    n_left, n_right = len(left), len(right)

    while i < n_left and j < n_right:
        val_l = getattr(left[i], key)
        val_r = getattr(right[j], key)
        condition = (val_l >= val_r) if reverse else (val_l <= val_r)
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    if i < n_left:
        merged.extend(left[i:])
    if j < n_right:
        merged.extend(right[j:])
    return merged

def quick_sort_parcels(parcels: List[Parcel], key: str = "deadline", reverse: bool = False) -> List[Parcel]:
    arr = list(parcels)
    _quicksort_helper(arr, 0, len(arr) - 1, key, reverse)
    return arr

def _quicksort_helper(arr: List[Parcel], low: int, high: int, key: str, reverse: bool):
    if low < high:
        lt, gt = _partition_3way(arr, low, high, key, reverse)
        _quicksort_helper(arr, low, lt - 1, key, reverse)
        _quicksort_helper(arr, gt + 1, high, key, reverse)

def _partition_3way(arr: List[Parcel], low: int, high: int, key: str, reverse: bool):
    mid = (low + high) // 2
    candidates = [(getattr(arr[low], key), low), (getattr(arr[mid], key), mid), (getattr(arr[high], key), high)]
    candidates.sort(key=lambda x: x[0], reverse=reverse)
    median_idx = candidates[1][1]
    arr[low], arr[median_idx] = arr[median_idx], arr[low]

    pivot = getattr(arr[low], key)
    lt = low
    i = low + 1
    gt = high

    while i <= gt:
        val = getattr(arr[i], key)
        if (val > pivot if reverse else val < pivot):
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif (val < pivot if reverse else val > pivot):
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    return lt, gt
