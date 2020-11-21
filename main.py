import requests
import threading
import json
from bs4 import BeautifulSoup
from win10toast_persist import ToastNotifier
import urllib.parse as urlparse
from urllib.parse import parse_qs

counter = 0

# Change URL to other product such as the RTX 3070
# https://www.canadacomputers.com/index.php?cPath=43&sf=:3_7&mfr=&pr=
URL = 'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_5&mfr=&pr='

# Prefered location
ENABLE_PREF_LOCATION = True
LOCATION_CODE = 'LOND'

# Desktop Notification
ENABLE_DESKTOP_NOTIFICATIONS = True

toaster = ToastNotifier()

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    CLEAR = '\033[H\033[J'

def getData():
    global counter
    threading.Timer(30.0, getData).start()

    try:
        page = requests.get(URL)
    except:
        print("Could not connect to: " + URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_="col-xl-3 col-lg-4 col-6 mt-0_5 px-0_5 toggleBox mb-1")

    print(bcolors.CLEAR, end='')

    itemCount = 0

    for stock in results:
        stockStatus = stock.find('div').find('div').find('div', class_="allInfoSearch").find('div', class_='row').find('div').find('a').find_all('div')[1].text.strip()
        stockURL = stock.find('div').find('div').find('div', class_="productImageDesc").find('div', class_='row').find('div', class_='productInfoSearch').find('span').find('a').get('href')
        stockName = stock.find('div').find('div').find('div', class_="productInfoSearch").find('span', class_='productTemplate_title').find('a').text.strip()

        itemCount += 1

        if (stockStatus != 'In-Store Back Order'):
            parsed = urlparse.urlparse(stockURL)
            stockCheckURL = 'https://www.canadacomputers.com/product_info.php?ajaxstock=true&itemid=' + str(parse_qs(parsed.query)['item_id'][0])

            try:
                if (ENABLE_PREF_LOCATION == True):
                    cookies = {'preferloc': LOCATION_CODE}
                    stockCheckRequest = json.loads(requests.get(stockCheckURL, cookies=cookies).text)
                else:
                    stockCheckRequest = json.loads(requests.get(stockCheckURL).text)
                
            except:
                print(bcolors.FAIL + "Error getting stock data!" + bcolors.ENDC)

            if (ENABLE_DESKTOP_NOTIFICATIONS == True):
                toaster.show_toast(stockStatus, stockName, duration=None)

            print(bcolors.OKGREEN + bcolors.BOLD + stockStatus + bcolors.ENDC + " | " + (stockCheckRequest['loc'] + " - " + str(stockCheckRequest['avail']) + " | " + stockName).ljust(111))
        else:
            print(bcolors.FAIL + bcolors.BOLD + stockStatus + bcolors.ENDC + " | " + stockURL)

    counter += 1

    print('\nChecks: ' + str(counter) + '\t Items this loop: ' + str(itemCount))

getData()