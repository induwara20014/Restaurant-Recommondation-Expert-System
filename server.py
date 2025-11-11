from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pyswip import Prolog
import os

app = Flask(__name__)
CORS(app)

# Initialize Prolog
prolog = Prolog()
prolog.consult("restaurant.pl")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    style = data.get('style')
    taste = data.get('taste')
    budget = data.get('budget')
    type_ = data.get('type')

    # Query Prolog for recommendations
    query = f"findall(Restaurant, restaurant(Restaurant, {style}, {taste}, {budget}, {type_}), RestaurantList)"
    result = list(prolog.query(query))
    
    if result and result[0]['RestaurantList']:
        restaurants = result[0]['RestaurantList']
        return jsonify({'restaurants': restaurants})
    else:
        return jsonify({'restaurants': []})

if __name__ == '__main__':
    # Serve static files from the current directory
    app.static_folder = '.'
    app.run(debug=True)