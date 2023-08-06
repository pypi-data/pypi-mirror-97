from bs4 import BeautifulSoup
from .general import get_data
from ..utils import list_get


def details(response):
    return _Details(response).parse()

class _Details:
    def __init__(self, response):
        self.response = response
        try:
            self.soup = BeautifulSoup(response, 'lxml')
        except:
            self.soup = BeautifulSoup(response, 'html.parser')

    def parse(self):
        self.jLZZ2e = get_data('jLZZ2e', self.response, self.soup)
        self.jLZZ2e = list_get(self.jLZZ2e, [0], [])
        self.IoIWBc = get_data('IoIWBc', self.response, self.soup)
        self.d5UeYe = get_data('d5UeYe', self.response, self.soup)
        self.d5UeYe = list_get(self.d5UeYe, [0], [])
        self.MLWfjd = get_data('MLWfjd', self.response, self.soup)

        return {
            'title':  self.title,
            'description': self.description,
            'screenshots': self.screenshots,
            'icon': self.icon, 
            'additional_info': self.additional_info,
            'editors_choice': self.editors_choice,
            'whats_new': self.whats_new,
            'category': self.category,
            'released': self.released,
            'esrb': self.esrb,
            'prices': self.prices,
            'rating_value': self.rating_value,            
            'histogram': self.histogram,
            'rating_count': self.rating_count,
        }

    @property
    def title(self):        
        return list_get(self.jLZZ2e, [0, 0])

    @property
    def description(self):
        _description = list_get(self.jLZZ2e, [10, 0, 1])
        try:
            return _description.replace('<br>', '\n')
        except:
            return _description

    @property
    def screenshots(self):
        return [ss[3][2] for ss in list_get(self.jLZZ2e, [12, 0]) or []]

    @property
    def icon(self):
        return list_get(self.jLZZ2e, [12, 1, 3, 2])

    @property
    def additional_info(self):
        offered_by = list_get(self.jLZZ2e, [12, 5, 1])
        installs = list_get(self.jLZZ2e, [12, 9])
        interactive_elements = list_get(self.jLZZ2e, [12, 4, 3, 1])
        in_app_products = list_get(self.jLZZ2e, [12, 12, 0])

        content_rating = [list_get(self.jLZZ2e, [12, 4, 0])]
        cr = list_get(self.jLZZ2e, [12, 4, 2])
        if isinstance(cr, list):
            for item in cr[1:]:
                content_rating.append(item)

        developer = {
            'site': list_get(self.jLZZ2e, [12, 5, 3, 5, 2]),
            'mailto': list_get(self.jLZZ2e, [12, 5, 2, 0]),
            'more_apps': list_get(self.jLZZ2e, [12, 5, 5, 4, 2]),
            'privacy_policy': list_get(self.jLZZ2e, [12, 7, 2]),
            'address': list_get(self.jLZZ2e, [12, 5, 4, 0]),
        }

        soup_div = self.soup.find(lambda tag: tag.text == 'Updated')
        try:
            sibling = soup_div.next_sibling
            updated = sibling.find(text=True)
        except:
            updated = None

        app_size = list_get(self.IoIWBc, [0])
        current_version = list_get(self.IoIWBc, [1])
        requires_android = list_get(self.IoIWBc, [2])

        return {
            'offered_by': offered_by,
            'installs': installs,
            'interactive_elements': interactive_elements,
            'in_app_products': in_app_products,
            'content_rating': content_rating,
            'updated': updated,
            'app_size': app_size,
            'current_version': current_version,
            'requires_android': requires_android,
            'developer': developer,
        }

    @property
    def editors_choice(self):
        return bool(list_get(self.jLZZ2e, [12, 15, 0]))

    @property
    def whats_new(self):
        _whats_new = list_get(self.jLZZ2e, [12, 6, 1])
        try:
            return _whats_new.replace('<br>', '\n')
        except:
            return _whats_new

    @property
    def category(self):
        return list_get(self.jLZZ2e, [12, 13, 0, 2])

    @property
    def released(self):
        return list_get(self.jLZZ2e, [12, 36])

    @property
    def esrb(self):
        return {
            'description': list_get(self.jLZZ2e, [12, 4, 0]),
            'icon': list_get(self.jLZZ2e, [12, 4, 7, 3, 2])
        }

    @property
    def prices(self):
        _prices = list_get(self.d5UeYe, [2, 0, 0, 0, 1])
        try:
            normal_price = {
                'raw': _prices[-1][0],
                'currency': _prices[-1][1],
                'formatted': _prices[-1][2]
            }
        except:
            normal_price = None

        try:
            offer_price = {
                'raw': _prices[-2][0],
                'currency': _prices[-2][1],
                'formatted': _prices[-2][2]
            }
        except:
            offer_price = None

        return {
            'normal': normal_price,
            'offer': offer_price
        }

    @property
    def rating_value(self):
        return list_get(self.MLWfjd, [0, 6, 0])

    @property
    def histogram(self):
        return {
            '1': list_get(self.MLWfjd, [0, 6, 1, 1, 1]),
            '2': list_get(self.MLWfjd, [0, 6, 1, 2, 1]),
            '3': list_get(self.MLWfjd, [0, 6, 1, 3, 1]),
            '4': list_get(self.MLWfjd, [0, 6, 1, 4, 1]),
            '5': list_get(self.MLWfjd, [0, 6, 1, 5, 1]),
        }

    @property
    def rating_count(self):
        return list_get(self.MLWfjd, [0, 6, 2, 1])