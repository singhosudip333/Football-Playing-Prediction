import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define base path
BASE_PATH = r"C:\Users\HP\Football-Playing-Prediction\New folder"

# Load and preprocess data
df = pd.read_csv(os.path.join(BASE_PATH, "football.csv"))
df.columns = ['Weather', 'Temperature', 'Humidity', 'Play Football?']
print("Dataset Shape:", df.shape)
print("\nFeature Distribution:")
print(df.describe())

# Encode categorical variables
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

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Perform cross-validation with base model
base_model = RandomForestClassifier(random_state=42)
cv_scores = cross_val_score(base_model, X_train, y_train, cv=5)
print("\nCross-validation scores:", cv_scores)
print("Average CV Score: {:.2f} (+/- {:.2f})".format(cv_scores.mean(), cv_scores.std() * 2))

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), 
                         param_grid=param_grid,
                         cv=5,
                         n_jobs=-1,
                         verbose=1)

grid_search.fit(X_train, y_train)

print("\nBest parameters:", grid_search.best_params_)
print("Best cross-validation score: {:.2f}".format(grid_search.best_score_))

# Train final model with best parameters
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

# Model Evaluation
y_pred = best_model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature Importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_model.feature_importances_
})
feature_importance = feature_importance.sort_values('importance', ascending=False)
print("\nFeature Importance:")
print(feature_importance)

# Create visualizations
plt.figure(figsize=(15, 5))

# 1. Confusion Matrix
plt.subplot(131)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

# 2. Feature Importance Plot
plt.subplot(132)
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Feature Importance')
plt.xlabel('Importance Score')

# 3. ROC Curve
plt.subplot(133)
y_pred_proba = best_model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(BASE_PATH, 'model_evaluation.png'))
plt.close()

# Save the best model and encoders
joblib.dump(best_model, os.path.join(BASE_PATH, 'model.pkl'))
joblib.dump(le_weather, os.path.join(BASE_PATH, 'le_weather.pkl'))
joblib.dump(le_temperature, os.path.join(BASE_PATH, 'le_temperature.pkl'))
joblib.dump(le_humidity, os.path.join(BASE_PATH, 'le_humidity.pkl'))
joblib.dump(le_play, os.path.join(BASE_PATH, 'le_play.pkl'))

print("\nModel and visualizations have been saved!")
