''' Use of :class:`~scholar_retriever.ProfileSearch` class.

This script performs a profile search on Google Scholar and saves 
the results of multiple pages in a JSON file named 'pages.json'.

Usage:
------

    1. Ensure you have the scholar_retriever module installed.
    2. Modify the constants `SEARCH_TERM` and `LABEL` with the desired values.
    3. Run the script.

Example usage:
--------------

python profile_search_json.py


'''

from scholar_retriever import ProfileSearch
import json
import time

SEARCH_TERM = 'upv.es'
LABEL = 'iot'

NUM_OF_PAGES = 3

# Create an instance of ProfileSearch
p_search = ProfileSearch()

# Perform a search for all authors with verified email addresses at upv.es and labeled with IoT as interest
success, reason = p_search.search_by_author(SEARCH_TERM, LABEL)

# Check if the search was successful
if not success:
    # Print the error message and exit if the search failed
    print(f'Error: {reason}')
    exit()

# Open a file to store the results
with open('pages.json', 'w') as f_out:
    f_out.write('[\n')
    pages = 0
    while pages < NUM_OF_PAGES:
        
        # Add comma and newline if not the first page
        if pages > 0:
            f_out.write(',\n')
        
        # Write the current page of results to the file
        f_out.write(json.dumps(p_search.get_json(), indent=2, ensure_ascii=False))
        pages += 1
        
        # Move to the next page of results
        success, reason = p_search.next_page()
        if not success:
            # Print error message if unable to fetch the next page and exit the loop
            print('Failed:', reason)
            break

        # Add a delay to avoid being blocked by the server
        time.sleep(2)
        
    f_out.write(']\n')
