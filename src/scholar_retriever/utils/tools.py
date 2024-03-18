from urllib.parse import parse_qs, urlparse
from typing import AnyStr, Dict,List

class UrlUtilities:

	@staticmethod
	def url_extract_get_params( url: str ) -> Dict[AnyStr, List[AnyStr]]:
		"""
		Returns all parameters of a GET request from the url
		"""
		return parse_qs( urlparse(url).query )

	@staticmethod
	def url_extract_get_param( url: str, param: str ):
		"""
		Returns a parameter of a GET request from the url
		"""
		p = UrlUtilities.url_extract_get_params(url).get(param)
		if p is not None:
			p = p[0]
		
		return p


class HttpHeadersTemplate(object):
	DEFAULT_TEMPLATES = [

		# Brave (Linux)
		{
			'Authority': 'scholar.google.com',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
			'Accept-language': 'es-ES,es;q=0.9',
			'Cache-control': 'max-age=0',
			'Sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
			'Sec-ch-ua-mobile': '?0',
			'Sec-ch-ua-model': '""',
			'Sec-ch-ua-platform': '"Linux"',
			'Sec-ch-ua-platform-version': '"5.4.0"',
			'Sec-fetch-dest': 'document',
			'Sec-fetch-mode': 'navigate',
			'Sec-fetch-site': 'none',
			'Sec-fetch-user': '?1',
			'Sec-gpc': '1',
			'Upgrade-insecure-requests': '1',
			'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		},

		# Firefox (Linux)
		{
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
			'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
			# 'Accept-Encoding': 'gzip, deflate, br',
			'DNT': '1',
			'Sec-GPC': '1',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'cross-site',

		},

		# Chromium (Linux)
		{
			'Authority': 'scholar.google.es',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'Accept-language': 'es-ES,es;q=0.9',
			'Cache-control': 'max-age=0',
			# 'cookie': 'NID=511=iSVH1TaeB1dpAg1masqSjJ1IqHCrsRGPfRy0fMwEXMmR4FrrX7GJmHIiKqzkuxqiFxCDFz0JnkgYHeOUWVwcCi3xrRzeuQ3n8Fd--iiC6f15ZzgG9-97psl7AGKMR709_HSz3xa7cqLjpOKg_bsfT69yHSHVKkl_ScKCsaR8gtE; GSP=LM=1705687999:S=a2gi1otFGMM9-dbB',
			'Sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
			'Sec-ch-ua-arch': '"x86"',
			'Sec-ch-ua-bitness': '"64"',
			'Sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.129"',
			'Sec-ch-ua-mobile': '?0',
			'Sec-ch-ua-model': '""',
			'Sec-ch-ua-platform': '"Linux"',
			'Sec-ch-ua-platform-version': '"5.4.0"',
			'Sec-ch-ua-wow64': '?0',
			'Sec-fetch-dest': 'document',
			'Sec-fetch-mode': 'navigate',
			'Sec-fetch-site': 'none',
			'Sec-fetch-user': '?1',
			'Upgrade-insecure-requests': '1',
			'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		},

		# Chrome (Linux)
		{
			'Authority': 'scholar.google.es',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'Accept-language': 'es-US,es;q=0.9',
			'Cache-control': 'max-age=0',
			'Sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
			'Sec-ch-ua-mobile': '?0',
			'Sec-ch-ua-platform': '"Linux"',
			'Sec-fetch-dest': 'document',
			'Sec-fetch-mode': 'navigate',
			'Sec-fetch-site': 'none',
			'Sec-fetch-user': '?1',
			'Upgrade-insecure-requests': '1',
			'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		},

		# elinks
		{
    		"Accept": "*/*", 
			"Accept-Language": "es", 
			"Host": "", 
			"User-Agent": "ELinks/0.13.1 (textmode; Linux 5.4.0-169-generic x86_64; 80x24-2)", 
		},

		# Edge
		{
			'Authority': 'scholar.google.com',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'Accept-language': 'es',
			'Cache-control': 'max-age=0',
			'Sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
			'Sec-ch-ua-arch': '"x86"',
			'Sec-ch-ua-bitness': '"64"',
			'Sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.234", "Microsoft Edge";v="120.0.2210.144"',
			'Sec-ch-ua-mobile': '?0',
			'Sec-ch-ua-model': '""',
			'Sec-ch-ua-platform': '"Linux"',
			'Sec-ch-ua-platform-version': '"5.4.0"',
			'Sec-ch-ua-wow64': '?0',
			'Sec-fetch-dest': 'document',
			'Sec-fetch-mode': 'navigate',
			'Sec-fetch-site': 'none',
			'Sec-fetch-user': '?1',
			'Upgrade-Insecure-Requests': '1',
    		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
		},
	]