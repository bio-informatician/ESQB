# FluentES — Elasticsearch Fluent Query Builder

[![PyPI version](https://img.shields.io/pypi/v/fluentes.svg)](https://pypi.org/project/fluentes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What is FluentES

FluentES is a small Python library for building Elasticsearch queries via a fluent (method-chaining) API.  
It allows you to construct complex search or filtering queries for Elasticsearch in a readable and composable way — without manually writing raw query JSON.

## Why use it

- Builds on standard Python, for easy integration into existing Elasticsearch workflows  
- Provides a clean, chainable interface instead of manual JSON dict construction  
- Useful when you want to programmatically build or modify queries — e.g., dynamic filtering, conditional clauses, pipelines, etc.

## Install / Requirements

```bash
pip install fluentes==0.1.0
```

Requires **Python ≥ 3.8**.

## Quick Start Example

```python
from fluentes import QueryBuilder

q = (
    QueryBuilder()
    .match("title", "python")
    .term("status", "active")
    .build()
)

print(q)
# Output might be something like:
# {
#   "bool": {
#     "must": [
#       {"match": {"title": "python"}},
#       {"term": {"status": "active"}}
#     ]
#   }
# }
```

This builds a query that matches documents where 'title' contains "python" and 'status' is "active".

## Usage / API Reference

- `QueryBuilder()` — start a new query  
- `.match(field: str, value: Any)` — add a “match” clause  
- `.term(field: str, value: Any)` — add a “term” clause  
- `.bool()` / `.must()` / `.should()` / `.filter()` — combine clauses  
- `.build()` — generate the final Elasticsearch‑compatible query (Python dict or JSON)

## Contribute / Development

- Fork the repository  
- Create a new branch (feature / bugfix)  
- Write tests if adding functionality  
- Ensure code style / linting (if applicable)  
- Submit a Pull Request

You may also include a `CONTRIBUTING.md` & optionally a `CODE_OF_CONDUCT.md` file.

## License

FluentES is released under the MIT License — see the [`LICENSE`](LICENSE) file for details.

## Roadmap / Future Work

- Support for aggregations, sort, pagination  
- Support for nested queries / boolean combinations  
- Integration with newer Elasticsearch versions or high-level client libraries

