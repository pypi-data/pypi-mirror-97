import json


def permissions(app_id):
    form = {
        'f.req': [[[
            'xdSrCf',
            f'[[null,["{app_id}",7],[]]]',
            None,
            '1'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form