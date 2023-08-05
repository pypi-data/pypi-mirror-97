# gpscraper

Welcome to this Google Play scraper which offers you the following:
- [Search results](#search-results)
- [App details](#app-details)
- [App reviews](#app-reviews)
- [App review history](#app-review-history)

## Search results

Use the function generator `search`, its parameters are:
- **query**: the search query.
- **token (default=None)**: used for search contination.
- **unknown_1 (default=None)**: used for search continuation.
- **pagination_delay (default=1)**: time between each scrape pagination.
- **lang (default="en")**: language of results.

> You will get a list in each pagination.

**Example**
```python
import gpscraper as gp

searches = [s for s in gp.search('github')]
```

You will get something like this
```python
[
    {
        "search": [
            {
                "icon": "https://play-lh.googleusercontent.com/PCpXdqvUWfC....",
                "title": "GitHub",
                "offered_by": "GitHub",
                "developer": {
                    "more_apps": "/store/apps/developer?id=GitHub"
                },
                "description": "Triage notifications, review, comment, and ...",
                "rating": [
                    "4.7",
                    4.6537657
                ],
                "app_id": "com.github.android"
            },
            {
                "icon": "https://play-lh.googleusercontent.com/kAmJ52R7k_H...",
                "title": "FastHub for GitHub",
                "offered_by": "Fast Access",
                "developer": {
                    "more_apps": "/store/apps/developer?id=Fast+Access"
                },
                "description": "FastHub is the ultimate unofficial client for GitHub",
                "rating": [
                    "4.4",
                    4.361516
                ],
                "app_id": "com.fastaccess.github"
            },
            {...}
        ],
        "next": {
            "query": "github",
            "token": "Cgj6noGdAwIIChAKGguCAQgKBmd...",
            "unknown_1": "[10,[10,50]],true,null,[96,...",
            "pagination_delay": 1,
            "lang": "en"
        }
    },
    {
        "search": [...],
        "next": {...}
    },
    {...}
]
```

> You may have noticed the `next` field, that is because each pagination contains a token for the next results, also `search` retrieves all results available, so if you break in a loop and want to continue from the last results found, you can do something like this:

```python
for s in gp.search(**searches[-1]['next']):
    searches.append(s)
```

### App details

You will gather lots of information from an specific application. Use the function `details`, it parameters are:
- **app_id**: app id/package name.
- **lang (default="en")**: app details language to be shown.

**Example**
```python
import gpscraper as gp

details = gp.details('com.github.android')
```

And get something like this
```python
{
    "title": "GitHub",
    "description": "There's a lot you can do on G...",
    "screenshots": [
        "https://play-lh.googleusercontent.com/_x8EKTss...",
        "https://play-lh.googleusercontent.com/oJIO3RR...",
        "https://play-lh.googleusercontent.com/UY_55o3qfR...",
        "https://play-lh.googleusercontent.com/BP7LyjN7Z..."
    ],
    "icon": "https://play-lh.googleusercontent.com/PCpXdqvUWf...",
    "additional_info": {
        "offered_by": "GitHub",
        "installs": [
            "1,000,000+",
            1000000,
            1455151,
            "1M+"
        ],
        "interactive_elements": "Users Interact",
        "in_app_products": None,
        "content_rating": [
            "Everyone"
        ],
        "updated": "February 17, 2021",
        "app_size": "9.7M",
        "current_version": "1.4.9",
        "requires_android": "6.0 and up",
        "developer": {
            "site": "https://github.com/mobile",
            "mailto": "mobilefeedback+android@github.com",
            "more_apps": "/store/apps/developer?id=GitHub",
            "privacy_policy": "https://help.github.com/en/...",
            "address": None
        }
    },
    "editors_choice": False,
    "whats_new": "Introducing Sponsors! A new button in the...",
    "category": "PRODUCTIVITY",
    "released": "Feb 15, 2020",
    "esrb": {
        "description": "Everyone",
        "icon": "https://play-lh.googleusercontent.com/OBVqgRK7eer..."
    },
    "prices": {
        "normal": {
            "raw": 0,
            "currency": "USD",
            "formatted": ""
        },
        "offer": None
    },
    "rating_value": [
        "4.7",
        4.6537657
    ],
    "histogram": {
        "1": 343,
        "2": 286,
        "3": 754,
        "4": 2577,
        "5": 14288
    },
    "rating_count": 18249
}
```

### App reviews

You can also retrieve all reviews from an specific app. Use the function generator `reviews`, its parameters are:
- **app_id**: app id/package name.
- **token (default=None)**: used for search contination.
- **pagination_delay (default=1)**: time between each scrape pagination.
- **review_size (default=100)**: total reviews per page, except page 1, which always retrieves 40 reviews.
- **sort_by (default="most_relevant")**: Sorting option, available options are *most_relevant*, *newest* and *rating*.
- **rating (default=0)**: Shows reviews by rating. Zero (0) means all ratings.
- **lang (default="en")**: language of results.

> You will get a list in each pagination.

**Example**
```python
import gpscraper as gp

reviews = [r for r in gp.reviews('com.github.android)]
```

And get something like this
```python
[
    {
        "reviews": [
            {
                "id": "gp:AOqpTOH7nyGs86KRcFE3xd9y9N2Mr0tIrIaGsT77BP...",
                "rating": 5,
                "name": "John Doe",
                "comment": "Really good app with clean and intuiti",
                "reply": None,
                "app_version": "1.4.9",
                "epoch": 1613707223,
                "datetime": "2021-02-19 00:00:23",
                "profile_pic": "https://play-lh.googleusercontent.com/a-/AOh14...",
                "background_pic": "https://play-lh.googleusercontent.com/Yq7oy...",
                "likes": 28
            },
            {
                "id": "gp:AOqpTOEtto46NQ4KQhs1Za7GKkT5gyJd1x0Teq-6-5HLu...",
                "rating": 4,
                "name": "User 2",
                "comment": "The app is very good! Has beautiful UI design an...",
                "reply": None,
                "app_version": "1.4.4",
                "epoch": 1613482474,
                "datetime": "2021-02-16 09:34:34",
                "profile_pic": "https://play-lh.googleusercontent.com/a-/AOh1...",
                "background_pic": "https://play-lh.googleusercontent.com/Yq7oyN...",
                "likes": 24
            },
            {...}            
        ],
        "next": {
            "app_id": "com.github.android",
            "token": "CsUBCsIBKpsBCm73O5rM0f____9nYWlhOjAwMDAwMGUzMjYyNGZhNzk6...",
            "pagination_delay": 1,
            "review_size": 100,
            "sort_by": "most_relevant",
            "rating": 0,
            "lang": "en"
        }
    },
    {
        "reviews": [...],
        "next": {...}
    },
    {...}
]
```

> You also get the `next` field to continue pagination in case you break the loop.
```python
for r in gp.search(**reviews[-1]['next']):
    reviews.append(r)
```

### App review history

You can get the history from an app's single review. Use the function `review_history`, its parameters are:
- **app_id**: app id/package name.
- **review_id**: review id.

**Example**
```python
import gpscraper as gp

history = gp.review_history('com.github.android', 'gp:AOqpTOHJ5XsIP4YtJgaSHnqlN...')
```

And get something like this
```python
[
    {
        "id": "gp:AOqpTOHJ5XsIP4YtJgaSHnqlNMYqNaFwjWMZ1L-o7hvqmfUTPgmOdd...",
        "name": "Foo Bar",
        "profile_pic": "https://play-lh.googleusercontent.com/a-/AOh14GhXO...",
        "background_pic": "https://play-lh.googleusercontent.com/Yq7oyNI...",
        "rating": 5,
        "comment": "really nice interface with fast access...",
        "epoch": 1611289171,
        "datetime": "2021-01-22 00:19:31",
        "app_version": "1.4.0"
    },
    {...}
]
```
