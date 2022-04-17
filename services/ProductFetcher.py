from bs4 import BeautifulSoup
import requests

pickabooDomain = 'pickaboo.com'


def pickaboo(url) -> dict:
    url = url.replace(' ', '')
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            title = soup.find('span', class_="base").get_text().strip()
        except:
            title = ''
        try:
            # availability = soup.find(title="Availability").get_text().strip()
            # if availability == 'In stock':
            #     price = soup.find(
            #         'span', class_="price").get_text().strip()[1:]
            pricestr = soup.find('span', class_="price").get_text().strip()[1:]
            price = float(pricestr.replace(',', ''))
        except:
            price = 0
        try:
            image = soup.find('img', class_="fotorama__img--full")['src']
            # image = soup.find('img', class_="fotorama__img")
            print(image)
        except:
            image = None
    except:
        print(' ***error***')
        return None
    return {'Title': title, 'Price': price, 'image': image, 'URL': url}


ecoms = [
    (pickabooDomain, pickaboo),
]


def getProduct(url):
    url = url.replace(' ', '')
    # if(url.find(pickabooDomain) > 0):
    #     return pickaboo(url)
    for ecom in ecoms:
        if(url.find(ecom[0]) > 0):
            return ecom[1](url)
    return None


if __name__ == '__main__':
    print(getProduct('https://www.pickaboo.com/redmi-note-11-6gb-128gb.html'))
