"""ScholarRetriever is a Python module designed to interact with Google Scholar in a manner akin to an API.

    ScholarRetriever provides a convenient and effective means of accessing the
    rich information available on Google Scholar, equipping users with the 
    necessary tools to explore and leverage the extensive academic database 
    offered by this platform.
"""

from .profile_search import ProfileSearch
from .author_retriever import (
    AuthorInfoRetriever,
    CoAuthorsRetriever,
    AuthorArticlesRetriever,
    ArticlesOrder,
)


VERSION = "0.1.0"

__version__ = VERSION

__all__ = [
    "ProfileSearch",
    "AuthorInfoRetriever",
    "AuthorArticlesRetriever",
    "CoAuthorsRetriever",
    "ArticlesOrder",
]
