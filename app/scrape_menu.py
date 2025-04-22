# scrape_menu.py
import requests
from bs4 import BeautifulSoup
import json
import re
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# _scrape_structured_menu function remains the same as provided previously
# ... (Keep the existing _scrape_structured_menu function here) ...
def _scrape_structured_menu(url, target_stations):
    """
    Internal function to scrape menu data and organize by meal period/station.
    (This is the function from the previous step, kept private)

    Args:
        url (str): The URL of the print menu page.
        target_stations (list): A list of station names (case-insensitive) to scrape.

    Returns:
        dict: A dictionary representing the structured menu data, or an empty dict on error.
              Example: {'BREAKFAST': {'Station1': [{'meal': 'MealA', 'description': 'DescA'}, ...], ...}, ...}
    """
    normalized_target_stations = set(
        re.sub(r'[^a-z0-9]', '', station.lower()) for station in target_stations
    )

    structured_menu = {}
    current_meal_period = "Unknown Meal Period"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logging.info(f"Successfully fetched URL: {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve URL {url}: {e}")
        return {} # Return empty dict on error

    soup = BeautifulSoup(response.content, 'html.parser')
    menu_content_area = soup.find('div', id='menu-items') or soup.find('div', class_='main daily')

    if not menu_content_area:
        logging.warning("Could not find the main menu content area on the page.")
        return {}

    potential_elements = menu_content_area.select('.daypart, .row.even, .row.odd')
    if not potential_elements:
         potential_elements = menu_content_area.find_all('div', recursive=False)
         logging.info(f"Using fallback to find elements, found: {len(potential_elements)}")


    for element in potential_elements:
        is_daypart = 'daypart' in element.get('class', [])
        day_spacer = element.find('div', class_='spacer day') if is_daypart else None
        if day_spacer:
            current_meal_period = day_spacer.get_text(strip=True)
            logging.debug(f"Found Meal Period: {current_meal_period}")
            continue

        is_row = 'row' in element.get('class', [])
        if is_row:
            station_span = element.find('span', class_='stationname')
            if not station_span:
                continue

            station_name = station_span.get_text(strip=True)
            normalized_station = re.sub(r'[^a-z0-9]', '', station_name.lower())

            if normalized_station in normalized_target_stations:
                logging.debug(f"Processing target station: {station_name} under {current_meal_period}")
                if current_meal_period not in structured_menu:
                    structured_menu[current_meal_period] = {}
                if station_name not in structured_menu[current_meal_period]:
                    structured_menu[current_meal_period][station_name] = []

                description_div = element.find('div', class_='description')
                if not description_div:
                    continue

                items = description_div.find_all('div', class_='item')
                for item in items:
                    p_tag = item.find('p')
                    if not p_tag:
                        continue

                    meal_name = "Unknown Item"
                    strong_tag = p_tag.find('strong')
                    text_content = p_tag.get_text(separator=' ', strip=True)

                    if strong_tag:
                         meal_name = strong_tag.get_text(strip=True)
                         meal_name = re.split(r'\s*\|', meal_name, 1)[0].strip()
                    elif text_content:
                         meal_name = re.split(r'\s*(?:<span class="cafeCorIcons">|<div class="price">|\|)', text_content, 1)[0].strip()
                         meal_name = re.split(r'\s*\|', meal_name, 1)[0].strip()

                    description = None
                    sides_span = p_tag.find('span', class_='sides collapsed')
                    if sides_span:
                        desc_text = sides_span.get_text(strip=True)
                        desc_text = re.sub(r'^(with|side:)\s+', '', desc_text, flags=re.IGNORECASE)
                        description = desc_text if desc_text else None
                    elif meal_name != "Unknown Item":
                         potential_desc = text_content.replace(meal_name, '', 1).strip()
                         potential_desc = re.split(r'\s*(?:<span class="cafeCorIcons">|<div class="price">)', potential_desc, 1)[0].strip()
                         potential_desc = re.sub(r'^\s*[\|-]\s*', '', potential_desc).strip()
                         potential_desc = re.sub(r'^(with|side:)\s+', '', potential_desc, flags=re.IGNORECASE)
                         if potential_desc and len(potential_desc) > 2 and potential_desc.lower() != meal_name.lower():
                             description = potential_desc

                    if meal_name != "Unknown Item":
                         structured_menu[current_meal_period][station_name].append({
                             "meal": meal_name,
                             "description": description
                         })

    if not structured_menu:
        logging.warning("Scraping finished, but no items found for target stations.")
    else:
        logging.info(f"Scraping finished. Found data for meal periods: {list(structured_menu.keys())}")

    return structured_menu


def get_menu_data_for_template():
    """
    Public function to fetch and transform menu data for the Flask template.
    Filters out specific unwanted meal options during transformation.
    """
    URL = "https://legacy.cafebonappetit.com/print-menu/cafe/17/menu/545346/days/today/pgbrks/0/"
    TARGET_STATIONS = ["Kettle", "Chefs Table", "CHEF'S TABLE", "6th st grill", "6TH ST. GRILL", "home cookin", "HOME COOKIN'", "Pizzeria"]

    # Define the specific meal text to filter out (case-insensitive)
    unwanted_meal_text = "vegan and made without gluten pizza available upon request"

    scraped_data = _scrape_structured_menu(URL, TARGET_STATIONS)
    template_data = {'breakfast': [], 'lunch': [], 'dinner': []}

    if not scraped_data:
        logging.warning("No data scraped, returning empty structure for template.")
        return template_data

    for meal_period, stations in scraped_data.items():
        period_key = meal_period.lower()
        if period_key in template_data:
            logging.debug(f"Transforming data for meal period: {period_key}")
            for station_name, meal_items in stations.items():

                # Extract meal names, applying the filter
                meal_options = [
                    item['meal']
                    for item in meal_items
                    if item.get('meal')                           # Ensure meal key exists
                    and item['meal'] != "Unknown Item"             # Exclude placeholder items
                    # --- Add filter condition ---
                    and item['meal'].lower().strip() != unwanted_meal_text
                ]

                if meal_options:
                    template_data[period_key].append({
                        'name': station_name,
                        'options': meal_options
                    })
                    logging.debug(f"Added Station: {station_name} with options: {meal_options} to {period_key}")
        else:
             logging.warning(f"Skipping transformation for unknown meal period: {meal_period}")


    logging.info("Menu data transformation complete.")
    return template_data

# --- Main execution block for testing ---
if __name__ == '__main__':
    print("Testing scrape_menu module with filtering...")
    menu_for_template = get_menu_data_for_template()
    print("\n--- Data for Template (Filtered) ---")
    print(json.dumps(menu_for_template, indent=4))