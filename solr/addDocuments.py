import pysolr
import json

# Connect to Solr
solr_url = 'http://localhost:8983/solr/hybrid_search'
solr = pysolr.Solr(solr_url, always_commit=True, timeout=10)

# Example data
data = [
    {"content": "Learn the basics of Python."},
    {"content": "Advanced data analysis techniques."},
    # Add more documents
]

# Add documents to Solr
solr.add(data)

print("Data indexed successfully.")
