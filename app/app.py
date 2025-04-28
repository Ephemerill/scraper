# app.py
from flask import Flask, render_template
from scrape_menu import get_menu_data_for_template
from scrape_weather import get_weather
from datetime import datetime

app = Flask(__name__,
            template_folder='../templates')


@app.route('/')
def home():
    print("Route '/' accessed")
    weather_data = get_weather()
    menu_data = get_menu_data_for_template()
    return render_template('index.html',
                           weather=weather_data,
                           menu=menu_data)


if __name__ == '__main__':
    app.run(debug=True)