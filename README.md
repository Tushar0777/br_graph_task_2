# Rule Graph Engine

> A lightweight, production-oriented graph processing engine for dependency systems.

Built to model, normalize, deduplicate, and validate graph structures in a clean transformation pipeline.

Designed with **Low-Level Design (LLD)** principles, **separation of concerns**, and **production-grade maintainability** in mind.

---

## Why This Project Exists

In dependency-driven systems, raw graph data is often inconsistent.

Example:

```text
" Rule A "
"RULE A"
"Rule A"
```

All represent the same logical node.

Without preprocessing:

- graph traversal breaks
- dependency mapping becomes inconsistent
- duplicate nodes appear
- invalid references corrupt downstream systems

This project solves that problem through a structured processing pipeline:

```text
Raw Graph
    ↓
Normalize IDs
    ↓
Remove Duplicates
    ↓
Validate Integrity
    ↓
Clean Graph
```

---

## Features

### Graph Modeling

Simple graph abstraction:

- **Node**
- **Edge**
- **Graph**

Example:

```text
Rule_A ───depends_on───> Rule_B
```

---

### Graph Normalization

Standardizes node identifiers.

Transforms:

| Raw Input | Normalized |
|-----------|-------------|
| ` Rule A ` | `rule_a` |
| `RULE A` | `rule_a` |
| `Rule@1` | `rule1` |

Normalization rules:

- trim whitespace
- lowercase conversion
- whitespace → underscore
- remove special characters

---

### Graph Deduplication

Removes duplicate nodes after normalization.

Example:

Before:

```text
rule_a
rule_a
rule_b
```

After:

```text
rule_a
rule_b
```

Also removes invalid edges referencing missing nodes.

---

### Graph Validation

Ensures graph integrity.

Checks:

- edge source exists
- edge target exists
- graph consistency

Example invalid graph:

```text
R1 ───depends_on───> R999
```

Raises:

```python
ValueError("Invalid edge target: R999")
```

---

# Architecture

The project follows a **pipeline-based architecture**.

Each layer has **exactly one responsibility**.

```text
GraphNormalizer
        ↓
GraphDeduplicator
        ↓
GraphValidator
```

This follows:

- Single Responsibility Principle (SRP)
- Immutable transformations
- Composable processing stages
- Clean architecture

---

## Project Structure

```text
project/
│
├── graph/
│   ├── __init__.py
│   ├── models.py
│   ├── normalization.py
│   ├── deduplicator.py
│   └── validator.py
│
├── tests/
│   └── graph/
│       ├── test_normalization.py
│       ├── test_deduplicator.py
│       ├── test_validator.py
│       └── test_pipeline.py
│
├── pyproject.toml
└── README.md
```

---

# Low-Level Design (LLD)

## 1. Graph Models

Located in:

```text
graph/models.py
```

The domain model is intentionally minimal.

### Node

Represents a graph entity.

```python
Node(
    id="rule_a",
    type="rule",
    metadata={}
)
```

Responsibilities:

- unique identifier
- optional type classification
- extensible metadata storage

---

### Edge

Represents a directed relationship.

```python
Edge(
    source="rule_a",
    target="rule_b",
    type="depends_on"
)
```

Graph relationship:

```text
rule_a ───depends_on───> rule_b
```

---

### Graph

Container object.

```python
Graph(
    nodes=[],
    edges=[]
)
```

Acts as the shared contract between all processors.

---

# Processing Pipeline

## 1. Graph Normalization

File:

```text
graph/normalization.py
```

### Goal

Convert inconsistent IDs into a standardized format.

Example:

Before:

```text
" Rule A "
"RULE A"
"Rule A"
```

After:

```text
rule_a
rule_a
rule_a
```

### Why normalization happens first

Real-world systems contain inconsistent naming.

Without normalization:

```text
Rule A
rule_a
RULE_A
```

would become different graph nodes.

Normalization ensures deterministic IDs.

### Responsibility

**Only transform data.**

The normalizer intentionally **does not validate duplicates**.

Reason:

Duplicate handling belongs to the deduplication layer.

This keeps responsibilities isolated.

---

## 2. Graph Deduplication

File:

```text
graph/deduplicator.py
```

### Goal

Remove duplicate nodes created after normalization.

Example:

Input:

```text
rule_a
rule_a
rule_b
```

Output:

```text
rule_a
rule_b
```

### Why deduplication is separate

Alternative design:

```text
Normalizer → detect duplicates
```

Problem:

Breaks separation of concerns.

A normalizer should:

```text
transform only
```

A deduplicator should:

```text
remove duplicates only
```

This improves:

- readability
- maintainability
- testability

---

## 3. Graph Validation

File:

```text
graph/validator.py
```

### Goal

Guarantee graph integrity.

Checks:

```text
edge.source exists
edge.target exists
```

Example:

Broken graph:

```text
R1 ───> R999
```

Validator:

```python
raise ValueError(
    "Invalid edge target: R999"
)
```

### Why validation is last

Validation happens after cleanup.

Pipeline logic:

```text
Normalize
    ↓
Deduplicate
    ↓
Validate
```

