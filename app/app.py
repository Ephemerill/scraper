# app.py
from flask import Flask, render_template
from scrape_menu import get_menu_data_for_template
from scrape_weather import get_weather
from scrape_chapel import get_chapel_events
from datetime import datetime
import pytz  # For handling timezones

app = Flask(__name__,
            template_folder='../templates')

@app.route('/')
def home():
    print("Route '/' accessed")
    weather_data = get_weather()
    menu_data = get_menu_data_for_template()
    
    # --- Filter chapel events to show only future ones ---
    all_chapel_events = get_chapel_events()
    pacific_tz = pytz.timezone('America/Los_Angeles')
    now = datetime.now(pacific_tz)
    
    future_events = []
    
    for event in all_chapel_events:
        time_str = event.get('time', '')
        if not time_str:
            continue
            
        try:
            cleaned_time_str = " ".join(time_str.split())
            event_dt_template = datetime.strptime(cleaned_time_str, "%a, %b %d, %I:%M %p")
            
            event_year = now.year
            if event_dt_template.month < now.month:
                event_year = now.year + 1
            
            event_dt_naive = event_dt_template.replace(year=event_year)
            event_dt = pacific_tz.localize(event_dt_naive)
            
            if event_dt >= now:
                time_delta = event_dt - now
                total_seconds = time_delta.total_seconds()
                
                # If it's less than a full day away, show hours
                if total_seconds < 86400:
                    if total_seconds < 3600:  # Less than 1 hour
                        event['countdown_value'] = "<1"
                        event['countdown_unit'] = "hour"
                    else: # 1 to 23 hours
                        hours = int(total_seconds // 3600)
                        event['countdown_value'] = hours
                        event['countdown_unit'] = "hour" if hours == 1 else "hours"
                # If it's one day or more away, calculate days by rounding
                else:
                    # FIX: Round the total seconds to the nearest day
                    days = round(total_seconds / 86400)
                    # Safeguard in case rounding results in 0
                    if days < 1:
                        days = 1
                    
                    event['countdown_value'] = int(days)
                    event['countdown_unit'] = "day" if days == 1 else "days"
                
                future_events.append(event)
                
        except ValueError:
            print(f"Could not parse chapel event time: '{time_str}'")
            continue

    return render_template('index.html',
                           weather=weather_data,
                           menu=menu_data,
                           chapel=future_events)

if __name__ == '__main__':
    app.run(debug=True)