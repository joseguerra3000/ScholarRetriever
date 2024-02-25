==================
Scholar Retriever
==================

A Python package for efficiently extracting information from Google Scholar.

It's capable of extract:

* Profile results from the Google Scholar Profiles search page.

* Information from the Google Scholar Author page:

  * Name, Affiliations, Email, interests, thumbnail
  * Citations stats
  * Articles
  * Co-Authors

Installation
^^^^^^^^^^^^

You can install ScholarRetriever via pip:

.. code-block:: console

    pip install scholar_retriever


Usage Examples
^^^^^^^^^^^^^^

Retrieve results from the Google Scholar Profiles search page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    # Pending 


.. code-block:: text

    output

Retrieve basic information about an author
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

Retrieve articles from an author
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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


.. code-block:: text

    Articles ordered by # of citations
    ---------------------------------------
    404 Client Error: Not Found for url: https://scholar.google.com/citations?user=M4l534gAAAAJ&hl=en&pagesize=100&cstart=0&sortby=cited
    Details:
    Headers-req: {'headers': {'Accept': '*/*', 'Accept-Language': 'es', 'Host': '', 'User-Agent': 'ELinks/0.13.1 (textmode; Linux 5.4.0-169-generic x86_64; 80x24-2)'}}
    Headers-resp: {'Date': 'Sun, 25 Feb 2024 19:01:45 GMT', 'Content-Type': 'text/html', 'Server': 'HTTP server (unknown)', 'Content-Length': '49', 'X-XSS-Protection': '0', 'Alt-Svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000'}
    Citations by    Title
    2       Automatic Classification of Field Winding Faults in Synchronous Motors based on Bicoherence Image Segmentation and Higher Order Statistics of Stray Flux Signals
    2       Multifractal 1-D Wavelet Leader based on Spectral Kurtosis of Armature Currents for Sparking Detection in DC Motors
    1       Design of an Algorithm for Modeling Multiple Thermal Zones Using a Lumped-Parameter Model
    1       Bicoherence and Skewness-Kurtosis Analysis for the Detection of Field Winding Faults in Synchronous Motors using stray flux signals
    1       Variability of coil inductance measurements inside an interleaving structure
    0       Spectral Analysis of Anomalous Capacitance Measurements in Interleaving Structures: Study of Frequency Distribution in Photomultipliers
    0       Indoor Air Quality Analysis Using Recurrent Neural Networks: A Case Study of Environmental Variables
    0       Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables
    0       Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables
    0       Multifractal Spectrum and Complex Cepstrum Analysis of Armature Currents and Stray Flux Signals for Sparking Detection in DC Motors
    0       Spectral Entropy and Frequency Cepstral Coefficients of Stray Flux Signals for Sparking Detection in DC Motors
    0       Influence of the Flux Sensor Position for Rotor Fault Detection in WRIM: A Power Spectral Entropy Analysis

    Articles ordered by publication date
    ---------------------------------------
    Year    Title   Journal
    2023    Spectral Analysis of Anomalous Capacitance Measurements in Interleaving Structures: Study of Frequency Distribution in Photomultipliers        Symmetry 16 (1), 15, 2023
    2023    Indoor Air Quality Analysis Using Recurrent Neural Networks: A Case Study of Environmental Variables    Mathematics 11 (24), 4872, 2023
    2023    Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental VariablesPreprints, 2023
    2023    Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables
    2023    Multifractal Spectrum and Complex Cepstrum Analysis of Armature Currents and Stray Flux Signals for Sparking Detection in DC Motors    IEEE Transactions on Industry Applications, 2023
    2023    Spectral Entropy and Frequency Cepstral Coefficients of Stray Flux Signals for Sparking Detection in DC Motors2023 IEEE 14th International Symposium on Diagnostics for Electrical …, 2023
    2023    Influence of the Flux Sensor Position for Rotor Fault Detection in WRIM: A Power Spectral Entropy Analysis    2023 IEEE 32nd International Symposium on Industrial Electronics (ISIE), 1-6, 2023
    2023    Automatic Classification of Field Winding Faults in Synchronous Motors based on Bicoherence Image Segmentation and Higher Order Statistics of Stray Flux Signals       IEEE Transactions on Industry Applications, 2023
    2023    Design of an Algorithm for Modeling Multiple Thermal Zones Using a Lumped-Parameter Model       Energies 16 (5), 2247, 2023
    2022    Bicoherence and Skewness-Kurtosis Analysis for the Detection of Field Winding Faults in Synchronous Motors using stray flux signals    2022 IEEE Energy Conversion Congress and Exposition (ECCE), 1-5, 2022
    2022    Variability of coil inductance measurements inside an interleaving structure    Scientific Reports 12 (1), 16272, 2022
    2022    Multifractal 1-D Wavelet Leader based on Spectral Kurtosis of Armature Currents for Sparking Detection in DC Motors    2022 International Conference on Electrical Machines (ICEM), 1589-1594, 2022

    Articles ordered by title
    ---------------------------------------
    Year    Title   Journal
    2023    Automatic Classification of Field Winding Faults in Synchronous Motors based on Bicoherence Image Segmentation and Higher Order Statistics of Stray Flux Signals       IEEE Transactions on Industry Applications, 2023
    2022    Bicoherence and Skewness-Kurtosis Analysis for the Detection of Field Winding Faults in Synchronous Motors using stray flux signals    2022 IEEE Energy Conversion Congress and Exposition (ECCE), 1-5, 2022
    2023    Design of an Algorithm for Modeling Multiple Thermal Zones Using a Lumped-Parameter Model       Energies 16 (5), 2247, 2023
    2023    Indoor Air Quality Analysis Using Recurrent Neural Networks: A Case Study of Environmental Variables    Mathematics 11 (24), 4872, 2023
    2023    Influence of the Flux Sensor Position for Rotor Fault Detection in WRIM: A Power Spectral Entropy Analysis    2023 IEEE 32nd International Symposium on Industrial Electronics (ISIE), 1-6, 2023
    2022    Multifractal 1-D Wavelet Leader based on Spectral Kurtosis of Armature Currents for Sparking Detection in DC Motors    2022 International Conference on Electrical Machines (ICEM), 1589-1594, 2022
    2023    Multifractal Spectrum and Complex Cepstrum Analysis of Armature Currents and Stray Flux Signals for Sparking Detection in DC Motors    IEEE Transactions on Industry Applications, 2023
    2023    Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental VariablesPreprints, 2023
    2023    Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables
    2023    Spectral Analysis of Anomalous Capacitance Measurements in Interleaving Structures: Study of Frequency Distribution in Photomultipliers        Symmetry 16 (1), 15, 2023
    2023    Spectral Entropy and Frequency Cepstral Coefficients of Stray Flux Signals for Sparking Detection in DC Motors2023 IEEE 14th International Symposium on Diagnostics for Electrical …, 2023
    2022    Variability of coil inductance measurements inside an interleaving structure    Scientific Reports 12 (1), 16272, 2022
    JSON with all information:
    [
    {
        "title": "Automatic Classification of Field Winding Faults in Synchronous Motors based on Bicoherence Image Segmentation and Higher Order Statistics of Stray Flux Signals",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:9yKSN-GCB0IC",
        "citation_id": "M4l534gAAAAJ:9yKSN-GCB0IC",
        "authors": "ME Iglesias-Martínez, JG Carmenate, JAA Daviu, L Dunai, CA Platero, ...",
        "publication": "IEEE Transactions on Industry Applications, 2023",
        "cited_by": {
        "value": 2,
        "link": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=6680160498783872496",
        "cites_id": "6680160498783872496"
        },
        "year": "2023"
    },
    {
        "title": "Bicoherence and Skewness-Kurtosis Analysis for the Detection of Field Winding Faults in Synchronous Motors using stray flux signals",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:u5HHmVD_uO8C",
        "citation_id": "M4l534gAAAAJ:u5HHmVD_uO8C",
        "authors": "JG Carmenate, MEI Martínez, JA Antonino-Daviu, C Platero, ...",
        "publication": "2022 IEEE Energy Conversion Congress and Exposition (ECCE), 1-5, 2022",
        "cited_by": {
        "value": 1,
        "link": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=1111073863143960203",
        "cites_id": "1111073863143960203"
        },
        "year": "2022"
    },
    {
        "title": "Design of an Algorithm for Modeling Multiple Thermal Zones Using a Lumped-Parameter Model",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:u-x6o8ySG0sC",
        "citation_id": "M4l534gAAAAJ:u-x6o8ySG0sC",
        "authors": "P Fernández de Córdoba, FF Montes, MEI Martínez, JG Carmenate, ...",
        "publication": "Energies 16 (5), 2247, 2023",
        "cited_by": {
        "value": 1,
        "link": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=1154778110830399897",
        "cites_id": "1154778110830399897"
        },
        "year": "2023"
    },
    {
        "title": "Indoor Air Quality Analysis Using Recurrent Neural Networks: A Case Study of Environmental Variables",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:zYLM7Y9cAGgC",
        "citation_id": "M4l534gAAAAJ:zYLM7Y9cAGgC",
        "authors": "CA Reyes Pérez, ME Iglesias Martínez, J Guerra-Carmenate, ...",
        "publication": "Mathematics 11 (24), 4872, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Influence of the Flux Sensor Position for Rotor Fault Detection in WRIM: A Power Spectral Entropy Analysis",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:IjCSPb-OGe4C",
        "citation_id": "M4l534gAAAAJ:IjCSPb-OGe4C",
        "authors": "JG Carmenate, MEI Martínez, JA Antonino-Daviu, PF de Cordoba, ...",
        "publication": "2023 IEEE 32nd International Symposium on Industrial Electronics (ISIE), 1-6, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Multifractal 1-D Wavelet Leader based on Spectral Kurtosis of Armature Currents for Sparking Detection in DC Motors",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:2osOgNQ5qMEC",
        "citation_id": "M4l534gAAAAJ:2osOgNQ5qMEC",
        "authors": "ME Iglesias-Martínez, PM Velasco-Pla, J Antonino-Daviu, JG Carmenate, ...",
        "publication": "2022 International Conference on Electrical Machines (ICEM), 1589-1594, 2022",
        "cited_by": {
        "value": 2,
        "link": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=7117494277430465248",
        "cites_id": "7117494277430465248"
        },
        "year": "2022"
    },
    {
        "title": "Multifractal Spectrum and Complex Cepstrum Analysis of Armature Currents and Stray Flux Signals for Sparking Detection in DC Motors",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:UeHWp8X0CEIC",
        "citation_id": "M4l534gAAAAJ:UeHWp8X0CEIC",
        "authors": "JG Carmenate, ME Iglesias-Martínez, PM Velasco-Pla, JAA Daviu, ...",
        "publication": "IEEE Transactions on Industry Applications, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:Y0pCki6q_DkC",
        "citation_id": "M4l534gAAAAJ:Y0pCki6q_DkC",
        "authors": "CAR Pérez, MEI Martínez, JG Carmenate, HM Álvarez, E Balvis, ...",
        "publication": "Preprints, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Real-Time Indoor Air Quality Analysis using Recurrent Neural Networks: A Case Study of Environmental Variables",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:Tyk-4Ss8FVUC",
        "citation_id": "M4l534gAAAAJ:Tyk-4Ss8FVUC",
        "authors": "RP CA, IM ME, JG Carmenate, E Balvis, P Fernández de Cordoba",
        "publication": "",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Spectral Analysis of Anomalous Capacitance Measurements in Interleaving Structures: Study of Frequency Distribution in Photomultipliers",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:qjMakFHDy7sC",
        "citation_id": "M4l534gAAAAJ:qjMakFHDy7sC",
        "authors": "V Milián-Sánchez, ME Iglesias-Martínez, JG Carmenate, ...",
        "publication": "Symmetry 16 (1), 15, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Spectral Entropy and Frequency Cepstral Coefficients of Stray Flux Signals for Sparking Detection in DC Motors",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:d1gkVwhDpl0C",
        "citation_id": "M4l534gAAAAJ:d1gkVwhDpl0C",
        "authors": "MEI Martínez, JG Carmenate, JA Antonino-Daviu, L Dunai, ...",
        "publication": "2023 IEEE 14th International Symposium on Diagnostics for Electrical …, 2023",
        "cited_by": {
        "value": 0,
        "link": "",
        "cites_id": null
        },
        "year": "2023"
    },
    {
        "title": "Variability of coil inductance measurements inside an interleaving structure",
        "link": "https://scholar.google.com/citations?view_op=view_citation&hl=en&user=M4l534gAAAAJ&pagesize=100&sortby=title&citation_for_view=M4l534gAAAAJ:W7OEmFMy1HYC",
        "citation_id": "M4l534gAAAAJ:W7OEmFMy1HYC",
        "authors": "A Mocholí, F Mocholí, V Milián-Sánchez, J Guerra-Carmenate, ...",
        "publication": "Scientific Reports 12 (1), 16272, 2022",
        "cited_by": {
        "value": 1,
        "link": "https://scholar.google.com/scholar?oi=bibs&hl=en&cites=17692101323543048359",
        "cites_id": "17692101323543048359"
        },
        "year": "2022"
    }
    ]    

