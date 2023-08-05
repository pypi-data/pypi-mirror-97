from datetime import datetime
from .general import get_data
from ..utils import list_get

import json
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def review_history(response):
    text = re.search(r'"UsvDTd","(.*)\\n",null,null', response).group(1)

    try:
        data = json.loads(text.replace('\\n', '').replace('\\"', '"'))
    except (json.JSONDecodeError, TypeError):
        logging.error('Could not parse review_history.')
        return [] 

    results = []

    for d in data[0]:
        history = {}

        history['id'] = list_get(d, [0])
        history['name'] = list_get(d, [1, 0])
        history['profile_pic'] = list_get(d, [9, 3, 0, 3, 2])
        history['background_pic'] = list_get(d, [9, 4, 3, 2])
        history['rating'] = list_get(d, [2])
        history['comment'] = list_get(d, [4])
        history['epoch'] = list_get(d, [5, 0])

        _datetime = datetime.fromtimestamp(history['epoch'])
        history['datetime'] = _datetime.strftime('%Y-%m-%d %H:%M:%S')
        history['app_version'] = list_get(d, [10])

        results.append(history)

    return results