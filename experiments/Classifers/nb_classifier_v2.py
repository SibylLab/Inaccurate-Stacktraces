import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

FILEPATH = "D:/IS/stracktraces/Stack Trace Classification/"

all_features = [["Filename"], ["Filename", "Method name"], ["Filename", "Exception"],
                ["Filename", "Method name", "Exception"]]

astrx = "*" * 30
for filename in os.listdir(FILEPATH):
    if filename.endswith(".csv"):
        file = FILEPATH + filename
        dataset = pd.read_csv(file, encoding='unicode_escape')
        for features in all_features:
            print(filename)
            X = pd.get_dummies(dataset[features])
            print(astrx)
            print("Filename:", filename)
            print("Features:", features)
            X = pd.get_dummies(dataset[features])
            y = dataset['Label'].map(lambda p: 1 if p == "Helpful" else 0)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

            gnb = GaussianNB()
            y_pred = gnb.fit(X_train, y_train).predict(X_test)
            score = metrics.accuracy_score(y_test, y_pred)

            print("Precision: %.2f" % metrics.precision_score(y_test, y_pred))
            print("Recall: %.2f" % metrics.recall_score(y_test, y_pred))
            print("F1 Score: %.2f" % metrics.f1_score(y_test, y_pred))
            print("Accuracy: %.2f" % score)

            tn, fp, fn, tp = metrics.confusion_matrix(y_test, y_pred).ravel()
            print("Confusion Matrix(tn, fp, fn, tp) :", tn, fp, fn, tp)
            print(astrx)
