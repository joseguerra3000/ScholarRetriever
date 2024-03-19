'''Use of :class:`~scholar_retriever.ProfileSearch` class.

This code performs a search for profiles associated with the 
Organization ID: '13086801797746034500' using the 
:class:`~scholar_retriever.ProfileSearch` class.

Usage:
------

    1. Ensure you have the scholar_retriever module installed.
    2. Modify the constant `ORGANIZATION_ID` with the desired ID.
    3. Run the script.

Example usage:
--------------

python profile_search_org.py

'''


from scholar_retriever import ProfileSearch

# Universitat Politècnica de València
ORGANIZATION_ID = '13086801797746034500'  

# Create an instance of ProfileSearch
p_search = ProfileSearch()

# Perform a search by organization ID
success, reason = p_search.search_by_organization(ORGANIZATION_ID)

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
