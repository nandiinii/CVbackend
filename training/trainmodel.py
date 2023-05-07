import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

import pickle

df = pd.read_csv('train.csv')
le = LabelEncoder()
# convert the 'gender' column into numerical values
df['Gender'] = le.fit_transform(df['Gender'])
X = df.drop(['Personality (Class label)'], axis=1)
y = df['Personality (Class label)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
filename = 'personality_model.pkl'
pickle.dump(model, open(filename, 'wb'))

