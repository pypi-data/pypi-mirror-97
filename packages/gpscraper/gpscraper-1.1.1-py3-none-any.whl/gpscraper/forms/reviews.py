import json


def reviews_next_page(app_id, token, review_size, sort_by, rating):
    if not token:
        token = json.dumps(None)
    else:
        token = f'"{token}"'

    sort_by = json.dumps(sort_by)

    if 1 <= rating <= 5:
        rating = f'[null,{rating}]'
    else:
        # By default, Google Play shows reviews of all ratings.
        rating = '[]'

    long_data = (
        f'[null,null,[2,{sort_by},[{review_size},null,'
        f'{token}],null,{rating}],["{app_id}",7]]'
    )

    form = {
        'f.req': [[[
            'UsvDTd',
            long_data,
            None,
            'generic'
        ]]]
    }

    form['f.req'] = json.dumps(form['f.req'], separators=(',', ':'))
    return form
