import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def scrape_menu():
    # Scrape the website
    source = requests.get('https://cafebiola.cafebonappetit.com/cafe/cafe-biola/').text
    soup = BeautifulSoup(source, 'lxml')

    data = {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    }

    # Extract breakfast options
    for breakfast in soup.find_all('section', id='breakfast'):
        for stations in breakfast.find_all('div', class_='station-title-inline-block'):
            name = stations.h3.text
            if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                options = []
                for button in stations.find_all('button'):
                    option = button.text.strip()
                    options.append(option)
                data['breakfast'].append({'name': name, 'options': options})

    # Extract lunch options
    for lunch in soup.find_all('section', id='lunch'):
        for real in lunch.find_all('div', {'data-key-index': '0'}):
            for stations in real.find_all('div', class_='station-title-inline-block'):
                name = stations.h3.text
                if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                    options = []
                    for button in stations.find_all('button'):
                        option = button.text.strip()
                        options.append(option)
                    data['lunch'].append({'name': name, 'options': options})

    # Extract dinner options
    for dinner in soup.find_all('section', id='dinner'):
        for real in dinner.find_all('div', {'data-key-index': '0'}):
            for stations in real.find_all('div', class_='station-title-inline-block'):
                name = stations.h3.text
                if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                    options = []
                    for button in stations.find_all('button'):
                        option = button.text.strip()
                        options.append(option)
                    data['dinner'].append({'name': name, 'options': options})

    return data