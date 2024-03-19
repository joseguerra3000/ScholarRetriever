'''Use of :class:`~scholar_retriever.ProfileSearch` class.

This code performs a search for profiles using the provided link on 
Google Scholar using the :class:`~scholar_retriever.ProfileSearch` class. 
It retrieves the results from the first page and prints relevant 
information for each profile.

Usage:
------

    1. Ensure you have the scholar_retriever module installed.
    2. Modify the constant `LINK` with the desired url.
    3. Run the script.

Example usage:
--------------

	python profile_search_link.py
'''

from scholar_retriever import ProfileSearch

LINK = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=upv+label%3Apython&btnG='

# Create an instance of ProfileSearch
p_search = ProfileSearch()

# Perform a search by link
success, reason = p_search.search_by_link(LINK)

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

