import pandas as pd
import numpy as np

# Read original data to understand patterns
original_df = pd.read_csv('football.csv')

# Define possible values for each feature
weather_options = ['Sunny', 'Cloudy', 'Rainy']
temperature_options = ['Hot', 'Warm', 'Cool', 'Mild']
humidity_options = ['High', 'Normal', 'Low']

# Generate more combinations
n_samples = 100  # You can adjust this number
data = []

for _ in range(n_samples):
    weather = np.random.choice(weather_options)
    temperature = np.random.choice(temperature_options)
    humidity = np.random.choice(humidity_options)
    
    # Logic for determining if football should be played
    play_football = 'Yes'
    
    # Unfavorable conditions
    if (temperature == 'Hot' and humidity == 'High'):
        play_football = 'No'
    elif (weather == 'Rainy' and temperature == 'Cool'):
        play_football = 'No'
    elif (humidity == 'High' and temperature == 'Cool'):
        play_football = 'No'
    
    data.append([weather, temperature, humidity, play_football])

# Create new dataframe
new_df = pd.DataFrame(data, columns=['Weather', 'Temperature', 'Humidity', 'Play Football?'])

# Combine with original data
combined_df = pd.concat([original_df, new_df], ignore_index=True)

# Remove duplicates
combined_df = combined_df.drop_duplicates()

# Save the expanded dataset
combined_df.to_csv('football_expanded.csv', index=False)
print(f"Generated dataset with {len(combined_df)} samples") 