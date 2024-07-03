from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

PORT = int(os.getenv('PORT', 3000))
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/api/hello', methods=['GET'])
def get_ip():
    try:
        client_ip = request.headers.get('X-Forwarded-For', '').split(',')[0]
        visitor_name = request.args.get('visitor_name', 'Guest')

        # Get location data using the IP
        nap_response = requests.get(f'https://ipapi.co/{client_ip}/json/')
        nap_response.raise_for_status()
        data = nap_response.json()
        ip = data.get('ip', 'Unknown IP')
        city = data.get('city', 'Unknown City')

        # Get weather data for the city
        weather_response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['current']['temp_c']

        greeting = f"Hello {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"

        return jsonify({
            'client_ip': ip,
            'location': city,
            'greeting': greeting
        })
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
