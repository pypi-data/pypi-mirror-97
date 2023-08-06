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


def permissions(app_id, lang='en'):
    """Shows app permissions (access) for all versions.

    Parameters
    ----------
    app_id : str
        App id/Package name.
    lang : str
        Language to be shown.

    Returns
    -------
    list of dict

    Raises
    ------
    TypeError | ValueError
    """
    validators.permissions(app_id, lang)
    try:
        form = forms.permissions(app_id)
        response = _do_post_permissions(form, lang)
        return parsers.permissions(response.text)
    except requests.exceptions.RequestException:
        logging.exception('Unexpected end.')
    except Exception:
        logging.exception('Unexpected end.')


def _do_post_permissions(form, lang):
    url = 'https://play.google.com/_/PlayStoreUi/data/batchexecute'
    params = {'hl': lang, 'gl': 'US'}

    return requests.post(
        url, params=params, headers=headers.POST, data=form, timeout=TIMEOUT
    )