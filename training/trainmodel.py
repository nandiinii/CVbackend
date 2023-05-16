import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

import pickle

df = pd.read_csv('train.csv')
le = LabelEncoder()
# convert the 'gender' column into numerical values
df['Gender'] = le.fit_transform(df['Gender'])
X = df.drop(['Personality (Class label)'], axis=1)
X.columns = ['Gender','Age','openness','neuroticism','conscientiousness','agreeableness','extraversion']
y = df['Personality (Class label)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=123, max_depth=25,random_state=42,max_features='sqrt')

cv_scores = cross_val_score(model, X, y, cv=5)
print('Cross-validation Scores: ',cv_scores)

model.fit(X_train, y_train)
filename = 'personality_model.pkl'
pickle.dump(model, open(filename, 'wb'))

model = pickle.load(open('personality_model.pkl','rb'))
y_pred = model.predict(X_test) 
accuracy = accuracy_score(y_test,y_pred)
print('Accuracy:',accuracy)
