from flask import Flask, render_template
from datetime import datetime # Keep datetime if needed elsewhere, but not for meal period logic here
from scrape_menu import scrape_menu
from scrape_weather import get_weather

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    weather_data = get_weather()
    menu_data = scrape_menu()  # Get the full menu data
    # Pass the full menu dictionary and weather data
    return render_template('index.html',
                           weather=weather_data,
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
    app.run(debug=True)