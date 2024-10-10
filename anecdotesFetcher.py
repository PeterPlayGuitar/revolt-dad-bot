import random

import requests
from bs4 import BeautifulSoup


def fetchRandom():
    # Step 1: Fetch the website's HTML content
    url = "https://www.anekdot.ru/random/anekdot/"  # Replace with the target URL
    response = requests.get(url)

    # Step 2: Check if the request was successful
    if response.status_code == 200:
        # Step 3: Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        content_div = soup.find('div', class_='content-min')
        if content_div:
            text_divs = content_div.find_all('div', class_='text')

            return text_divs[random.randint(0, len(text_divs) - 1)].text
    return None
