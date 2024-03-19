import logging
from logging import NullHandler
from typing import Callable, Tuple, Dict, Any, Union

from .scholar_retriever import ScholarWebRetriever, PaginateBase
from . import profile_parser as pp
from .utils.tools import UrlUtilities
logger = logging.getLogger( __name__ )
logger.setLevel(logging.INFO)
logger.addHandler(NullHandler())

class ProfileSearch(ScholarWebRetriever, PaginateBase):
    """A class for searching profiles on Google Scholar.

    This class inherits from ScholarWebRetriever and PaginateBase classes.

    .. attribute:: URL_ENDPOINT (str): 
        The URL endpoint for profile search.
    """
    
    URL_ENDPOINT = "https://scholar.google.es/citations"
    
    def __init__(self, get_request_params: Callable[[], dict] = None) -> None:
        """
        Initialize the ProfileSearch object.

        :param get_request_params: A callable that returns parameters for the GET request. Defaults to None.
        :type get_request_params: Callable, optional
        """
        ScholarWebRetriever.__init__(self, get_request_params)
        PaginateBase.__init__(self, )
        
        self._view_op = ""
        # params
        self._after_author = None
        self._before_author = None

        self._results = {}

    def search_by_link(self, link: str) -> Tuple[bool, str]:
        """
        Search for profiles by link.

        This method verifies that it's a profile search, extracts the GET parameters from the link,
        uses set_params and load_params, and starts navigation.

        :param link: The link to search by.
        :type link: str
        """
        self.params = {}
        params = UrlUtilities.url_extract_get_params( link )
        
        if 'view_op' not in params:
            return (False, 'Invalid link: missing view_op parameter')
        
        if params['view_op'][0] != 'search_authors':
            return (False, 'Invalid link: incorrect view_op parameter')
        
        self.add_params(view_op="search_authors")

        if 'hl' in params:
            self.language = params['hl'][0]
        else :
            self.language = self.HL_DEFAULT
        
        if 'mauthors' in params:
            self.add_params(mauthors=params['mauthors'][0])
        else:
            return (False, 'Invalid link: missing mauthors parameter')
            
        self._results = {}
        
        return self._reload_page()

    def search_by_organization(self, org_id: str, hl: str = ScholarWebRetriever.HL_DEFAULT) -> Tuple[bool, str]:
        """
        Search for profiles by organization.

        :param org_id: The organization ID to search by.
        :type org_id: str
        :param hl: The language for the search. Defaults to ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :return: A tuple indicating success (``True``) or failure (``False``) along with an error message.
        :rtype: tuple[bool, str]
        """

        self.params = {} # clear params
        self.add_params(org=org_id)
        self.add_params(view_op='view_org')
        self.add_params(hl=hl)
        self._results = {}
        
        return self._reload_page()

    def search_by_author(
        self, author: str = "", label: str = "", hl: str = ScholarWebRetriever.HL_DEFAULT
    ) -> Tuple[bool,str]:
        """
        Search for profiles by author.

        :param author: The author's name to search by. Defaults to "".
        :type author: str, optional
        :param label: The label to search by. Defaults to "".
        :type label: str, optional
        :param hl: The language for the search. Defaults to ScholarWebRetriever.HL_DEFAULT.
        :type hl: str, optional
        :return: A tuple indicating success (``True``) or failure (``False``) along with an error message.
        :rtype: tuple[bool,str]
        """
        
        mauthors = author
        if label != "":
            mauthors += f" label:{label}"

        if mauthors == "":
            logging.info("Invalid args: author or label must be provided")
            return (False, "Invalid args: author or label must be provided")
        
        self.params = {} # clear params
        self.add_params(view_op="search_authors")
        self.add_params(mauthors=mauthors, hl=hl)
        
        if self._after_author is not None:
            self.add_params(after_author=self._after_author)

        if self._before_author is not None:
            self.add_params(before_author=self._before_author)

        self._results = {}
        
        return self._reload_page()

    def _reload_page(self, retry: int = 3) -> Tuple[bool, str]:
        """
        Reload the search page.

        :param retry: The number of retries if the request fails initially. Defaults to 3.
        :type retry: int, optional
        :return: A tuple indicating success (``True``) or failure (``False``) along with an error message.
        :rtype: tuple[bool, str]
        """
        
        if self._update_pagination():
            self.add_params(
                after_author = self._after_author,
                before_author = self._before_author)
        
        success, error = self.reload_web_content()
        
        if success:
            self._results = pp.profiles_search_parser( self.html )
            return True, 'Success'

        return False, error

    def get_json(self) -> Dict[str, Any]:
        """
        Get the search results as a JSON object.

        :return: The search results.
        :rtype: dict
        """
        return self._results

    def _update_pagination(self) -> bool:
        """
        Update pagination parameters.

        :return: ``True`` if pagination is updated, ``False`` otherwise.
        :rtype: bool
        """
        
        if "pagination" not in self._results:
            return False
        
        if "next_page_token" in self._results["pagination"]:
            self._after_author = self._results["pagination"]["next_page_token"]
        else:
            self._after_author = None

        if "prev_page_token" in self._results["pagination"]:
            self._before_author = self._results["pagination"]["prev_page_token"]
        else:
            self._before_author = None

    def next_page(self) -> Tuple[bool,str]:
        """
        Navigate to the next page of results.

        :return: A tuple indicating success (``True``) or failure (``False``) along with an error message.
        :rtype: tuple[bool,str]
        """
        
        self._update_pagination()
        if self._after_author is None:
            return False, 'Last page'
        
        self.add_params(
            after_author = self._after_author,
            before_author = self._before_author)

        return self._reload_page()

    def prev_page(self) -> Tuple[bool,str]:
        """
        Navigate to the previous page of results.

        :return: A tuple indicating success (True) or failure (False) along with an error message.
        :rtype: tuple[bool,str]
        """
        
        self._update_pagination()
        if self._before_author is None:
            return False, 'First page'
        
        self.add_params(
            after_author = None,
            before_author = self._before_author)

        return self._reload_page()

    @property
    def after_author(self) -> Union[str, None]:
        """
        Get the token for the next page of results.

        :return: The token for the next page of results.
        :rtype: str
        """
        return self._after_author
    
    @property
    def before_author(self) -> Union[str, None]:
        """
        Get the token for the previous page of results.

        :return: The token for the previous page of results.
        :rtype: str
        """
        return self._before_author
