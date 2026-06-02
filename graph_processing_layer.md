# Graph Processing Layer (Production Design)

## 1. Overview

The Graph Processing Layer is responsible for transforming a **raw graph** (generated from the injection layer) into a **clean, normalized, and production-ready graph**.

### Input

* Raw graph (nodes + edges)
* May contain:

  * Duplicate nodes
  * Inconsistent naming
  * Invalid edges

### Output

* Clean graph
* Consistent IDs
* Valid relationships
* Enriched metadata

---

## 2. Responsibilities

### 2.1 Normalization

Standardizes node identifiers and attributes.

Example:
"Aadhaar Check" → "aadhaar_check"

---

### 2.2 Deduplication

Merges duplicate nodes based on normalized keys.

Example:
"Aadhaar", "aadhaar", "AADHAAR" → single node

---

### 2.3 Validation

Ensures graph integrity:

* All edges refer to valid nodes
* No broken references

---

### 2.4 Enrichment

Adds metadata:

* Node types
* Default attributes

---

## 3. Architecture

```
Raw Graph
   ↓
Normalizer
   ↓
Deduplicator
   ↓
Validator
   ↓
Processed Graph
```

---

## 4. Components

### 4.1 GraphNormalizer

* Cleans names
* Standardizes IDs

### 4.2 GraphDeduplicator

* Merges duplicate nodes
* Rewrites edges

### 4.3 GraphValidator

* Checks integrity

### 4.4 GraphProcessor

* Orchestrates full pipeline

---

## 5. Data Model

```json
{
  "nodes": [
    { "id": "aadhaar_check", "type": "rule" }
  ],
  "edges": [
    { "source": "rule_a", "target": "aadhaar_check" }
  ]
}
```

---

## 6. Guarantees

After processing:

* No duplicate nodes
* All edges valid
* Consistent naming
* Ready for storage & analysis

---
```text

project/
│
├── ingestion/
│   ├── excel_reader.py
│   ├── validator.py
│   ├── transformer.py
│   └── service.py
│
├── graph/
│   ├── extractor.py
│   ├── processor.py
│   ├── normalizer.py
│   ├── deduplicator.py
│   ├── validator.py
│   └── repository.py
│
├── versioning/
│   ├── manager.py
│
├── diff/
│   ├── engine.py
│
├── intelligence/
│   ├── impact.py
│
├── simulation/
│   ├── engine.py
│
├── models/
│   ├── graph.py
│   ├── rule.py
│
├── api/
│   ├── routes.py
│
├── core/
│   ├── config.py
│   ├── db.py
│
└── main.py
```

