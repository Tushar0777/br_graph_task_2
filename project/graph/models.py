from dataclasses import dataclass,field
from typing import List,Dict

@dataclass(frozen=True)
class Node:
    id:str
    type:str="unknown"
    metadata:Dict[str,any]=field(default_factory=dict)
    # metadata :Dict={} would have been a bad design as 
    # it would have been shared across all instances of Node 
    # Because mutable defaults are shared.

@dataclass(frozen=True)
class Edge:
    source:str
    target:str
    type:str="depends_on"

@dataclass(frozen=True)
class Graph:
    nodes: List[Node]
    edges: List[Edge]