Why?

Because validating before cleanup would produce unnecessary failures.

Example:

```text
duplicate nodes
temporary invalid edges
```

may be fixed during processing.

---

# Design Decisions

## Why Pipeline Architecture?

Instead of:

```python
process_graph()
```

with 500 lines of logic.

We split responsibilities.

Benefits:

### 1. Composability

Easy to extend:

```text
Normalizer
    ↓
Deduplicator
    ↓
CycleDetector
    ↓
Validator
```

---

### 2. Testability

Every stage can be tested independently.

Example:

```python
test_normalizer()

test_deduplicator()

test_validator()
```

instead of testing a giant function.

---

### 3. Maintainability

Changes remain isolated.

Example:

Changing normalization rules:

```text
normalization.py
```

No risk of breaking validation logic.

---

### 4. Production Safety

Immutable transformations.

Each processor:

```python
process(graph) -> Graph
```

returns a new graph.

No hidden mutations.

This reduces side effects.

---

# Complexity Analysis

| Component | Complexity |
|-----------|------------|
| Normalizer | O(N + E) |
| Deduplicator | O(N + E) |
| Validator | O(N + E) |

Where:

- `N` = nodes
- `E` = edges

Efficient for:

```text
100k+ nodes
millions of edges
```

---

# Installation

Clone repository:

```bash
git clone <repo-url>
cd project
```

Install dependencies:

```bash
pip install -e ".[dev]"
```

---

# Quick Start

## Create Graph

```python
from graph.models import (
    Graph,
    Node,
    Edge
)

graph = Graph(
    nodes=[
        Node(" Rule A "),
        Node("Rule A"),
        Node("Rule B")
    ],
    edges=[
        Edge(
            " Rule A ",
            "Rule B"
        )
    ]
)
```

---

## Run Pipeline

```python
from graph.normalization import GraphNormalizer
from graph.deduplicator import GraphDeduplicator
from graph.validator import GraphValidator

graph = (
    GraphNormalizer()
    .process(graph)
)

graph = (
    GraphDeduplicator()
    .process(graph)
)

graph = (
    GraphValidator()
    .process(graph)
)
```

Result:

```text
rule_a ───depends_on───> rule_b
```

---

# Testing

This project follows a layered testing approach.

### Unit Tests

Each processor tested independently.

```text
test_normalization.py
test_deduplicator.py
test_validator.py
```

### Integration Tests

Full pipeline testing.

```text
Normalize
    ↓
Deduplicate
    ↓
Validate
```

Run tests:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Coverage:

```bash
pytest --cov=graph
```

---

# Production Considerations

This project intentionally focuses on:

### Deterministic Processing

Same input → same output.

---

### Immutable Pipeline

No hidden graph mutation.

---

### Separation of Concerns

Each layer has one responsibility.

---

### Extensibility

Easy to add:

- cycle detection
- topological sorting
- dependency scoring
- graph traversal
- DAG validation

Example future pipeline:

```text
Normalize
    ↓
Deduplicate
    ↓
Cycle Detection
    ↓
Dependency Scoring
    ↓
Validate
```

---

# Interview Talking Points

This project demonstrates:

### Low-Level Design

- domain modeling
- clean abstractions
- pipeline architecture

### SOLID Principles

Especially:

```text
Single Responsibility Principle
```

---

### Clean Code

- small focused services
- isolated responsibilities
- composable pipeline

---

### Testing Strategy

- unit tests
- integration tests
- failure scenarios

---

### Scalability Thinking

Uses:

```text
set → O(1) lookup
dict → O(1) deduplication
```

instead of nested loops.

Avoids:

```text
O(N²)
```

operations.

---

# Future Improvements

Potential roadmap:

### Graph Algorithms

- BFS
- DFS
- cycle detection
- shortest path
- topological sort

### Storage

- JSON export
- GraphML support

### Integrations

- NetworkX
- Neo4j
- visualization layer

### Validation

- self-loop detection
- DAG enforcement
- schema validation

---

# License

MIT


# Versioning Module

A lightweight graph versioning system designed to maintain immutable snapshots of graph states over time.

This module enables:

* **Graph snapshot versioning**
* **Rollback to historical states**
* **Version history tracking**
* **Immutable storage**
* **Diff preparation for dependency detection**

The system follows a clean layered architecture using a **Manager + Repository pattern**, making it easy to replace in-memory storage with databases such as PostgreSQL later.

---

# Why Versioning?

In graph-based rule systems, overwriting graph state is dangerous.

Problems with overwriting:

* No rollback capability
* No audit/history tracking
* Difficult debugging
* Hard to compare graph changes

Instead of mutating existing graphs, the system stores **immutable snapshots**.

Example:

```text
V1 → Initial graph
V2 → Added node
V3 → Removed dependency
```

If a bad update happens:

```text
rollback(V1)
```

the system creates:

```text
V4 → copy of V1
```

instead of modifying history.

This preserves a complete audit trail.

---

# Folder Structure

```text
versioning/
│
├── models.py
├── repository.py
├── manager.py
```

---

# Architecture

The module follows a layered design:

