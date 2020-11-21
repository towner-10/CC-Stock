# Canada Computers Stock Checker

This script is written in Python 3 and uses the following libraries
- requests
- threading
- BeautifulSoup
- win10toast_persist

## How to Run

Make sure you have Python3 installed and use `pip3` to install the required packages if needed. Python3 can be acquired via Windows Store.

Run this script in a program that supports colour code output. I used Windows Terminal which can be acquired on the Windows Store.

Run the script using `python3 <folder>/main.py` and it will then start running and sending desktop notifications when a product is availible in stock. If you don't want to track RTX 3080s, change the URL to the product that you want to track on the search page.

If you don't want desktop notifications, just set `ENABLE_DESKTOP_NOTIFICATIONS` to `False`