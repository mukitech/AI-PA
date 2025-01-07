from flask import Flask, render_template, request, jsonify
import openai
import requests

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = 'your_openai_api_key'

# OpenWeather API Key (For weather feature)
WEATHER_API_KEY = 'your_openweathermap_api_key'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Chatbot function to interact with OpenAI's GPT model
def generate_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# Weather function
def get_weather(city):
    try:
        complete_url = f"{BASE_URL}q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temperature = main["temp"]
            return f"Weather in {city}: {temperature}°C, {weather_description}"
        else:
            return "City not found!"
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    if 'weather' in user_message.lower():
        # Extract city name (a very simple method)
        city_name = user_message.split('in')[-1].strip()
        weather_response = get_weather(city_name)
        return jsonify({'response': weather_response})
    else:
        assistant_response = generate_response(user_message)
        return jsonify({'response': assistant_response})

if __name__ == '__main__':
    app.run(debug=True)