```text
Application
      ↓
VersionManager
      ↓
VersionRepository
      ↓
Storage (In-Memory / PostgreSQL)
```

### Responsibilities

| Layer           | Responsibility    |
| --------------- | ----------------- |
| `models.py`     | Domain models     |
| `repository.py` | Persistence logic |
| `manager.py`    | Business logic    |

---

# Components

## 1. GraphVersion (`models.py`)

Represents a snapshot of a graph.

### Responsibilities

* Store graph state
* Store version metadata
* Track creation timestamp

### Model

```python
@dataclass
class GraphVersion:
    version_id: int
    created_at: datetime
    graph: Graph
```

### Why this exists

Returning only `Graph` loses useful metadata:

```text
version_id
created_at
audit history
```

Using `GraphVersion` preserves complete version information.

---

## 2. VersionRepository (`repository.py`)

Handles persistence of graph snapshots.

Current implementation uses:

```text
In-memory storage
```

but can later be replaced with:

* PostgreSQL
* Redis
* Object storage

without changing manager logic.

### Responsibilities

* Save graph versions
* Retrieve latest version
* Retrieve historical versions
* List available versions
* Serialize/deserialize graphs

### Core APIs

#### Save Graph

```python
save(graph)
```

Creates immutable snapshot.

Example:

```text
Graph → Version 1
```

---

#### Get Latest Version

```python
get_latest()
```

Returns:

```text
Most recent GraphVersion
```

---

#### Get Specific Version

```python
get_by_version(version_id)
```

Example:

```python
repo.get_by_version(2)
```

Returns graph snapshot from version 2.

---

#### List Versions

```python
list_versions()
```

Example:

```python
[1, 2, 3, 4]
```

---

### Serialization

Since databases cannot store Python objects directly:

```text
Graph object
    ↓
Serialized dictionary
    ↓
Storage
```

On retrieval:

```text
Stored dictionary
    ↓
Deserialization
    ↓
Graph object
```

This makes the system database-friendly.

---

## 3. VersionManager (`manager.py`)

Contains business logic.

The manager sits above repository and orchestrates operations.

### Responsibilities

* Create graph versions
* Fetch latest version
* Fetch historical versions
* Prepare graph diff input
* Handle rollback logic

---

### Create Version

```python
create_version(graph)
```

Creates a new graph snapshot.

---

### Get Latest

```python
get_latest()
```

Returns latest `GraphVersion`.

---

### Get Version

```python
get_version(version_id)
```

Returns historical snapshot.

---

### Diff Input

```python
get_diff_input(new_graph)
```

Returns:

```python
(old_graph, new_graph)
```

Used for graph comparison or dependency detection.

Example:

```text
Old Graph (V2)
        vs
New Graph
```

---

### Rollback

```python
rollback(version_id)
```

Rollback **does not overwrite history**.

Instead:

```text
V1
V2
V3
rollback(V1)
```

becomes:

```text
V1
V2
V3
V4 ← copy of V1
```

This ensures immutable history.

---

# Example Usage

```python
from versioning.repository import (
    VersionRepository
)

from versioning.manager import (
    VersionManager
)

repo = VersionRepository()

manager = VersionManager(repo)

# Save graph
v1 = manager.create_version(graph)

# Get latest version
latest = manager.get_latest()

# Get version by ID
old = manager.get_version(1)

# Rollback
manager.rollback(1)
```

---

# Design Decisions

## Why Repository Pattern?

Keeps storage separate from business logic.

Without repository:

```text
Manager → Database queries
```

Tightly coupled.

With repository:

```text
Manager
   ↓
Repository
   ↓
Storage
```

Easy to swap persistence layers.

---

## Why Immutable Snapshots?

Avoid accidental mutations.

Bad approach:

```text
Version 1 changes unexpectedly
```

Correct approach:

```text
Every save = frozen snapshot
```

This improves:

* reliability
* rollback safety
* debugging

---

## Why Rollback Creates New Version?

Mutating history breaks traceability.

Wrong:

```text
V2 overwritten
```

Correct:

```text
V5 = copy(V2)
```

This preserves audit history.

---

# Testing

Tests are located in:

```text
tests/versioning/
```

Run only versioning tests:

```bash
pytest tests/versioning -v
```

Run one file:

```bash
pytest tests/versioning/test_repository.py -v
```

---

# Future Improvements

### PostgreSQL Support

Replace in-memory storage with:

```text
PostgreSQL + JSONB
```

for persistence.

---

### Delta-Based Versioning

Current system stores:

```text
Full graph snapshot
```

Future optimization:

```text
Only graph changes
```

(similar to Git)

---

### Version Metadata

Possible future additions:

```text
created_by
change_reason
commit_message
checksum
```

---

# Complexity

| Operation     | Complexity |
| ------------- | ---------- |
| Save          | O(1)       |
| Get Latest    | O(1)       |
| Get Version   | O(1)       |
| List Versions | O(n)       |

---

# Summary

This module provides a clean, extensible versioning system for graph-based rule engines using immutable snapshots, rollback support, and layered architecture.

It is designed to be simple for local development while remaining extensible for production databases such as PostgreSQL.
