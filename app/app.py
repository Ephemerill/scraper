from flask import Flask, render_template
from datetime import datetime # Keep datetime if needed elsewhere, but not for meal period logic here
from scrape_menu import scrape_menu
from scrape_weather import get_weather

# REMOVE this function
# def get_meal_period():
#     current_time = datetime.now()
#     hour = current_time.hour
#
#     if 7 <= hour < 11:
#         return 'breakfast'
#     elif 11 <= hour < 16:
#         return 'lunch'
#     elif 16 <= hour < 20:
#         return 'dinner'
#     else:
#         # Decide what to do outside main periods - maybe default?
#         # For client-side, we'll likely default to breakfast or lunch
#         return 'breakfast' # Or another default like 'lunch'

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    weather_data = get_weather()
    # REMOVE meal period determination from backend
    # meal_period = get_meal_period()
    menu_data = scrape_menu()  # Get the full menu data

    # Pass the full menu dictionary and weather data
    return render_template('index.html',
                           weather=weather_data,
                           # REMOVE meal_period=meal_period,
                           menu=menu_data)

@app.route('/scrape')
def scrape():
    menu_data = scrape_menu()
    # Assuming menu.html expects the full dictionary too
    return render_template('menu.html', menu=menu_data)

@app.route('/assistant')
def assistant():
    return render_template('assistant.html')


if __name__ == '__main__':
    # Ensure you're running in the correct directory context if needed
    # Example: If templates are in ./templates relative to app.py
    # app = Flask(__name__, template_folder='templates')
    app.run(debug=True)