from . import details
from .general import TIMEOUT
from .. import forms
from .. import headers
from .. import parsers
from .. import validators

import logging
import requests
import requests.exceptions
import time


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


SORT_TYPE = {
    'most_relevant': None,
    'newest': 2,
    'rating': 3
}


def reviews(
    app_id, 
    token=None, 
    pagination_delay=1, 
    review_size=100, 
    sort_by='most_relevant', 
    rating=0, 
    lang='en'):
    """Generator, gets all reviews.

    Parameters
    ----------
    app_id : str
        App id/Package name.
    token : str | None
        For continuation of reviews, you must provide this token.
    pagination_delay : int | float
        Time between each scrape.
    review_size : int
        Reviews by page, except page 1.
    sort_by : str
        Sorting option, available 'most_relevant', 'newest', 'rating'.
    rating : int
        Shows reviews by rating. Zero (0) means all ratings. 
    lang : str
        Language of reviews.
    
    Yields
    ------
    list of dict

    Raises
    ------
    TypeError | ValueError
    
    """
    validators.reviews(
        app_id, token, pagination_delay, review_size, sort_by, 
        rating, lang
    )
    
    try:
        token = token or -1
        while token:
            # The only time we do a GET request to first page is
            # when sort_by and rating are default values.
            if token == -1 and not sort_by and not rating:
                response = details._do_get_details(app_id, lang)
                results, token = parsers.reviews_first_page(response.text)
            else:
                form_next_page = forms.reviews_next_page(
                    app_id, None if token == -1 else token, 
                    review_size, SORT_TYPE[sort_by], rating
                )
                response = _do_post_next_reviews(form_next_page, lang)
                results, token = parsers.reviews_next_page(response.text)
            
            yield {
                'reviews': results,
                'next': {
                    'app_id': app_id,
                    'token': token,
                    'pagination_delay': pagination_delay,
                    'review_size': review_size,
                    'sort_by': sort_by,
                    'rating': rating,
                    'lang': lang,
                }
            }
            
            time.sleep(pagination_delay)
    except GeneratorExit:
        return
    except requests.exceptions.RequestException:
        logging.exception('Unexpected end.')
    except Exception:
        logging.exception('Unexpected end.')


def _do_post_next_reviews(form_next_page, lang):
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
    params = {
        'hl': lang
    }
    return requests.post(
        url, 
        params=params, 
        headers=headers.POST, 
        data=form_next_page,
        timeout=TIMEOUT
    )
