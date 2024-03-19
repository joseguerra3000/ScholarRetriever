""" Use of :class:`~scholar_retriever.ProfileSearch` class.

This code uses the :class:`~scholar_retriever.ProfileSearch` class to 
perform a profile search on Google Scholar and then prints relevant 
information for each profile found on the first page of results.

Usage:
------

    1. Ensure you have the scholar_retriever module installed.
    2. Modify the constant `SEARCH_TERM` with the desired term.
    3. Run the script.

Example usage:
--------------

python profile_search_basic.py

"""

from scholar_retriever import ProfileSearch

SEARCH_TERM = 'Jose Guerra'

# Create an instance of ProfileSearch
p_search = ProfileSearch()

# Perform a search by author name
success, reason = p_search.search_by_author(SEARCH_TERM)

# Check if the search was successful
if not success:
    # Print the error message and exit if the search failed
    print(f'Error: {reason}')
    exit()

# Get the results from the first page
results = p_search.get_json()

# Iterate through the results and print relevant information for each profile
for p in results['profiles']:
    print(f"name: {p['name']}")
    print(f"author_id: {p['author_id']}")
    print(f"link: {p['link']}")
    print(f"affiliations: {p['affiliations']}")
    print(f"email: {p['email']}")
    print(f"cited by: {p['cited_by']}")
    print("------------------")
