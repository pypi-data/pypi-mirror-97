from .general import get_data
from ..utils import list_get

import json
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def permissions(response):
    text = re.search(r'"xdSrCf","(.*)\\n",null,null', response).group(1)

    try:
        data = json.loads(text.replace('\\n', '').replace('\\"', '"'))
    except (json.JSONDecodeError, TypeError):
        logging.error('Could not parse permissions.')
        return []

    results = []

    # Must double loop because when an app has "Other" permissions, it appears
    # in the second element in data.
    for _data in data:
        for d in _data:
            results.append({
                'access': list_get(d, [0]),
                'icon': list_get(d, [1, 3, 2]),
                'details': [
                    list_get(detail, [1])
                    for detail in list_get(d, [2], [])
                ]
            })
       
    return results