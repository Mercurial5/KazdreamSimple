import json
import re

import requests
from bs4 import BeautifulSoup


class Parser:
    domain = 'https://shop.kz'
    base_link = '/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
    headers = {
        'User-Agent': 'beep-boop shopkz let me to your website'
    }

    def get_items(self) -> list[dict]:
        """
        Scraps all the smartphones.

        :return: list[dict]
        """
        page, has_next_page = 1, True

        while has_next_page:
            link = f'{self.domain}{self.base_link}?PAGEN_1={page}'
            has_next_page, items = self._parse_page(link)

            # This way we don't need to wait when all the items are parsed.
            # There are a lot of downsides (when we wait for all items and only then return) so I used yield instead.
            # Although in this case I anyway turn everything to list when saving items in smartphones.
            yield from items

            page += 1

    def _parse_page(self, link: str) -> tuple[bool, list[dict]]:
        """
        Scraps all the smartphones from one page.

        If there is another page, return True (as first parameter in tuple), otherwise False.

        :param link: str
        :return: tuple[bool, list[dict]]
        """

        response = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        next_link = soup.find('link', attrs={'rel': 'next'})
        has_next_page = next_link is not None

        items = soup.find_all('div', attrs={'class': 'bx_catalog_item_container gtm-impression-product'})
        items = [self._parse_item(item['data-product']) for item in items]

        return has_next_page, items

    def _parse_item(self, data: str) -> dict:
        data = json.loads(data)
        return {
            'id': data['item_id'],
            'name': data['item_name'],
            'price': int(data['price']),
            'memory': self._parse_memory(data['item_name'])
        }

    @staticmethod
    def _parse_memory(name: str) -> str:
        """
        The safest method to parse memory would be this one:

        Go to the smartphone page and find key `a_OPERATIVE_MEMORRY`, which has correct memory size.
        But this method requires us to make a request (1) and parse html tree (2).
        And considering amount of phones the time to parse each phone will sum-up and will slow the parsing overall.

        This is why I decided to use regular expressions, because every phone has memory-size in their names.

        Note:
        To make this method perfect, we could add one condition. If regular expression found memory size and
        didn't raise any errors, it will just return the memory size. Otherwise, it would make a request and
        took memory size from the `a_OPERATIVE_MEMORRY` key.

        P.S. I didn't make this method `perfect` because it worked this way anyway.
        P.S.S. And it also would make my code `dirtier`. (Too long to explain...)

        :param name: str
        :return: str
        """
        return re.search(r'(\d+)\s*[TG][Bb]', name).group()
