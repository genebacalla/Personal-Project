import build 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn import metrics
import numpy as np
import preprocess
import joblib
import os



# build.dataset()

train_path = "dataset/train/"
test_path = "dataset/test"

labels = []
data = []

for filename in ["Buff.txt","Nerf.txt","Rework.txt"]:
    with open(os.path.join(train_path, filename), 'r', encoding='utf-8') as file:
        phrases = file.readlines()
        labels.extend([filename.split('.')[0]] * len(phrases))
        data.extend(phrases)

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(data)

x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size=0.2,random_state=42)

param_grid = {
        'C': [100], 
        'gamma': [0.1],
        'kernel': ['rbf']} 

svm_model = GridSearchCV(SVC(), param_grid, refit = True, verbose = 0)
svm_model.fit(x_train,y_train)


print("MODEL INITIAL EVALUATION")
y_pred = svm_model.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
precision = metrics.precision_score(y_test, y_pred, average='weighted')
recall = metrics.recall_score(y_test, y_pred, average='weighted')
f1 = metrics.f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(svm_model.best_params_)
print("\n")

joblib.dump(svm_model,"model.joblib")
joblib.dump(vectorizer,"vector.pkl")
svm_model = joblib.load("model.joblib")
vectorizer = joblib.load("vector.pkl")

for filename in ["Buff.txt","Nerf.txt","Rework.txt"]:
    with open(os.path.join(test_path, filename), 'r', encoding='utf-8') as file:
        phrases = file.readlines()
        labels.extend([filename.split('.')[0]] * len(phrases))
        data.extend(phrases)

print("ACTUAL TEST EVALUATION")
x = vectorizer.transform(data)

pred = svm_model.predict(x)
accuracy = metrics.accuracy_score(labels, pred)
precision = metrics.precision_score(labels, pred, average='weighted')
recall = metrics.recall_score(labels, pred, average='weighted')
f1 = metrics.f1_score(labels, pred, average='weighted')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")