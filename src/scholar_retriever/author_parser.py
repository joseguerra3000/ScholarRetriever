from bs4 import BeautifulSoup, Tag
from .utils.tools import UrlUtilities
from typing import List, Dict, Any

PROFILE_URL_BASE = 'https://scholar.google.com'

class ParserBase:
    def __init__(self, html: str = '') -> None:
        self._html = html
        self._soup = BeautifulSoup(self._html, 'html.parser')

    @property
    def html(self):
        return self._html
    
    @html.setter
    def html(self, new_html: str):
        self._html = new_html
        self._soup = BeautifulSoup(self._html,'html.parser')

    def parse(self):
        pass


class AuthorInfoParser(ParserBase):    
    def __init__(self, html: str = '') -> None:
        super().__init__(html)
    
    def parse_header_info(self) -> Dict[str, Any]:
        author_info = self._soup.find( 'div', id='gsc_prf' )

        if author_info is None:
            return {}
        
        try:
            thumbnail = author_info.find('img')['src']
            if not thumbnail.startswith('https'):
                thumbnail = PROFILE_URL_BASE + thumbnail
        except Exception:
            thumbnail = None
        
        try:
            name = author_info.find('div', id='gsc_prf_in').text
        except Exception:
            name = None
        
        info_lines : list[BeautifulSoup] = author_info.find_all('div', class_='gsc_prf_il')
        
        try:
            affiliation = info_lines[0].text
        except Exception:
            affiliation = None
        
        try:
            email = info_lines[1].text.split('-')[0]
        except Exception:
            email = None
            
        try:
            website = info_lines[1].find('a')['href']
        except Exception:
            website = None
        
        try:
            author_interests = info_lines[2].find_all('a', class_='gsc_prf_inta gs_ibl')
            interests = [ { 'title': i.text ,'link': 'https://scholar.google.es' + i['href']} for i in author_interests ]
        except Exception:
            interests = None
            
        return {
            'name': name,
            'thumbnail': thumbnail,
            'affiliation': affiliation,
            'email': email,
            'website': website,
            'interests': interests,
        }
    
    def parse_cited_by(self) -> Dict[str, Any]:
        cited_by = self._soup.find(id='gsc_rsb_cit')
        
        ####### Parse table #######
        table_bs = cited_by.find('table', id='gsc_rsb_st')

        t_row_titles: list[BeautifulSoup] = table_bs.find('thead').find_all('th')
        t_row_titles = [ t.text.replace(' ', '_').replace('-', '_').lower() for t in t_row_titles ]
        
        table_rows: list[BeautifulSoup] = table_bs.find('tbody').find_all( 'tr' )
        table = list()
        
        for tr in table_rows:
            columns: list[BeautifulSoup] = tr.find_all('td')
            columns = [ c.text.replace(' ', '_').replace('-', '_').lower() for c in columns ]
            table.append(
                {
                    columns[0]:{
                        t_row_titles[1]: columns[1],
                        t_row_titles[2]: columns[2],
                    }
                }
            )
        
        ####### Parse Graph #######
        
        graph_bs = self._soup.find('div', class_='gsc_md_hist_w')
        try:
            year_list = graph_bs.find_all('span', class_='gsc_g_t')
            year_list = [ y.text for y in year_list ]
            
            citation_list = graph_bs.find_all('a', class_='gsc_g_a')
            citation_list = [ c.text for c in citation_list ]
        
            graph = [ {"year":int(year), "citations":int(citations)} for year,citations in zip( year_list,citation_list ) ]
        except Exception:
            graph = []
            
        return {
            'table': table,
            'graph': graph,
            }

    def parse_public_access(self) -> Dict[str, Any]:
        access_bs = self._soup.find(id='gsc_rsb_mnd')
        
        try:
            link = 'https://scholar.google.com/' + access_bs.find('a')['href']
        except Exception:
            link = None
        
        try:
            available = access_bs.find('div', class_='gsc_rsb_m_a').text.split(' ')[0]
            not_available = access_bs.find('div', class_='gsc_rsb_m_na').text.split(' ')[0]
        except Exception:
            available = not_available = 0
            
        return {
            'link': link,
            'available': available,
            'not_available': not_available
        }
        
    def parse(self, html: str = None,) -> Dict[str, Any]:
        if html is not None:
            self.html = html
        
        author_info = self.parse_header_info()
        cited_by = self.parse_cited_by()
        public_access = self.parse_public_access()
        
        return {
            'author': author_info,
            'cited_by': cited_by,
            'public_access': public_access,
        }

    def parse_citations(self, html:str = None):
        pass
    
    def parse_all(self):
        return self.parse()


class CoAuthorsParser(ParserBase):
    
    def __init__(self, html: str = '') -> None:
        super().__init__(html)
    
    def _parse_coauthors(self) -> List[Dict[str, Any]]:
        
        coauthors_bs = self._soup.find('div', id='gsc_codb_content')
        
        coauthors_list = coauthors_bs.find_all('div', class_='gs_ai gs_scl')
        #print(len(coauthors_list))
        coauthors = list()
        
        for ca in coauthors_list:
            name = ca.find('h3', class_='gs_ai_name').text
            link = PROFILE_URL_BASE + ca.find('a')['href']
            author_id = UrlUtilities.url_extract_get_param( link, 'user' )
            affiliation = ca.find('div', class_='gs_ai_aff').text
            email = ca.find('div', class_='gs_ai_eml').text
            thumbnail = ca.find('img')['src']
            
            coauthors.append(
                {
                    'name': name,
                    'link': link,
                    'author_id' : author_id,
                    'affiliation': affiliation,
                    'email': email,
                    'thumbnail': thumbnail
                }
            )
            
        return coauthors

    def parse(self, html:str = None):
        if html is not None:
            self.html = html
        
        return self._parse_coauthors()



class AuthorArticlesParser(ParserBase):
    def __init__(self, html: str = '') -> None:
        super().__init__(html)
    
    def _parse_one_article( self, art: Tag ):
        
        #### gsc_a_t #####
        title = art.find('td', class_='gsc_a_t').find('a').text
        link = PROFILE_URL_BASE + art.find('td', class_='gsc_a_t').find('a')['href']
        citation_id = UrlUtilities.url_extract_get_param( link, 'citation_for_view' )
        
        gray = art.find_all('div', class_='gs_gray')
        authors = gray[0].text
        publication = gray[1].text
        
        #### cited_by ####
        cited_by = art.find('td', class_='gsc_a_c')
        try:
            cby_value = int(cited_by.find('a').text)
        except Exception:
            cby_value = 0
        cby_link = cited_by.find('a')['href']
        cites_id = UrlUtilities.url_extract_get_param(cby_link, 'cites')
        
        #### year ####
        year = art.find('td', class_='gsc_a_y').text
        
        return {
            'title': title,
            'link': link,
            'citation_id': citation_id,
            'authors': authors,
            'publication': publication,
            'cited_by': {
                'value': cby_value,
                'link': cby_link,
                'cites_id': cites_id,
            },
            'year': year
        }
        
    def _parse(self):
        articles_bs = self._soup.find('table', id='gsc_a_t')
        
        articles = articles_bs.find_all('tr', class_='gsc_a_tr')

        art_list = list()
        
        for art in articles:
            art_list.append( self._parse_one_article(art) )
        
        return art_list
    
    def parse(self):
        return self._parse()
    
    
if __name__ == '__main__': 

    import utils.html_test_author
    parser = AuthorInfoParser( html=utils.html_test_author.html_text )

    print(parser.parse_header_info())