import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

import json
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_weather():
    # Send a GET request to the webpage
    source = requests.get('https://www.biola.edu/academics/physics/weather/').text
    soup = BeautifulSoup(source, 'lxml')

    # Initialize a dictionary to store the temperature
    data = {
        'temperature': [],
    }

    # Find the element containing the temperature value (assuming the color="#3366FF" is correct)
    temperature = soup.find('font', color="#3366FF").text.strip()

    # Append the temperature data to the dictionary
    data['temperature'].append({'temperature': temperature,})

    # Return the data dictionary containing the temperature
    return data

# Example of calling the function
weather_data = get_weather()
print(weather_data)

