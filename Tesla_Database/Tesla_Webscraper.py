from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv

#Beautiful soup code below finds all the addresses of Tesla stores, service centers, and superchargers. Pulls all addreses from 'vcard' for all Tesla locations listed on website.
def find_address (country,append,filename):
    url = 'https://www.tesla.com' + append

    #Required to get around Tesla anti-scraping
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()

    page_soup = soup(webpage, "html.parser")

    addresses = page_soup.find_all('address', class_='vcard')

    for address in addresses:
        try:
            name = address.find('a').contents[0]
        except:
            name = ''

        try:
            street = address.find('span', class_= 'street-address').text.strip()
        except:
            street = ''

        try:
            extended = address.find('span', class_='extended-address').text.strip()
        except:
            extended = ''

        try:
            locality = address.find('span', class_='locality').text.strip()
        except:
            locality = ''

        try:
            phone = address.find('span', class_='value').text.strip()
        except:
            phone = ''


        with open(filename, 'a', encoding='utf8') as f:
            f.write('%s|' % country)
            f.write('%s|' % name)
            f.write('%s|' % street )
            f.write('%s|' % extended)
            f.write('%s|' % locality)
            f.write('%s|' % phone)
            f.write('\n')

# Main executable. Iterates through all links in the 'findus' page and scrapes locations.
url = 'https://www.tesla.com/findus/list'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

webpage = urlopen(req).read()

page_soup = soup(webpage, "html.parser")

divs = page_soup.find_all('div', class_ = 'row')
count = 0

for div in divs:
    div = div.find_all('ul')
    for elements in div:
        for tag in elements.find_all("li"):
            address = str(tag.a).split('\"')[1]
            country = tag.span.text.strip()
            find_address(country, address, 'filetest2.csv')
            print(count)
            count = count + 1
