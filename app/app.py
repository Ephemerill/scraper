# app.py
from flask import Flask, render_template
from scrape_menu import get_menu_data_for_template
from scrape_weather import get_weather
from datetime import datetime

app = Flask(__name__,
            #static_folder='../static',
            template_folder='../templates') # Assumes templates are one level up


@app.route('/')
def home():
    print("Route '/' accessed") # Add print statement for debugging
    weather_data = get_weather()
    # Call the function that gets and transforms the data
    menu_data = get_menu_data_for_template()
    #print(f"Menu data for template: {menu_data}") # Debug print
    # Pass the transformed menu dictionary and weather data
    return render_template('index.html',
                           weather=weather_data,
                           menu=menu_data) # 'menu' variable now holds the correct structure


# --- Keep other routes if they exist ---
# @app.route('/scrape')
# def scrape():
#     # Ensure this route also uses the transformed data if menu.html expects it
#     menu_data = get_menu_data_for_template()
#     # Assuming menu.html expects the same structure as index.html
#     return render_template('menu.html', menu=menu_data)

# @app.route('/assistant')
# def assistant():
#     return render_template('assistant.html')
# --- End other routes ---


if __name__ == '__main__':
    # Consider setting host and port if running not just locally
    # app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True) # Keep simple for local testing