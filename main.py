# -*- coding: utf-8 -*-
"""CardiovascularClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jjjd9wuqKdFx_Bdv2AezLKmSR-bXNyeq

***Step-1: Importing Libraries***
"""

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_score, recall_score, f1_score

"""***Step-2: Read CSV file***"""


dataset = pd.read_csv('cdv_train (3).csv')

dataset.head()

dataset.info()

dataset.describe()

"""***Step-3: Data Preprocessing***"""

dataset['age'] = (dataset['age'] / 365).astype('int')

dataset['age'] = dataset['age'].apply(lambda x: int(x))

dataset.head()

dataset.drop('id', axis=1, inplace=True)

dataset.head()

dataset['high'], dataset['low'] = np.where(dataset['low'] > dataset['high'], (dataset['low'], dataset['high']), (dataset['high'], dataset['low']))

def BPCategorize(x,y):
    if x<=120 and y<=80:
        return 'normal'
    elif x<=129 and y<=80:
        return 'elevated'
    elif x<=139 or y<=89:
        return 'high 1'
    elif x<=180 or y<=120:
        return "high 2"
    elif x>180 or y>120:
        return 'high 3'
    else:
        return None

dataset.insert(8, "bp", dataset.apply(lambda row: BPCategorize(row['high'], row['low']), axis=1))
dataset['bp'].value_counts()

dataset.head()

dataset.drop(dataset.query('high >220 or low >180 or high<40 or low<40').index, axis=0, inplace=True)

dataset['bp'] = dataset['bp'].map({'normal':0, 'elevated':1, 'high 1':2, 'high 2':3, 'high 3':4})

dataset.drop(['high', 'low'], axis=1, inplace=True)

dataset.head()

dataset.columns

"""***Step-4:Feature Selection***"""

X = dataset.drop(['cardio'], axis=1)
y = dataset['cardio']

print(X)

print(y)

"""***Step-4: Splitting datset into test and train***"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

print(X_train)

print(X_test)

print(y_train)

print(y_test)

"""***Step-5: Model Training***"""

""
'''
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier()

parameters={'n_neighbors': np.arange(1, 10)}

cv_knn=GridSearchCV(classifier, cv = 5, param_grid = parameters)
cv_knn.fit(X_train,y_train)
'''
from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)

'''
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)
'''

'''
from sklearn.ensemble import RandomForestClassifier
rfclassifier = RandomForestClassifier()
rfclassifier.fit(X_train, y_train)
'''

'''
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(fit_intercept=True, max_iter=10000000)
classifier.fit(X_train,y_train)
'''
'''
from xgboost import XGBClassifier
classifier = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1,n_jobs=4)
classifier.fit(X_train, y_train, early_stopping_rounds=5,
          eval_set=[(X_test, y_test)],
          verbose=False)
'''
from xgboost import XGBClassifier
def model_metrics(y_train, y_test, train_preds, test_preds):
    train_accuracy = accuracy_score(y_train, train_preds)
    test_accuracy = accuracy_score(y_test, test_preds)
    print(f"{'Train Accuracy':<20}{train_accuracy:.4f}")
    print(f"{'Test Accuracy':<20}{test_accuracy:.4f}")
'''
xgb = XGBClassifier()
# Fit the Algorithm
xgb.fit(X_train, y_train)
'''



"""***Step-6: Model Prediction***"""
# Predict on the model
y_train_xgb_pred = xgb.predict(X_train)
y_test_xgb_pred = xgb.predict(X_test)

print(y_train_xgb_pred)
print(y_test_xgb_pred)
"""***Step-7:Model Evaluation***"""
model_metrics(y_train, y_test, y_train_xgb_pred, y_test_xgb_pred)


#Pickling the file
import pickle

pickle.dump(xgb,open('cdv_model.pk1', 'wb'))