import requests # Library to make HTTP requests
import re      # Regular expression library

# The URL of the page to scrape
target_url = "https://cafebiola.cafebonappetit.com/cafe/cafe-biola/"

# The pattern to find the specific print menu URL
url_pattern = r"https://legacy\.cafebonappetit\.com/print-menu/cafe/17/menu/\d+/days/today/pgbrks/0/"

try:
    # --- Fetching the web page content ---
    # Send an HTTP GET request to the target URL
    # Use a User-Agent header to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(target_url, headers=headers, timeout=10) # Added timeout

    # Raise an exception if the request was unsuccessful (e.g., 404 Not Found, 500 Server Error)
    response.raise_for_status()

    # Get the HTML content from the response
    html_content = response.text

    # --- Finding the URL using regular expression ---
    match = re.search(url_pattern, html_content)

    # --- Extracting and printing the URL ---
    if match:
        extracted_url = match.group(0)
        print(f"Found URL: {extracted_url}")

        # Example of extracting just the menu ID number
        menu_id_match = re.search(r"/menu/(\d+)/days/", extracted_url)
        if menu_id_match:
            menu_id = menu_id_match.group(1)
            print(f"Extracted Menu ID: {menu_id}")
    else:
        print(f"Could not find the URL pattern on the page: {target_url}")

except requests.exceptions.RequestException as e:
    # Handle errors during the web request (e.g., connection error, timeout)
    print(f"Error fetching URL {target_url}: {e}")
except Exception as e:
    # Handle other potential errors
    print(f"An unexpected error occurred: {e}")