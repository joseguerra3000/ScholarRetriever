""" Basic use of ``AuthorInfoRetriever`` class.

This script uses the AuthorInfoRetriever class from the scholar_retriever module
to retrieve information about an author using their identifier.

Usage:
------

	1. Make sure you have the scholar_retriever module and its dependencies installed.
	2. Modify the variable `author_identifier` with the corresponding author identifier.
	3. Run the script.

Example usage:
--------------

python author_info_print.py

"""


# Import the AuthorInfoRetriever class from the scholar_retriever module
from scholar_retriever import AuthorInfoRetriever

# Identifier of the author for which information is desired
author_identifier = 'X_M530AAAAAJ'

# Create an instance of AuthorInfoRetriever with the author identifier and language 'en' (English)
author_retriever = AuthorInfoRetriever(author_identifier, 'en')

# Attempt to retrieve information about the author
success, reason = author_retriever.fetch()

# Check if the retrieval was successful
if not success:
    # Print the error if the retrieval was unsuccessful
    print(f'Error:{reason}')
else:
    # Get the author information in JSON format
    info = author_retriever.get_json()
    
    # Print the author information
    print('Author Info:')
    print('------------')
    # Print the author's name
    print(f"Name: {info['author']['name']}")
    # Print the author's thumbnail
    print(f"Thumbnail: {info['author']['thumbnail']}")
    # Print the author's affiliation
    print(f"Affiliation: {info['author']['affiliation']}")
    # Print the author's email
    print(f"Email: {info['author']['email']}")
    # Print the author's website
    print(f"Website: {info['author']['website']}")
    # Print the author's interests
    print("Interests:")
    for i in info['author']['interests']:
        print(' - ' + i['title'])
