from enum import Enum
from typing import Any, Callable, Dict, List, Tuple

from .scholar_retriever import ScholarWebRetriever
from .author_parser import AuthorInfoParser, CoAuthorsParser, AuthorArticlesParser

# Ejemplos para la lectura de publicaciones de un autor
# https://scholar.google.es/citations?hl=en&user=izlC3EEAAAAJ&cstart=1&pagesize=5


class AuthorBase(ScholarWebRetriever):
    """
    A base class for retrieving information about authors from Google Scholar.

    This class inherits from ScholarWebRetriever.
    """

    URL_ENDPOINT = "https://scholar.google.com/citations"
    """The URL endpoint for author information."""

    def __init__(
        self,
        author_id: str = None,
        hl: str = ScholarWebRetriever.HL_DEFAULT,
        get_request_params: Callable[[], dict] = None,
    ) -> None:
        """
        Initialize the AuthorBase object.

        :param author_id: The author's unique identifier. Defaults to None.
        :type author_id: str, optional
        :param hl: The language for the request. Defaults to ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :param get_request_params: A callable that returns parameters for the GET request. Defaults to None.
        :type get_request_params: Callable[[], dict], optional
        """

        super().__init__(get_request_params)

        self.author_id = author_id
        self.language = hl

    @property
    def author_id(self) -> str:
        """
        Get the author's unique identifier.

        :return: The author's unique identifier.
        :rtype: str
        """
        return self._author_id

    @author_id.setter
    def author_id(self, new_author_id: str) -> None:
        """
        Set the author's unique identifier and update the request parameters.

        :param new_author_id: The new author's unique identifier.
        :type new_author_id: str
        """
        self._author_id = new_author_id
        self.add_params(user=self._author_id)

    def fetch(self) -> Tuple[bool, str]:
        raise Exception(
            "This function must be implemented by classes that inherit from Paginate"
        )
    
    def get_json(self):
        raise Exception(
            "This function must be implemented by classes that inherit from Paginate"
        )


class AuthorInfoRetriever(AuthorBase):
    """
    A class for retrieving main information about authors from Google Scholar.

    This class inherits from AuthorBase.
    """

    def __init__(
        self,
        author_id: str = None,
        hl: str = ScholarWebRetriever.HL_DEFAULT,
        get_request_params: Callable[[], dict] = None,
    ) -> None:
        """
        Initialize the AuthorInfoRetriever object.

        :param author_id: The author's unique identifier. Defaults to None.
        :type author_id: str, optional
        :param hl: The language for the request. Defaults to ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :param get_request_params: A callable that returns parameters for the GET request. Defaults to None.
        :type get_request_params: Callable[[], dict], optional
        """

        super().__init__(get_request_params)

        self.language = hl
        self.author_id = author_id
        self._parser = AuthorInfoParser()
        self._result_author_info = {
            "author": None,
            "cited_by": None,
            "public_access": None,
        }

    def fetch_author_info(self) -> Tuple[bool, str]:
        """
        Fetch information about the author from Google Scholar in html format.

        :return: A tuple indicating success (``True``) or failure (``False``) along with a reason.
        :rtype: tuple[bool, str]
        """

        success, reason = self.reload_web_content()

        if not success:
            return (success, reason)

        self._result_author_info = self._parser.parse(self.html)

        return (True, "Success")

    def fetch(self) -> Tuple[bool, str]:
        """
        Fetch the author information.

        :return: A tuple indicating success (``True``) or failure (``False``) along with a reason.
        :rtype: tuple[bool, str]
        """
        success, reason = self.fetch_author_info()
        return success, reason

    def get_json(self) -> dict:
        """
        Get the author information as a JSON object.

        :return: The author information.
        :rtype: dict
        """
        ret = {}
        ret.update(self._result_author_info)
        return ret


