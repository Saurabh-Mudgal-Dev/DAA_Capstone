from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

@dataclass
class Parcel:
    id: str
    weight: int
    value: int
    deadline: int
    destination: str

    @property
    def ratio(self) -> float:
        return round(self.value / self.weight, 2) if self.weight > 0 else 0.0

    @property
    def urgency_tier(self) -> str:
        if self.deadline <= 30:
            return "Urgent"
        if self.deadline <= 60:
            return "High"
        return "Standard"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "weight": self.weight,
            "value": self.value,
            "deadline": self.deadline,
            "destination": self.destination,
            "ratio": self.ratio,
            "urgency": self.urgency_tier
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Parcel":
        return cls(
            id=data["id"],
            weight=int(data["weight"]),
            value=int(data["value"]),
            deadline=int(data["deadline"]),
            destination=data["destination"]
        )

class RoadGraph:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        self._edge_count = 0

    def add_edge(self, u: str, v: str, weight: float):
        if weight < 0:
            raise ValueError(f"Dijkstra requires non-negative edge weights. Got {weight} between {u} and {v}")
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        self._edge_count += 1

    def get_nodes(self) -> List[str]:
        return list(self.adj.keys())

    def has_node(self, u: str) -> bool:
        return u in self.adj

    def neighbors(self, u: str) -> List[Tuple[str, float]]:
        return self.adj.get(u, [])

    def edge_count(self) -> int:
        return self._edge_count

    def get_weight(self, u: str, v: str) -> float:
        for neighbor, weight in self.adj.get(u, []):
            if neighbor == v:
                return weight
        return float('inf')
