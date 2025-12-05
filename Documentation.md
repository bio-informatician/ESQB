# FluentES (fluentes) Documentation

---

## Overview

**FluentES** (`fluentes`) is a Python library for building Elasticsearch queries using a **fluent API**. It allows developers to construct complex Elasticsearch queries in a readable and composable way, without manually writing JSON DSL.

- GitHub: https://github.com/bio-informatician/FluentES
- PyPI: https://pypi.org/project/fluentes/
- License: MIT

---

## Installation

```bash
pip install fluentes==0.1.0
```

Requires Python >= 3.8.

---

## Quick Start

```python
from fluentes import QueryBuilder
from elasticsearch import Elasticsearch
import os

ES_HOST = os.getenv("ELASTIC_URL_PORT")
ES_USER = os.getenv("ELASTIC_USER")
ES_PASSWORD = os.getenv("ELASTIC_PASSWORD")
CERT = "PATH_TO_CERT"

es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USER, ES_PASSWORD),
    verify_certs=True,
    ca_certs=CERT
)

query = (
    QueryBuilder()
    .term("0am", "2655", occurrence="must")
    .term("0gh", "Retroviridae", occurrence="must")
    .term("0af", "USA", occurrence="filter")
    .terms("0al", ["Homo sapiens", "Pan troglodytes"], occurrence="filter")
    .build()
)

response = es.search(index="ES_DATABASE_INDEX", body=query)

for hit in response['hits']['hits']:
    print(hit['_source'])
```

**Explanation:**
- `.term(field, value, occurrence)` → exact match for a field.
- `.terms(field, [values], occurrence)` → matches any value in the list.
- `occurrence` can be `must`, `filter`, `should`, or `must_not`.
- `.build()` generates the final Elasticsearch query dict.

---

## QueryBuilder Class

### **Initialization**

```python
qb = QueryBuilder(size=10, source=None, min_score=None)
```

- `size`: number of results to return (default 10)
- `source`: list of fields to include in `_source`
- `min_score`: minimum score for document inclusion

---

### **Clause Methods**

| Method | Description | Occurrence |
|--------|-------------|------------|
| `match(field, query, occurrence='should', boost=None, analyzer=None)` | Match text using analyzed field | must / should / filter / must_not |
| `match_phrase(field, query, occurrence='should', boost=None, slop=None)` | Match exact phrase | must / should / filter / must_not |
| `term(field, value, occurrence='filter', boost=None)` | Exact match (keyword) | must / should / filter / must_not |
| `terms(field, values, occurrence='filter')` | Matches any value in a list | must / should / filter / must_not |
| `range(field, occurrence='must', gte=None, gt=None, lte=None, lt=None)` | Numeric/date range query | must / should / filter / must_not |
| `wildcard(field, value, occurrence='should', boost=None)` | Wildcard pattern match | must / should / filter / must_not |
| `exists(field, occurrence='must')` | Checks that field exists | must / should / filter / must_not |
| `query_string(query, default_field=None, occurrence='should')` | Search without specifying field | must / should / filter / must_not |
| `geo_distance(field, lat, lon, distance, occurrence='filter')` | Geo-distance query | must / should / filter / must_not |

---

### **Aggregations**

```python
qb.aggregation(name='top_tags', agg_type='terms', field='tags', size=10)
```
- Adds Elasticsearch aggregation.
- `name`: aggregation key
- `agg_type`: type of aggregation (`terms`, `avg`, `sum`, etc.)
- Additional kwargs passed to aggregation body

---

### **Highlighting**

```python
qb.highlight(fields=['title', 'abstract'], pre_tags=['<b>'], post_tags=['</b>'])
```
- Highlights matched terms in specified fields
- `pre_tags` / `post_tags` are HTML tags

---

### **Setters**

- `.size(n)` → set number of results
- `.source([fields])` → include only specified fields
- `.min_score(score)` → set minimum score threshold

---

### **Build Query**

```python
query_dict = qb.build()
```
- Returns Elasticsearch query as a Python dictionary
- Alias: `.to_dict()`

---

## **Boolean Occurrences**

- The `_bool` dict internally stores: `must`, `should`, `filter`, `must_not`
- Pass `occurrence="filter"` (or `"must"`, `"should"`, `"must_not"`) in **any clause**
- Example:

```python
qb.term('tax_id', '351418', occurrence='must')
qb.term('status', 'active', occurrence='filter')
qb.terms('category', ['bacteria', 'virus'], occurrence='should')
```

---

## **Searching Without Field**

Use `.query_string()` to search across default fields:

```python
qb.query_string('Retroviridae')
```
- Optionally, restrict to a field: `default_field='0gh'`

---

## **Filters and Multiple Values**

- Use `occurrence='filter'` for filter clauses
- Use `.terms()` for OR-match on multiple values

```python
qb.terms('0al', ['Homo sapiens', 'Pan troglodytes'], occurrence='filter')
```
- Only documents with `0al` matching any of the values are returned.

---

## **Putting It All Together**

```python
query = (
    QueryBuilder()
    .term('0am', '2655', occurrence='must')
    .term('0gh', 'Retroviridae', occurrence='must')
    .term('0af', 'USA', occurrence='filter')
    .terms('0al', ['Homo sapiens', 'Pan troglodytes'], occurrence='filter')
    .query_string('envelope glycoprotein', occurrence='should')
    .build()
)
```
- Combines must, filter, should clauses and full-text search.

---

## **Contributing**

- Fork repository, create feature branch, submit PR
- Add tests for new functionality
- Follow consistent code style

---

## **License**

MIT License

---