class CoAuthorsRetriever(AuthorBase):
    """
    A class for retrieving information about co-authors from Google Scholar.

    This class inherits from AuthorBase.
    """

    def __init__(
        self,
        author_id: str = None,
        hl: str = ScholarWebRetriever.HL_DEFAULT,
        get_request_params: Callable[[], dict] = None,
    ) -> None:
        """
        Initialize the CoAuthorsRetriever object.

        :param author_id: The author's unique identifier. Defaults to None.
        :type author_id: str, optional
        :param hl: The language for the request. Defaults to ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :param get_request_params: A callable that returns parameters for the GET request. Defaults to None.
        :type get_request_params: Callable[[], dict], optional
        """

        super().__init__(author_id, hl, get_request_params)
        self.add_params(view_op="list_colleagues")
        self._parser = CoAuthorsParser()

    def fetch(self) -> Tuple[bool, str]:
        """
        Fetch information about co-authors.

        :return: A tuple indicating success (``True``) or failure (``False``) along with a reason.
        :rtype: tuple[bool, str]
        """
        success, reason = self.reload_web_content()

        if not success:
            return (success, reason)

        self._result_coauthor = self._parser.parse(self.html)

        return (True, "Success")

    def get_json(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the co-authors' information.

        :return: The co-authors' information.
        :rtype: List[Dict[str, Any]]
        """
        return {"coauthors": self._result_coauthor}


class ArticlesOrder(Enum):
    """
    An enumeration representing different ordering options for articles.

    Used by :class:`~scholar_retriever.AuthorArticlesRetriever` class.

    """

    CITED_BY = "cited"
    """Order articles by the number of citations."""

    TITLE = "title"
    """Order articles by title."""

    PUBLICATION_DATE = "pubdate"
    """Order articles by publication date."""


class AuthorArticlesRetriever(AuthorBase):
    """
    A class for retrieving articles of an author from Google Scholar.

    This class inherits from AuthorBase and provides methods for retrieving articles of an author,
    as well as for exporting the results to a CSV file.

    """

    def __init__(
        self,
        author_id: str,
        hl: str = ScholarWebRetriever.HL_DEFAULT,
        get_request_args: Callable[[], dict] = None,
    ) -> None:
        """
        Initialize the AuthorArticlesRetriever object.

        :param author_id: The unique identifier of the author.
        :type author_id: str
        :param hl: The language for the request. Default is the default language of ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :param get_request_args: A function that returns arguments for the GET request. Default is None.
        :type get_request_args: Callable[[], dict], optional
        """
        super().__init__(
            author_id=author_id, hl=hl, get_request_params=get_request_args
        )
        self.language = hl
        self.page_size = 100
        self.author_id = author_id

    @property
    def page_size(self) -> int:
        """
        Get the page size for the request.

        :return: The page size.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, new_page_size):
        """
        Set the page size and update the request parameters.

        :param new_page_size: The new page size.
        :type new_page_size: int
        """
        self._page_size = new_page_size
        self.add_params(pagesize=self._page_size)

    def fetch(self):
        return self.fetch_citations()

    def fetch_citations(
        self,
        sort_by: ArticlesOrder = ArticlesOrder.CITED_BY,
        start: int = 0,
        num: int = -1,
    ) -> Tuple[bool, str]:
        self._sort_by = sort_by.value  # check values
        self._start = start  # check values
        self._num = num  # check values
        self._results = list()
        cstart = self._start

        while num < 0 or len(self._results) < num:
            success, reason = self._fetch_page(cstart, self.page_size)
            if not success:
                return success, reason

            page = reason
            self._results.extend(page)

            if len(page) < self.page_size:
                break

            cstart += self.page_size

        if self._num > 0:
            self._results = self._results[0 : self._num]

        return True, "Success"

    def _fetch_page(self, start: int, pagesize: int) -> List[Dict[str, Any]]:
        """
        Retrieve a page of articles.

        :param start: The start index for article retrieval.
        :type start: int
        :param pagesize: The page size for the request.
        :type pagesize: int
        :return: A tuple indicating success (``True``) along with the List or articles or
            failure (``False``) along with a reason.
        A Tuple with a list of dictionaries representing the articles.
        :rtype: Tuple[ bool, Union[ List[Dict[str, Any]], str ]
        """

        self.add_params(cstart=start, pagesize=pagesize, sortby=self._sort_by)

        success, reason = self.reload_web_content()

        if not success:
            print(success, reason)
            return success, reason

        return True, AuthorArticlesParser(self.html).parse()

    def get_json(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the results as a JSON object.

        :return: The results in JSON format.
        :rtype: dict
        """
        return {"publications": self._results}

    def export_to_csv(self, file_path: str, reload: bool = False):
        """
        Export the results to a CSV file.

        :param file_path: The destination CSV file path.
        :type file_path: str
        :param reload: A boolean indicator to reload the results before exporting. Default is False.
        :type reload: bool, optional
        """
        with open(file_path, "w") as f:
            f.write(
                "title;link;citation_id;authors;publications;cited_by;year\n",
            )
            for art in self._results:
                f.write(
                    f"{art['title']};{art['link']};{art['citation_id']};{art['authors']};{art['publication']};{art['cited_by']['value']};{art['year']}\n"
                )


# class AuthorRetriever(AuthorInfoRetriever):
#    def export_to_excel(self, reload: bool = None):
#        pass
#
#    pass
