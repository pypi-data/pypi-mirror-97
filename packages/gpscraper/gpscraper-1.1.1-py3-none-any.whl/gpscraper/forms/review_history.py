import json


def review_history(app_id, review_id):
    # It looks like 40 is the review_size but it doesnt matter
    # because we wont be iterating through a long review history.
    long_data = (
        f'[null,null,[4,null,[40]],["{app_id}",7],"{review_id}"]'
    )

    form = {
        'f.req': [[[
            'UsvDTd',
            long_data,
            None,
            '1'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form