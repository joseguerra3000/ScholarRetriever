from bs4 import BeautifulSoup
import bs4
#from .constants import PROFILE_URL_BASE
from .utils import tools

PROFILE_URL_BASE = 'https://scholar.google.com'

def _single_profile_parser( profile: bs4.BeautifulSoup ):
	'''
	Scrape information from a profile section and return it as a dict.

	'''
	# get name
	author_name = profile.find( 'h3', class_='gs_ai_name' )

	# get link
	author_link = PROFILE_URL_BASE + author_name.find( 'a' )['href']

	# get author id
	author_id = tools.UrlUtilities.url_extract_get_param(author_link, 'user')

	# get affiliations
	author_aff = profile.find( 'div', class_='gs_ai_aff' ).text

	# email verified
	author_email = profile.find('div', class_='gs_ai_eml').text

	# cited by
	author_citedby = 0
	citedby = profile.find('div', class_='gs_ai_cby').text
	if citedby != '':
		try:
			author_citedby = int(citedby.split(' ')[-1])
		except Exception:
			author_citedby = 0

	# interests
	interests = profile.find( 'div', class_='gs_ai_int' )
	interests = interests.find_all( 'a', class_='gs_ai_one_int' )
	
	author_interests = [ { 'title': i.text ,'link': PROFILE_URL_BASE + i['href']} for i in interests ]

	thumbnail = profile.find( 'img', recursive=True )['src']

	if not thumbnail.startswith('http'):
		thumbnail = PROFILE_URL_BASE + thumbnail

	profile_json = {
		'name': author_name.text,
		'link': author_link,
		'author_id': author_id,
		'affiliations': author_aff,
		'email': author_email,
		'cited_by': author_citedby,
		'interests': author_interests,
		'thumbnail': thumbnail,
	}

	#print(json.dumps(profile_json, indent=2))
	return profile_json

def _profile_list_parse( web_html: bs4.BeautifulSoup ):
	'''
	Parse the list of profiles form one profile page on Google scholar 

	:return dict with information about profiles

	'''

	# get list of div containing profiles
	profiles = web_html.find_all( 'div', class_='gs_ai' )

	# analice every one profile
	profiles_ret = [ _single_profile_parser(p) for p in profiles ]
	return profiles_ret

def _pagination_data_parse( web_html: bs4.BeautifulSoup ):

	pagination = {}

	buttons = web_html.find( 'div', id='gsc_authors_bottom_pag', recursive=True )
	if buttons is None:
		return {}
	# prev link and token
	btn_prev = buttons.find('button', class_='gsc_pgn_ppr')

	if btn_prev.has_attr('onclick'):
		# get and clean url
		link = str(btn_prev['onclick']).replace( 'window.location=', '' )
		# remove extra single quotes 
		link = link[1:-2].replace( '\\x3d', '=' ).replace('\\x26', '&')

		pagination.update( {'prev':PROFILE_URL_BASE + link } )
		token = tools.UrlUtilities.url_extract_get_param( pagination['prev'], 'before_author' )
		if token is not None:
			pagination.update( {'prev_page_token': token} )

	# next link and token
	btn_next = buttons.find('button', class_='gsc_pgn_pnx')
	if btn_next.has_attr('onclick'):
		# get and clean url
		link =  btn_next.get('onclick').replace( 'window.location=', '' )
		# remove extra single quotes 
		link = link[1:-2].replace( '\\x3d', '=' ).replace('\\x26', '&')
		
		pagination.update( {'next': PROFILE_URL_BASE + link } )
		token = tools.UrlUtilities.url_extract_get_param( pagination['next'], 'after_author' )
		if token is not None:
			pagination.update( {'next_page_token': token} )

	return pagination

def profiles_search_parser( html: str ) -> list:
	'''
	Scrape info from a profile google scholar search page and return it
	as a dict.
	
	.. code::

		Dict structure:
		{
			'profiles': [
				...
			],
			'pagination' : {
				...
			}
		}

	'''

	soup = BeautifulSoup( html, 'html.parser' )

	# get profile list
	profiles_ret = _profile_list_parse( soup )

	# get pagination data	
	pagination = _pagination_data_parse(soup)

	ret = {
		'profiles': profiles_ret,
		'pagination' : pagination,
	}

	#print(json.dumps(ret, indent=2))
	return ret




if __name__ == '__main__': 

	from .utils import html_test

	profiles_search_parser( html=html_test.html_text )