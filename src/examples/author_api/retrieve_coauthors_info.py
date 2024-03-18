""" Retrieves co-author information using :class:`CoAuthorsRetriever` class.

This script retrieves information about the co-authors of a specific author using the CoAuthorsRetriever class from the scholar_retriever module.

Usage:
------

    1. Make sure you have the scholar_retriever module and its dependencies installed.
    2. Modify the variable ``author_identifier`` with the corresponding author identifier.
    3. Run the script.

Example usage:
--------------

python retrieve_coauthors_info.py
"""




import json

# Import the CoAuthorsRetriever class from the scholar_retriever module
from scholar_retriever import CoAuthorsRetriever

# Identifier of the author for whom co-authors' information is desired
author_identifier = 'M4l534gAAAAJ'

# Create an instance of CoAuthorsRetriever with the author identifier and language 'en' (English)
coauthor_retriever = CoAuthorsRetriever(author_identifier, 'en')

# Attempt to retrieve information about the co-authors of the author
success, reason = coauthor_retriever.fetch()

# Check if the retrieval was successful
if not success:
    # Print the error if the retrieval was unsuccessful
    print(f'Error:{reason}')
else:
    # Get the co-authors' information
    info = coauthor_retriever.get_json()
    
    # Print the co-authors' information in JSON format with formatting and without escaping non-ASCII characters
    print(json.dumps(info, indent=2, ensure_ascii=False))
