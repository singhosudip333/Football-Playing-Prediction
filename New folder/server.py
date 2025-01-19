from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')

le_weather = joblib.load('le_weather.pkl')
le_temperature = joblib.load('le_temperature.pkl')
le_humidity = joblib.load('le_humidity.pkl')
le_play = joblib.load('le_play.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    weather = request.form.get('weather')
    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')

    data = [[le_weather.transform([weather])[0], le_temperature.transform([temperature])[0], le_humidity.transform([humidity])[0]]]
    prediction = model.predict(data)
    result = le_play.inverse_transform(prediction)[0]

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
