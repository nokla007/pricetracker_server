from bs4 import BeautifulSoup
import bs4
import requests



domain = 'gadstyle.com'


def getProduct(url) -> dict:
    url = url.replace(' ', '')
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            title = soup.find(
                'div', class_="summary-inner").find('h1').get_text().strip()
        except:
            title = ''
        try:
            pricestr = soup.find('p', class_="price").find(
                'ins').get_text().strip()[1:]
            price = float(pricestr.replace(',', ''))
        except:
            price = 0
        try:
            image = soup.find(
                'div', class_='product-images-inner').find('img')['src']
        except:
            image = None
    except:
        print(' ***error gadstyle***')
        return None
    return {'Title': title, 'Price': price, 'image': image, 'URL': url}


def getProductTile(product: bs4.element.Tag):
    try:
        producturl = product.find('a')['href']
    except:
        return None
    try:
        title = product.find('h3').get_text().strip()
    except:
        title = ''
    try:
        pricestr = product.find('span', class_="price").find(
            'ins').get_text().strip()[1:]
        price = float(pricestr.replace(',', ''))
    except:
        price = 0
    try:
        image = product.find('img')['src']
    except:
        image = None
    return {'Title': title, 'Price': price, 'image': image, 'URL': producturl}


def searchProduct(query) -> list:
    query = query.strip()
    queryfields = query.split(' ')
    searchQuery = ('+').join(queryfields)
    # print(searchQuery)
    url = 'https://www.gadstyle.com/?post_type=product&s=' + searchQuery
    # print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    products = []
    for productTile in soup.find_all('div', class_="product-wrapper"):
        product = getProductTile(productTile)
        if product:
            products.append(product)
    return products

