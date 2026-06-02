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
