###############
Getting Started
###############

This section will guide you through the process of getting started with the package. 
Follow these steps to quickly set up ScholarRetriever and begin extracting valuable 
information from Google Scholar

************************
Install ScholarRetriever
************************

First install ScholarRetriever as explained in the :ref:`Installation Guide`.

***********************************
Retrieving data from Google Scholar
***********************************

ScholarRetriever has two main modules:

- :mod:`~scholar_retriever.profile_search`: Allow you to retrieve profile results from 
  the `Google Scholar Profiles search page <https://scholar.google.com/citations?hl=es&view_op=search_authors>`_.

- :mod:`~scholar_retriever.author_retriever`: Para obtener la información sobre algún perfil en particular.

Profile Searches on Google Scholar
==================================

To obtain results from the profile search page, the 
:class:`~scholar_retriever.ProfileSearch` class is used. 
This class allows for three types of searches:

- Author info and/or tag-based search.
- Institution-based search (companies, universities, etc.).
- Search based on a link.

Examples for each of these modes are shown below.

Search by author information and/or labels
------------------------------------------

This example uses the :class:`~scholar_retriever.ProfileSearch` class to 
perform a profile search on Google Scholar and then prints relevant 
information for each profile found on the first page of results.

.. literalinclude:: ../../src/examples/profile_api/profile_search_basic.py
    :lines: 20-

Output: 

.. code-block:: text

  name: José Afonso Guerra-Assunção
  author_id: utb31TgAAAAJ
  link: https://scholar.google.com/citations?hl=en&user=utb31TgAAAAJ
  affiliations: Erasmus MC, Rotterdam, Netherlands
  email: Verified email at erasmusmc.nl
  cited by: 11210
  ------------------
  name: Antonio Jose Teixeira Guerra
  author_id: 9UZHs4IAAAAJ
  link: https://scholar.google.com/citations?hl=en&user=9UZHs4IAAAAJ
  affiliations: Professor Titular do Departamento de Geografia da UFRJ
  email: Verified email at igeo.ufrj.br
  cited by: 9384
  ------------------
  ...
  ...
  ...

Search by institution
---------------------

This code performs a search for profiles associated with the Universitat 
Politècnica de València (Organization ID: '13086801797746034500') using the 
:class:`~scholar_retriever.ProfileSearch` class from the ScholarRetriever package. 
It retrieves the results from the first page and prints relevant information for 
each profile.

.. literalinclude:: ../../src/examples/profile_api/profile_search_org.py
  :lines: 20-

Output:

.. code-block::

  name: AVELINO CORMA CANOS
  author_id: l9wNywsAAAAJ
  link: https://scholar.google.com/citations?hl=en&user=l9wNywsAAAAJ
  affiliations: Instituto de Tecnología Química, Universitat Politècnica de València-Consejo Superior de
  email: Verified email at itq.upv.es
  cited by: 186751
  ------------------
  name: Hermenegildo Garcia
  author_id: yfvjUr8AAAAJ
  link: https://scholar.google.com/citations?hl=en&user=yfvjUr8AAAAJ
  affiliations: Universitat Politecnica de Valencia
  email: Verified email at qim.upv.es
  cited by: 74899
  ------------------
  name: Ramón Martínez Mánez
  author_id: OGe_vZcAAAAJ
  link: https://scholar.google.com/citations?hl=en&user=OGe_vZcAAAAJ
  affiliations: Universidad Politécnica de Valencia
  ...
  ...
  ...

.. note:: 
  The method for obtain the ``ORGANIZATION_ID`` of an Institution is shown in the :ref:`Advanced use` section.


Search by link
--------------

This example performs a search for profiles using the provided link on 
Google Scholar using the :class:`~scholar_retriever.ProfileSearch` class 
from the ScholarRetriever package. It retrieves the results from the 
first page and prints relevant information for each profile.


.. literalinclude:: ../../src/examples/profile_api/profile_search_link.py
  :lines: 20-


Getting profile information
===========================


ScholarRetriever has three classes for obtaining profile information:

- :class:`~scholar_retriever.author_retriever.AuthorInfoRetriever`: To obtain basic information about profiles.
- :class:`~scholar_retriever.author_retriever.CoAuthorsRetriever`: To obtain the list of co-authors of the author.
- :class:`~scholar_retriever.author_retriever.AuthorArticlesRetriever`: To obtain a list of the author's publications.

.. note:: 
  In all cases, it is necessary to know the URL of the profile or its ``author_id``.
  Several methods for obtaining the ``author_id`` of a profile are shown in the :ref:`Advanced use` section.


Basic usage
--------------------------------------------------------------
Code:

.. literalinclude:: ../../src/examples/author_api/retrieve_author_all.py
    :lines: 20-

Output: 

.. code-block:: text

    Author Info:
    ------------
    Name: Pedro Ferreira da Silva
    Thumbnail: https://scholar.googleusercontent.com/citations?view_op=medium_photo&user=X_M530AAAAAJ&citpid=2
    Affiliation: Experimental Research Physicist CERN
    Email: Verified email at cern.ch
    Website: None
    Interests:
    - High energy physics


.. note:: Ver :ref:`advanced use` para mas detalles sobre la estructura de los datos devueltos por :class:`~scholar_retriever.AuthorInfoRetriever`.
