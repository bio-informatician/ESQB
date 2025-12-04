from esqb_files.query_builder import QueryBuilder

# Build a sample ES query
query = Q.boolean(
    must=[
        Q.match("title", "python"),
        Q.range("published_at", gte="2020-01-01"),
    ],
    filter=[
        Q.term("status", "active")
    ]
)

print(query.to_dict())
