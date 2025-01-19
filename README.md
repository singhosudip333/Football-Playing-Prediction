# Football Weather Prediction

A machine learning web application that predicts whether it's suitable to play football based on weather conditions.

## Features

- Predicts football playing conditions based on:
  - Weather (Sunny, Cloudy, Rainy)
  - Temperature (Hot, Warm, Mild, Cool)
  - Humidity (High, Normal)
- Provides detailed explanations for predictions
- Interactive web interface with real-time predictions
- Temperature ranges in both Celsius and Fahrenheit
- Detailed weather condition guidelines

## Technology Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript (jQuery)
- Machine Learning: scikit-learn (Random Forest Classifier)
- Data Processing: pandas, numpy

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python server.py
```

4. Open your web browser and go to:
```
http://localhost:5000
```

## Usage

1. Select the current weather condition (Sunny, Cloudy, or Rainy)
2. Choose the temperature range:
   - Hot (Above 30°C / 86°F)
   - Warm (25-30°C / 77-86°F)
   - Mild (18-24°C / 64-75°F)
   - Cool (10-17°C / 50-63°F)
3. Select the humidity level:
   - High (Above 60% RH)
   - Normal (40-60% RH)
4. Click "Get Prediction" to see the result

## Project Structure

```
Football-Playing-Prediction/
├── server.py           # Flask server
├── train_model.py      # ML model training
├── requirements.txt    # Project dependencies
├── football.csv        # Training data
├── model.pkl          # Trained model
├── le_*.pkl           # Label encoders
├── templates/
│   └── index.html     # Main webpage
└── static/
    ├── styles.css     # CSS styling
    └── scripts.js     # Frontend JavaScript
```

## Model Training

The model is trained using a Random Forest Classifier with the following features:
- Weather conditions
- Temperature levels
- Humidity levels

To retrain the model:
```bash
python train_model.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 