from typing import List
from bs4 import BeautifulSoup
import requests
from . import pickaboo, gadstyle


ecoms = [
    (pickaboo.domain, pickaboo.getProduct, pickaboo.searchProduct),
    (gadstyle.domain, gadstyle.getProduct, gadstyle.searchProduct),
]


def getProduct(url) -> dict:
    url = url.replace(' ', '')
    # if(url.find(pickabooDomain) > 0):
    #     return pickaboo(url)
    for ecom in ecoms:
        if(url.find(ecom[0]) > 0):
            return ecom[1](url)
    return None


def searchProduct(query) ->List[dict]:
    products = []
    for ecom in ecoms:
        products.extend(ecom[2](query))
    return products


if __name__ == '__main__':
    # print(getProduct('https://www.pickaboo.com/redmi-note-11-6gb-128gb.html'))
    print(searchProduct('anker q30'))
