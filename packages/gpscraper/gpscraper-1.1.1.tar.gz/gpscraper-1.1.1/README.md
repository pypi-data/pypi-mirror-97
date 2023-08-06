# gpscraper

Welcome to this Google Play scraper.

## Installation
```
pip install gpscraper
```

## What does it offer?
- [Search results](#search-results)
- [App details](#app-details)
- [App reviews](#app-reviews)
- [App review history](#app-review-history)
- [App permissions](#app-permissions)

## Search results

Use the function generator `search`, its parameters are:
- **query**: the search query.
- **token (default=None)**: used for search continuation.
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

## App details

You will gather lots of information from an specific application. Use the function `details`, it parameters are:
- **app_id**: app id/package name.
- **lang (default="en")**: app details language to be shown.

**Example**
```python
import gpscraper as gp

details = gp.details('com.mojang.minecraftpe')
```

And get something like this
```python
{
    "title": "Minecraft",
    "description": "Explore infinite worlds and build everything from the simplest...",
    "screenshots": [
        "https://play-lh.googleusercontent.com/0-zBoTxVn5PJQtNNnovURx1JIbIytd7_H8f...",
        "https://play-lh.googleusercontent.com/Cq6Sju3wrs8IvE7y0w1pGwjO1FNZchjIbXE...",
        "https://play-lh.googleusercontent.com/_T5Onj0iaqQjYTf-PNVMXBVENNm5LpQLeMA...",
        "https://play-lh.googleusercontent.com/0NS4VI__zHQ5ZG9sDNJF4C6uaccSgqUKV4T...",
        "https://play-lh.googleusercontent.com/eM2N3BdyvKYVI8V4eOZQxHFx9DFc9r1s0mk...",
        "https://play-lh.googleusercontent.com/GszvU00I5sSnujEL_zg4905MJuoBs4X57t5...",
        "https://play-lh.googleusercontent.com/34W0sPkaT9YL1mKYfJklQHS9N7FXVsFaW_v...",
        "https://play-lh.googleusercontent.com/8O1-J7YFRB1vtq4J73zkRXU-Zf7KWAXHdor..."
    ],
    "icon": "https://play-lh.googleusercontent.com/VSwHQjcAttxsLE47RuS4PqpC4LT7lCo...",
    "additional_info": {
        "offered_by": "Mojang",
        "installs": [
            "10,000,000+",
            10000000,
            34477214,
            "10M+"
        ],
        "interactive_elements": "Users Interact",
        "in_app_products": "$0.99 - $49.99 per item",
        "content_rating": [
            "Everyone 10+",
            "Fantasy Violence"
        ],
        "updated": "December 11, 2020",
        "app_size": "Varies with device",
        "current_version": "1.16.201.01",
        "requires_android": "Varies with device",
        "developer": {
            "site": "http://help.mojang.com",
            "mailto": "help@minecraft.net",
            "more_apps": "/store/apps/dev?id=4772240228547998649",
            "privacy_policy": "https://privacy.microsoft.com/en-us/privacystatement",
            "address": "Mojang\nMaria Skolgata 83\n118 53\nStockholm\nSweden"
        }
    },
    "editors_choice": True,
    "whats_new": "What&#39;s new in 1.16.201: Various bug fixes!",
    "category": "GAME_ARCADE",
    "released": "Aug 15, 2011",
    "esrb": {
        "description": "Everyone 10+",
        "icon": "https://play-lh.googleusercontent.com/bxs95MghtAOuZR_LPwVCUmUPYEv..."
    },
    "prices": {
        "normal": {
            "raw": 7490000,
            "currency": "USD",
            "formatted": "$7.49"
        },
        "offer": None
    },
    "rating_value": [
        "4.5",
        4.528572
    ],
    "histogram": {
        "1": 262486,
        "2": 72223,
        "3": 140257,
        "4": 312121,
        "5": 3156782
    },
    "rating_count": 3943871
}
```

## App reviews

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
                "reply": "We are glad you enjoy the hard work we ...",
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

## App review history

You can get app's single review history (all edits from that review). Use the function `review_history`, its parameters are:
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
        "comment": "Really nice interface with fast access to all...",
        "epoch": 1611289171,
        "datetime": "2021-01-22 00:19:31",
        "app_version": "1.4.0"
    },
    {
        "id": "gp:AOqpTOHJ5XsIP4YtJgaSHnqlNMYqNaFwjWMZ1L-o7hvqmfUTPgmOdd...",
        "name": "Foo Bar",
        "profile_pic": "https://play-lh.googleusercontent.com/a-/AOh14GhXO...",
        "background_pic": "https://play-lh.googleusercontent.com/Yq7oyNI...",
        "rating": 5,
        "comment": "nice interface.",
        "epoch": 1611279171,
        "datetime": "2021-01-21 21:32:51",
        "app_version": "1.4.0"
    },
    {...}
]
```

## App permissions

Every access available for the current application. Use the function `permissions`, its parameters are:
- **app_id**: app id/package name.
- **lang (default="en")**: app details language to be shown.

**Example**
```python
import gpscraper as gp

permissions = gp.permissions('com.t2kgames.civrev2')
```

And get something like this
```python
[
    {
        "access": "Identity",
        "icon": "https://play-lh.googleusercontent.com/AUs-Fih7eEfuhp-4lYG...",
        "details": [
            "find accounts on the device"
        ]
    },
    {
        "access": "Contacts",
        "icon": "https://play-lh.googleusercontent.com/c5fJsmDZCeHY1tZmeGX...",
        "details": [
            "find accounts on the device"
        ]
    },
    {
        "access": "Photos/Media/Files",
        "icon": "https://play-lh.googleusercontent.com/pHtIujPWxciAZcfYSw...",
        "details": [
            "read the contents of your USB storage",
            "modify or delete the contents of your USB storage"
        ]
    },
    {
        "access": "Storage",
        "icon": "https://play-lh.googleusercontent.com/aWNKQedLTpw6u6yyMj...",
        "details": [
            "read the contents of your USB storage",
            "modify or delete the contents of your USB storage"
        ]
    },
    {
        "access": "Wi-Fi connection information",
        "icon": "https://play-lh.googleusercontent.com/U-_SG8pHTsqU_IyZTG...",
        "details": [
            "view Wi-Fi connections"
        ]
    },
    {
        "access": "Other",
        "icon": "https://play-lh.googleusercontent.com/pkKXoPl5q7n8T0s7KR...",
        "details": [
            "view network connections",
            "full network access",
            "prevent device from sleeping",
            "Google Play license check"
        ]
    }
]
```


[#top](#gpscraper)
