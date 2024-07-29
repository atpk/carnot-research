import pysolr

# Connect to Solr
solr_url = 'http://localhost:8983/solr/hybrid_search'
solr = pysolr.Solr(solr_url, always_commit=True, timeout=10)

def keyword_search(query):
    # Use edismax query parser for flexible search
    query_string = f'{query}'
    params = {
        'defType': 'edismax',       # Use edismax query parser
        'qf': 'title content',      # Fields to search
        'q': query_string,          # Query string
        'mm': '60%'                # Minimum match (60% means minimum 3/5 terms in query must match)
    }
    results = solr.search(**params)
    print(f'Keyword search results: {results}')
    return results

# Keyword search
query = "Blefuscu learn embargo python lilliput"
results = keyword_search(query)
print("Results are:")
for result in results:
    print(result)  # Print each result object
