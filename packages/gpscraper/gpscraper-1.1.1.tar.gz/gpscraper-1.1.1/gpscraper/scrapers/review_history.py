from .general import TIMEOUT
from .. import forms
from .. import headers
from .. import parsers
from .. import validators

import logging
import requests


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def review_history(app_id, review_id):
    """Gets a review history (all modifications).

    Parameters
    ----------
    app_id : str
        App id/Package name.
    review_id : int
        Review id, it is retrieve from reviews when you use the
        reviews method.
    
    Yields
    ------
    list of dict | None

    Raises
    ------
    TypeError | ValueError        
    """
    validators.review_history(app_id, review_id)
    try:
        form = forms.review_history(app_id, review_id)
        response = _do_get_review_history(form)
        return parsers.review_history(response.text)
    except:
        logging.exception('Unexpected error.')
        return None


def _do_get_review_history(form):
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
    
    return requests.post(url, headers=headers.POST, data=form, timeout=TIMEOUT)