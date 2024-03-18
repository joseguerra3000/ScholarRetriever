"""Retrieve information about an author using various retrievers.

This script demonstrates the use of different retrievers from the scholar_retriever module
to obtain information about an author. It utilizes the :class:`~scholar_retriever.AuthorInfoRetriever`, 
:class:`~scholar_retriever.AuthorArticlesRetriever`and :class:`~scholar_retriever.CoAuthorsRetriever`

Usage:
------

    1. Ensure that you have the scholar_retriever package and its dependencies installed.
    2. Modify the variable `AUTHOR_IDENTIFIER` with the corresponding author identifier.
    3. Run the script.

Example usage:
--------------
python retrieve_author_all.py
"""

# Import necessary modules
import json
import scholar_retriever
from scholar_retriever import (
    AuthorInfoRetriever,
    AuthorArticlesRetriever,
    CoAuthorsRetriever,
)

# Identifier of the author for which information is desired
AUTHOR_IDENTIFIER = "M4l534gAAAAJ"

# Create instances of retrievers for author information, publications, and co-authors
author_info_retriever = AuthorInfoRetriever(AUTHOR_IDENTIFIER, "en")
author_pub_retriever = AuthorArticlesRetriever( author_id=AUTHOR_IDENTIFIER)
author_coauthor_retriever = CoAuthorsRetriever(AUTHOR_IDENTIFIER)

# Combine all retrievers into a list
author_retrievers: "list[scholar_retriever.author_retriever.AuthorBase]" = [
    author_info_retriever,
    author_pub_retriever,
    author_coauthor_retriever,
]

# Dictionary to store the combined output of all retrievers
output = {}

# Iterate through each retriever and fetch the information
for retriever in author_retrievers:
    success, reason = retriever.fetch()
    if not success:
        # Print error message if retrieval fails
        print(f"Error: {reason}")
    else:
        # Update the output dictionary with the retrieved information
        output.update(retriever.get_json())
        

# Write the combined output to a JSON file
with open('author.json', 'w') as f_out:
    f_out.write(json.dumps(output, ensure_ascii=False, indent=2))