Retrieve Co-authors from an author
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import json

    # Import the CoAuthorsRetriever class from the scholar_retriever module
    from scholar_retriever import CoAuthorsRetriever

    # Identifier of the author for whom co-authors' information is desired
    author_identifier = 'M4l534gAAAAJ'

    # Create an instance of CoAuthorsRetriever with the author identifier and language 'en' (English)
    coauthor_retriever = CoAuthorsRetriever(author_identifier, 'en')

    # Attempt to retrieve information about the co-authors of the author
    success, reason = coauthor_retriever.fetch()

    # Check if the retrieval was successful
    if not success:
        # Print the error if the retrieval was unsuccessful
        print(f'Error:{reason}')
    else:
        # Get the co-authors' information
        info = coauthor_retriever.get_json()
        
        # Print the co-authors' information in JSON format with formatting and without escaping non-ASCII characters
        print(json.dumps(info, indent=2, ensure_ascii=False))


.. code-block:: text

    [
    {
        "name": "Pedro Fernandez de Cordoba",
        "link": "https://scholar.google.com/citations?hl=en&user=i3gYBKIAAAAJ",
        "author_id": "i3gYBKIAAAAJ",
        "affiliation": "Professor of Applied Mathematics, Universitat Politècnica de València",
        "email": "Verified email at mat.upv.es",
        "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=small_photo&user=i3gYBKIAAAAJ&citpid=1"
    },
    {
        "name": "JOSE ANTONINO-DAVIU",
        "link": "https://scholar.google.com/citations?hl=en&user=eZoyHuMAAAAJ",
        "author_id": "eZoyHuMAAAAJ",
        "affiliation": "UNIVERSITAT POLITECNICA DE VALENCIA",
        "email": "Verified email at die.upv.es",
        "thumbnail": "https://scholar.googleusercontent.com/citations?view_op=small_photo&user=eZoyHuMAAAAJ&citpid=2"
    },
    {
        "name": "Eduardo Balvís",
        "link": "https://scholar.google.com/citations?hl=en&user=HAyKsnsAAAAJ",
        "author_id": "HAyKsnsAAAAJ",
        "affiliation": "Universidad de Vigo",
        "email": "Verified email at uvigo.es",
        "thumbnail": "/citations/images/avatar_scholar_56.png"
    }
    ]

Documentation
^^^^^^^^^^^^^

For detailed documentation and examples, please refer to the official documentation.

License
^^^^^^^

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.
