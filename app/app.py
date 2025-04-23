# app.py
from flask import Flask, render_template, request, jsonify # Added request and jsonify
from scrape_menu import get_menu_data_for_template
from scrape_weather import get_weather
from datetime import datetime
import logging # Optional: for logging received ratings

app = Flask(__name__, template_folder='../templates')

# Optional: Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    print("Route '/' accessed") # Keep for debugging if needed
    weather_data = get_weather()
    menu_data = get_menu_data_for_template()
    return render_template('index.html',
                           weather=weather_data,
                           menu=menu_data)

# --- NEW RATING ENDPOINT ---
@app.route('/rate', methods=['POST'])
def handle_rating():
    """Receives meal rating data from the frontend."""
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    meal_name = data.get('meal_name')
    rating = data.get('rating')

    # Basic Validation
    if not meal_name or not isinstance(meal_name, str):
        return jsonify({"status": "error", "message": "Missing or invalid meal_name"}), 400
    if not rating or not isinstance(rating, int) or not (1 <= rating <= 5):
         return jsonify({"status": "error", "message": "Invalid rating value (must be 1-5)"}), 400

    # --- Processing/Storage ---
    # For now, just log the received rating.
    # In a real application, you would:
    # 1. Sanitize meal_name further.
    # 2. Store the rating in a database (e.g., SQLite, PostgreSQL).
    # 3. Calculate the new average rating and count for the meal.
    # 4. Return the new average/count if you want to update the UI dynamically.
    
    logging.info(f"Received rating for '{meal_name}': {rating} stars")
    print(f"Received rating for '{meal_name}': {rating} stars") # Also print to console

    # Simulate successful storage
    # Placeholder: In a real app, you might return updated average/count
    # new_average = calculate_new_average(meal_name, rating) 
    # rating_count = get_rating_count(meal_name)

    return jsonify({
        "status": "success", 
        "message": "Rating received successfully"
        # "new_average_rating": new_average, # Example for future UI update
        # "rating_count": rating_count        # Example for future UI update
        }) 
# --- END NEW RATING ENDPOINT ---

if __name__ == '__main__':
    # Ensure debug is False in production
    app.run(debug=True, host='0.0.0.0', port=5000) # Example: Run on all interfaces