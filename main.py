from build_dataset import BuildDataset
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn import metrics
import os


dataset_path = "dataset/"

labels = []
data = []


patch_labels = ["Buff","Nerf","Rework"]
patch_versions = ["7.35","7.34","7.33","7.32"]


# for patch_ver in (patch_versions):
#     patch = BuildDataset(patch_ver)
#     for patch_lab in (patch_labels):
#         patch.build_data(patch_lab)


for filename in ["Buff.txt","Nerf.txt","Rework.txt"]:
    with open(os.path.join(dataset_path, filename), 'r', encoding='utf-8') as file:
        phrases = file.readlines()
        labels.extend([filename.split('.')[0]] * len(phrases))
        data.extend(phrases)



vectorizer = CountVectorizer()
x = vectorizer.fit_transform(data)


x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size=0.2,random_state=42)

param_grid = {
        'C': [0.1, 1, 10, 100, 1000], 
        'gamma': [1, 0.1, 0.01, 0.001, 0.0001,'auto'],
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid']} 

svm_model = GridSearchCV(SVC(),param_grid,refit=True,verbose=0)
svm_model.fit(x_train,y_train)

y_pred = svm_model.predict(x_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
precision = metrics.precision_score(y_test, y_pred, average='weighted')
recall = metrics.recall_score(y_test, y_pred, average='weighted')
f1 = metrics.f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

