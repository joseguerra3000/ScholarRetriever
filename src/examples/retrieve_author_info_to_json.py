""" Use of :class:`AuthorInfoRetriever` class for get information about several authors.

This script retrieves information about authors from Google Scholar using their identifiers.

Usage:
------

    1. Make sure you have installed the scholar_retriever module and its dependencies.
    2. Modify the variable `author_identifiers` with the corresponding author identifiers.
    3. Run the script.

Example usage:
--------------

python author_info_to_json.py

"""



import json
from scholar_retriever import AuthorInfoRetriever

# List of author identifiers for which information is desired
author_identifiers = [
    'X_M530AAAAAJ',
    'i3gYBKIAAAAJ',
    'qSHS-XQAAAAJ',
    'WupYDZsAAAAJ'
]

# Create an instance of AuthorInfoRetriever with English as the language
author_retriever = AuthorInfoRetriever(hl='en')

def retrieve_author(author: str):
    """
    Retrieve information about an author using their identifier.
    
    Args:
        author (str): The identifier of the author.
        
    Returns:
        dict: A dictionary containing information about the author.
    """
    author_retriever.author_id = author

    # Attempt to retrieve information about the author
    success, reason = author_retriever.fetch()

    # Check if the retrieval was successful
    if not success:
        # Print the error if the retrieval was unsuccessful
        print(f'Error: {reason}')
        return {}
    else:
        # Get the author information
        info = author_retriever.get_json()
        return info

if __name__ == '__main__':
    # Retrieve information for each author identifier
    authors_info = [retrieve_author(id) for id in author_identifiers]
        
    # Print the information in JSON format
    print(json.dumps(authors_info, indent=2, ensure_ascii=False))
