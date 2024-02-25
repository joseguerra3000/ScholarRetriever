
.. code-block:: python
    
    """ Use of :class:`AuthorArticlesRetriever` class.

    This script retrieves information about articles authored by a specific author from Google Scholar. 
    Show how to sort them based on different criteria such as the number of citations, publication date, and title.

    Usage:
    ------

        1. Ensure you have the scholar_retriever module installed.
        2. Modify the variable `author` with the identifier of the desired author.
        3. Run the script.

    Example usage:
    --------------

    python retrieve_author_articles.py
    """



    # Importing necessary modules
    from scholar_retriever import AuthorArticlesRetriever, ArticlesOrder
    import json

    # Defining the author identifier
    author = 'M4l534gAAAAJ'

    # Creating an instance of AuthorArticlesRetriever for the specified author
    articles_retriever = AuthorArticlesRetriever(author)

    # Function to retrieve article citations ordered by the specified criteria
    def get_citations(order: ArticlesOrder):
        # Attempting to fetch citations sorted by the specified order
        success, reason = articles_retriever.fetch_citations(sort_by=order)

        # Handling retrieval success or failure
        if not success:
            print(f'Error: {reason}')
        return articles_retriever.get_json()

    # Retrieving and printing articles ordered by number of citations
    print()
    print('Articles ordered by # of citations')
    print('---------------------------------------')
    art = get_citations(ArticlesOrder.CITED_BY)
    print("Citations by\tTitle")
    for a in art:
        print(f"{a['cited_by']['value']}\t{a['title']}")

    # Retrieving and printing articles ordered by publication date
    print()
    print('Articles ordered by publication date')
    print('---------------------------------------')
    art = get_citations(ArticlesOrder.PUBLICATION_DATE)
    print("Year\tTitle\tJournal")
    for a in art:
        print(f"{a['year']}\t{a['title']}\t{a['publication']}")

    # Retrieving and printing articles ordered by title
    print()
    print('Articles ordered by title')
    print('---------------------------------------')
    art = get_citations(ArticlesOrder.TITLE)
    print("Year\tTitle\tJournal")
    for a in art:
        print(f"{a['year']}\t{a['title']}\t{a['publication']}")

    # Printing JSON with all retrieved information
    print('JSON with all information:')
    print(json.dumps(art, indent=2, ensure_ascii=False))
