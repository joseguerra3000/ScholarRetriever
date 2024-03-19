.. _`Advanced use`:

###############
Advanced Topics
###############


- Performing proxy and agent rotation, delay between requests, etc.
- Advanced use of :mod:`scholar_retriever.profile_search` module
  
  - How get org_id
  - Pagination
  - Estructura de los datos devueltos

- Advanced use of :mod:`scholar_retriever.author_retriever` module
  
  - How get author_id: ProfileSearch, url
  - Estructura de los datos devueltos por cada clase


Getting profile information
===========================


ScholarRetriever has three classes for obtaining profile information:

- :class:`~scholar_retriever.author_retriever.AuthorInfoRetriever`: To obtain basic information about profiles.
  
  .. image:: /_static/AuthorInfoRetriever.svg

- :class:`~scholar_retriever.author_retriever.CoAuthorsRetriever`: To obtain the list of co-authors of the author.

  .. image:: /_static/CoAuthorsRetriever.svg
  
- :class:`~scholar_retriever.author_retriever.AuthorArticlesRetriever`: To obtain a list of the author's publications.

  .. image:: /_static/AuthorArticlesRetriever.svg

