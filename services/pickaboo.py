from bs4 import BeautifulSoup
import bs4
import requests

from api.schemas import Product

domain = 'pickaboo.com'


def getProduct(url) -> dict:
    url = url.replace(' ', '')
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup is None:
            return None
        try:
            title = soup.find('span', class_="base").get_text().strip()
        except:
            title = ''
            return None
        try:
            pricestr = soup.find('span', class_="price").get_text().strip()[1:]
            price = float(pricestr.replace(',', ''))
        except:
            price = 0
        try:
            # image = soup.find('img', class_="fotorama__img--full")['src']
            image = soup.find('img', class_="fotorama__img")['src']
        except:
            image = None
    except:
        print(' ***error pickaboo***')
        return None
    return {'title': title, 'price': price, 'image': image, 'url': url}
    # return Product(title, price, image, url)


def getProductTile(product: bs4.element.Tag):
    try:
        producturl = product.find('a')['href']
    except:
        return None
    try:
        title = product.find(
            'a', class_="product-item-link").get_text().strip()
    except:
        title = ''
    try:
        pricestr = product.find('span', class_="price").get_text().strip()[1:]
        price = float(pricestr.replace(',', ''))
    except:
        price = 0
    try:
        image = product.find('img', class_="product-image-photo")['src']
    except:
        image = None
    return {'title': title, 'price': price, 'image': image, 'url': producturl}


def searchProduct(query) -> list:
    query = query.strip()
    queryfields = query.split(' ')
    searchQuery = ('+').join(queryfields)
    # print(searchQuery)
    url = 'https://www.pickaboo.com/catalogsearch/result/?q=' + searchQuery
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup)
        products = []
        for productTile in soup.find_all('li', class_="item product product-item"):
            product = getProductTile(productTile)
            if product:
                products.append(product)
        return products
    except:
        print(' ***error search pickaboo***')
        return None
