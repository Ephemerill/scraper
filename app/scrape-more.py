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

    # Function to extract menu option and description for a given item div
    def extract_item_details(item_div):
        button = item_div.find('button', class_='site-panel__daypart-item-title')
        name = button.text.strip() if button else None
        description_div = item_div.find('div', class_='site-panel__daypart-item-content')
        description = None
        if description_div:
            description_element = description_div.find('div', class_='site-panel__daypart-item-description')
            description = description_element.text.strip() if description_element else None
        return {'name': name, 'description': description}

    # Function to extract all options for a station, including siblings with descriptions
    def get_station_items(station_block):
        station_name = station_block.h3.text
        all_items = []
        # Extract item details from the initial station title block's siblings
        for sibling in station_block.find_next_siblings():
            if sibling.get('class') and 'station-title-inline-block' in sibling.get('class'):
                break
            if sibling.get('class') and 'site-panel__daypart-item' in sibling.get('class'):
                item_details = extract_item_details(sibling)
                if item_details['name']:
                    all_items.append(item_details)
        return station_name, all_items

    # Extract breakfast options
    for breakfast in soup.find_all('section', id='breakfast'):
        for stations in breakfast.find_all('div', class_='station-title-inline-block'):
            name = stations.h3.text
            if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                station_name, items = get_station_items(stations)
                if items:
                    data['breakfast'].append({'name': station_name, 'items': items})

    # Extract lunch options
    for lunch in soup.find_all('section', id='lunch'):
        for real in lunch.find_all('div', {'data-key-index': '0'}):
            for stations in real.find_all('div', class_='station-title-inline-block'):
                name = stations.h3.text
                if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                    station_name, items = get_station_items(stations)
                    if items:
                        data['lunch'].append({'name': station_name, 'items': items})

    # Extract dinner options
    for dinner in soup.find_all('section', id='dinner'):
        for real in dinner.find_all('div', {'data-key-index': '0'}):
            for stations in real.find_all('div', class_='station-title-inline-block'):
                name = stations.h3.text
                if name in ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]:
                    station_name, items = get_station_items(stations)
                    if items:
                        data['dinner'].append({'name': station_name, 'items': items})

    print(json.dumps(data, indent=4))
    return data

# Call the function to execute the scraping and printing
scrape_menu()