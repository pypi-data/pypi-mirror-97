"""All functions functions must be common in all files in this folder."""
import json
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)


def html_script(text):
    regex = re.compile(r"key:\s*'ds:\d+',\s*isError:\s*false\s*,\s*hash:\s*'\d+',\s*data:")
    found = regex.search(text)
    if found is None:
        logging.error('1. Content inside <script> tag element has changed.')
        return []

    init = found.end()

    regex = re.compile(r",\s*sideChannel:\s*\{\}\}\);")
    found = regex.search(text)
    if found is None:
        logging.error('2. Content inside <script> tag element has changed.')
        return []

    end = found.start() - 1

    try:
        return json.loads(text[init:end])
    except json.JSONDecodeError:
        logging.error('Body content could not be parsed to dict.')
        return []


def get_ds(id, text):
	return re.findall(r"'(ds:\d+)' : {id:'" + id + "'", text)[-1]


def get_data(id, text, soup):
    try:
        ds = get_ds(id, text)
    except IndexError:
        logging.error(f'Not found {id}.')
        return []

    text = None   
    for script in soup.find_all('script'):
        if ds in script.decode_contents():
            text = script.decode_contents()

    if text is None:
        logging.error(f'Not found {ds} as a key in any script tag.')
        return []

    return html_script(text)