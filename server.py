from flask import Flask, request, jsonify, render_template
import joblib
import os
import numpy as np

app = Flask(__name__)

BASE_PATH = r"C:\Users\HP\Football-Playing-Prediction\New folder"

# Load model and encoders
model = joblib.load(os.path.join(BASE_PATH, 'model.pkl'))
le_weather = joblib.load(os.path.join(BASE_PATH, 'le_weather.pkl'))
le_temperature = joblib.load(os.path.join(BASE_PATH, 'le_temperature.pkl'))
le_humidity = joblib.load(os.path.join(BASE_PATH, 'le_humidity.pkl'))
le_play = joblib.load(os.path.join(BASE_PATH, 'le_play.pkl'))

def get_explanation(weather, temperature, humidity, prediction):
    if prediction == "Yes":
        if humidity == "Normal":
            return "With normal humidity, conditions are generally good for playing football."
        else:  # High humidity
            if temperature == "Warm":
                return "Although humidity is high, warm temperature makes it acceptable for playing."
            else:
                return "Despite high humidity, other conditions are favorable for playing."
    else:  # prediction == "No"
        if humidity == "High":
            if temperature == "Cool":
                return "Cool temperature combined with high humidity is not ideal for playing."
            elif temperature == "Hot":
                return "Hot temperature with high humidity creates uncomfortable conditions for playing."
        return "The combination of weather conditions is not favorable for playing football."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        weather = request.form.get('weather')
        temperature = request.form.get('temperature')
        humidity = request.form.get('humidity')
        
        print(f"Received input - Weather: {weather}, Temperature: {temperature}, Humidity: {humidity}")
        
        # Transform inputs
        try:
            weather_encoded = le_weather.transform([weather])[0]
            temperature_encoded = le_temperature.transform([temperature])[0]
            humidity_encoded = le_humidity.transform([humidity])[0]
            
            print(f"Encoded values - Weather: {weather_encoded}, Temperature: {temperature_encoded}, Humidity: {humidity_encoded}")
            
            # Make prediction
            data = [[weather_encoded, temperature_encoded, humidity_encoded]]
            prediction = model.predict(data)
            result = le_play.inverse_transform(prediction)[0]
            
            # Get explanation
            explanation = get_explanation(weather, temperature, humidity, result)
            
            print(f"Prediction result: {result}")
            print(f"Explanation: {explanation}")
            
            return jsonify({
                'prediction': result,
                'explanation': explanation,
                'success': True
            })
            
        except ValueError as e:
            print(f"Error in encoding: {str(e)}")
            return jsonify({
                'error': 'Invalid input values. Please check your selections.',
                'details': str(e),
                'success': False
            }), 400
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({
            'error': 'An error occurred while making the prediction.',
            'details': str(e),
            'success': False
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
