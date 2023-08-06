import json


def search_next_page(token, unknown_1):
    long_data = (
        f'[[null,[{unknown_1}],null,"{token}"]]'
    )

    form = {
        'f.req': [[[
            'qnKhOb',
            long_data,
            None,
            'generic'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form