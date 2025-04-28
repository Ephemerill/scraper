
"""
from bs4 import BeautifulSoup
import requests

source = requests.get('https://cafebiola.cafebonappetit.com/cafe/cafe-biola/').text
#with open('10:13:24.html') as html_file:
    #soup = BeautifulSoup(html_file, 'lxml')
soup = BeautifulSoup(source, 'lxml')





print("\n\n**********************\nBreakfast\n**********************\n")
for breakfast in soup.find_all('section', id='breakfast'):
    for stations in breakfast.find_all('div', class_='station-title-inline-block'):
        name = stations.h3.text
        if (name=="kettle" or name=="home cookin'" or name=="6th st. grill" or name=="pizzeria"):
            print(name)
            print("--------------------")
            for options in stations.find_all('button'):
                option = options.text.strip()
                print(option)
            print("--------------------")

print("\n\n**********************\nLunch\n**********************\n")
for lunch in soup.find_all('section', id='lunch'):
    for real in lunch.find_all('div', {'data-key-index': '0'}):
        for stations in real.find_all('div', class_='station-title-inline-block'):
            name = stations.h3.text
            if (name=="kettle" or name=="home cookin'" or name=="6th st. grill" or name=="pizzeria"):
                print(name)
                print("--------------------")
                for options in stations.find_all('button'):
                    option = options.text.strip()
                    print(option)
                print("--------------------")

print("\n\n**********************\nDinner\n**********************\n")
for dinner in soup.find_all('section', id='dinner'):
    for real in dinner.find_all('div', {'data-key-index': '0'}):
        for stations in real.find_all('div', class_='station-title-inline-block'):
            name = stations.h3.text
            if (name=="kettle" or name=="home cookin'" or name=="6th st. grill" or name=="pizzeria"):
                print(name)
                print("--------------------")
                for options in stations.find_all('button'):
                    option = options.text.strip()
                    print(option)
                print("--------------------")
"""

import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

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

# Generate today's date for the filename
today_date = datetime.now().strftime('%Y-%m-%d')
filename = f'menu_data_{today_date}.json'

# Save to JSON file
with open(filename, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f'Menu data saved to {filename}')
