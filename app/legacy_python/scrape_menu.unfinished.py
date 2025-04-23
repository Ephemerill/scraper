import json
from bs4 import BeautifulSoup, Tag # Import Tag for type checking
import requests
# from datetime import datetime # Not used in this version

# --- Function to process a meal section ---
def process_meal_section(section_soup, meal_type, data, target_stations):
    print(f"\n--- Processing {meal_type.upper()} ---")
    if not section_soup:
        print(f"Warning: Could not find section for {meal_type}")
        return

    # Find the main content area for items
    content_area = section_soup.find('div', class_='c-tab__content', attrs={'data-key-index': '0'})
    if not content_area:
        content_area = section_soup.find('div', class_='site-panel__daypart-tab-content-inner')
        if not content_area:
            content_area = section_soup # Last resort

    if not content_area:
        print(f"Warning: Could not find content area for {meal_type}")
        return

    # Find all potential station titles and item divs within the content area
    elements = content_area.find_all(['div'], class_=['station-title-inline-block', 'site-panel__daypart-item'], recursive=False)
    if not elements:
         print(f"Warning: No station/item elements found directly under content area for {meal_type}. Trying deeper search...")
         elements = content_area.find_all(['div'], class_=['station-title-inline-block', 'site-panel__daypart-item'])
         if not elements:
             print(f"Warning: Still no station/item elements found for {meal_type}.")
             return


    current_station_dict = None

    for element in elements:
        # Check if it's a station title block
        if 'station-title-inline-block' in element.get('class', []):
            # --- Output and Save the PREVIOUS station before starting new one ---
            if current_station_dict and current_station_dict['options']:
                print(f"  Finished Station: '{current_station_dict['name']}'")
                print(f"    Options: {current_station_dict['options']}")
                data[meal_type].append(current_station_dict)
            # --- Reset for the new station ---
            current_station_dict = None # Reset tracker

            h3 = element.find('h3', class_='site-panel__daypart-station-title')
            if h3:
                name = h3.text.strip()
                if name in target_stations:
                    print(f"\n  Found Target Station: '{name}'")
                    # It's a station we care about, initialize its dictionary
                    current_station_dict = {'name': name, 'options': []}
                    # Look for items *inside* this station title div as well
                    items_inside = element.find_all('button', class_='site-panel__daypart-item-title')
                    if items_inside:
                        print(f"    Items inside station block:")
                        for button in items_inside:
                             option = button.text.strip()
                             if option: # Ensure not empty
                                 print(f"      - Adding: {option}")
                                 current_station_dict['options'].append(option)
                else:
                    # It's a station we don't care about
                    print(f"\n  Ignoring Station: '{name}'")
                    current_station_dict = None # Ensure tracker is None
            else:
                 # Malformed station block? Stop tracking
                 print(f"  Found station block without h3 title, ignoring.")
                 current_station_dict = None

        # Check if it's an item block AND we are currently tracking a target station
        elif 'site-panel__daypart-item' in element.get('class', []) and current_station_dict is not None:
            button = element.find('button', class_='site-panel__daypart-item-title')
            if button:
                option = button.text.strip()
                if option: # Ensure not empty
                    print(f"    - Adding Item: {option}")
                    current_station_dict['options'].append(option)

    # --- Output and Save the VERY LAST station found in the section ---
    if current_station_dict and current_station_dict['options']:
        print(f"  Finished Station: '{current_station_dict['name']}'")
        print(f"    Options: {current_station_dict['options']}")
        data[meal_type].append(current_station_dict)

    print(f"--- Finished processing {meal_type.upper()} ---")


def scrape_menu():
    print("Starting menu scrape...")
    url = 'https://cafebiola.cafebonappetit.com/cafe/cafe-biola/'
    print(f"Fetching URL: {url}")

    # Scrape the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        source = response.text
        print("Successfully fetched website content.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return { 'error': f"Failed to fetch menu: {e}" }

    print("Parsing HTML content...")
    soup = BeautifulSoup(source, 'lxml')
    print("HTML parsed.")

    data = {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    }
    target_stations = ["kettle", "home cookin'", "6th st. grill", "pizzeria", "chef's table"]
    print(f"Target stations: {target_stations}")


    # --- Process each meal ---
    process_meal_section(soup.find('section', id='breakfast'), 'breakfast', data, target_stations)
    process_meal_section(soup.find('section', id='lunch'), 'lunch', data, target_stations)
    process_meal_section(soup.find('section', id='dinner'), 'dinner', data, target_stations)

    # Clean up stations with no options (should be less likely now but good practice)
    print("\nCleaning up any empty stations...")
    for meal in data:
        original_count = len(data[meal])
        data[meal] = [station for station in data[meal] if station.get('options')]
        if len(data[meal]) < original_count:
             print(f"Removed {original_count - len(data[meal])} empty station(s) from {meal}.")

    print("\nScraping complete.")
    return data

# --- Example Usage ---
if __name__ == "__main__":
    menu_data = scrape_menu()

    print("\n" + "="*40)
    print("          FINAL SCRAPED DATA")
    print("="*40)
    # Pretty print the JSON output to the terminal
    print(json.dumps(menu_data, indent=2))
    print("="*40)
