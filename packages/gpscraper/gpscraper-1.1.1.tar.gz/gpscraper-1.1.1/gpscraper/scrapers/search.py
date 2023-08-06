from .general import TIMEOUT
from .. import forms
from .. import headers
from .. import parsers
from .. import validators

import logging
import requests
import time


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def search(
    query, 
    token=None,
    unknown_1=None,
    pagination_delay=1, 
    lang='en'):
    """List every content according on the query.

    Parameters
    ----------
    query : str
        Search query.
    token : str
        For continuation of search, you must provide this token.
    unknown_1 : str
        For continuation of search, you must provide this unknown_1.
    pagination_delay : int | float
        Time between each scrape.
    lang : str
        Language of results.
    
    Yields
    ------
    list of dict

    Raises
    ------
    TypeError | ValueError
    
    """
    validators.search(query, token, unknown_1, pagination_delay, lang)

    try:
        token = token or -1
        while token:
            if token == -1:
                response = _do_get_search(query, lang)
                results, token, unknown_1 =  parsers.search_first_page(
                    response.text
                )
            else:
                form_next_page = forms.search_next_page(token, unknown_1)
                response = _do_post_next_search(form_next_page, lang)
                results, token = parsers.search_next_page(
                    response.text
                )

            yield {
                'search': results,
                'next': {
                    'query': query,
                    'token': token,
                    'unknown_1': unknown_1,
                    'pagination_delay': pagination_delay,
                    'lang': lang,
                }
            }

            time.sleep(pagination_delay)

    except requests.exceptions.RequestException:
        logging.exception('Unexpected end.')
    except Exception:
        logging.exception('Unexpected end.')


def _do_get_search(query, lang):
    url = 'https://play.google.com/store/search'
    params = {
        'q': query, 
        'hl': lang, 
        'gl': 'US'
    }
    return requests.get(
        url, 
        params=params, 
        headers=headers.GET, 
        timeout=TIMEOUT
    )


def _do_post_next_search(form_next_page, lang):
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
    params = {
        'hl': lang, 
        'gl': 'US'
    }
    return requests.post(
        url, 
        params=params, 
        headers=headers.POST, 
        data=form_next_page,
        timeout=TIMEOUT
    )
