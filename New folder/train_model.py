import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib



df = pd.read_csv("football.csv")
df.columns = ['Weather', 'Temperature', 'Humidity', 'Play Football?']
print(df.columns)



le_weather = LabelEncoder()
le_temperature = LabelEncoder()
le_humidity = LabelEncoder()
le_play = LabelEncoder()

df['Weather'] = le_weather.fit_transform(df['Weather'])
df['Temperature'] = le_temperature.fit_transform(df['Temperature'])
df['Humidity'] = le_humidity.fit_transform(df['Humidity'])
df['Play Football?'] = le_play.fit_transform(df['Play Football?'])

X = df[['Weather', 'Temperature', 'Humidity']]
y = df['Play Football?']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, 'model.pkl')
joblib.dump(le_weather, 'le_weather.pkl')
joblib.dump(le_temperature, 'le_temperature.pkl')
joblib.dump(le_humidity, 'le_humidity.pkl')
joblib.dump(le_play, 'le_play.pkl')
