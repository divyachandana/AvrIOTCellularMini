import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

# Seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 100000

# Generate simulated data
data = {
    'Temperature (°C)': np.random.uniform(-15, 15, n_samples),  # Between -15°C and 15°C
    'Water Flow (L/min)': np.random.uniform(0, 5, n_samples),  # Between 0 L/min (stagnant) and 5 L/min
    'Pipe Material': np.random.choice(['Copper', 'PVC', 'Steel'], n_samples),  # Types of pipe materials
    'Pipe Insulation': np.random.choice(['None', 'Low', 'High'], n_samples),  # Insulation levels
    'Pipe Diameter (cm)': np.random.uniform(1, 10, n_samples),  # Diameter between 1cm and 10cm
    'Pipe Length (m)': np.random.uniform(1, 100, n_samples),  # Length between 1m and 100m
    'Exposure to Wind': np.random.choice(['Low', 'Moderate', 'High'], n_samples),  # Wind exposure levels
    'Humidity (%)': np.random.uniform(20, 100, n_samples),  # Humidity between 20% and 100%
    'Pipe Location': np.random.choice(['Basement', 'Attic', 'Outside Wall', 'Heated Space'], n_samples),  # Possible locations
    'Air Circulation': np.random.choice(['Poor', 'Moderate', 'Good'], n_samples),  # Air circulation levels
}

df = pd.DataFrame(data)



def determine_freezing_condition_adjusted(row):
    if row['Temperature (°C)'] <= 0 and row['Water Flow (L/min)'] < 0.5 and \
       row['Pipe Insulation'] in ['None', 'Low'] and \
       row['Pipe Location'] in ['Basement', 'Attic', 'Outside Wall'] and \
       row['Air Circulation'] == 'Poor':
        return 1
    else:
        return 0

df['Freeze Condition'] = df.apply(determine_freezing_condition_adjusted, axis=1)


noise_level = 0.05
df['Temperature (°C)'] += np.random.normal(0, noise_level * np.abs(df['Temperature (°C)'].mean()), n_samples)
df['Water Flow (L/min)'] += np.random.normal(0, noise_level * np.abs(df['Water Flow (L/min)'].mean()), n_samples)


flip_percentage = 0.05
indices_to_flip = np.random.choice(df.index, size=int(flip_percentage * len(df)), replace=False)
df.loc[indices_to_flip, 'Freeze Condition'] = 1 - df.loc[indices_to_flip, 'Freeze Condition']


encoder = LabelEncoder()
for col in ['Pipe Material', 'Pipe Insulation', 'Exposure to Wind', 'Pipe Location', 'Air Circulation']:
    df[col] = encoder.fit_transform(df[col])

X = df.drop('Freeze Condition', axis=1)
y = df['Freeze Condition']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy}')


with open('piper.pkl', 'wb') as file:
    pickle.dump(model, file)
