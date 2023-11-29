from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
import os
import random

def labelType(val):
    if val == 1:
        return "Helpful"
    else:
        return "Misleading"


HELPFUL_DATASET_PATH = "D:/IS/infozilla-master/infozilla-master/demo/AspectJ/st_filenames/Top-1/Helpful/"
MISLEADING_DATASET_PATH = "D:/IS/infozilla-master/infozilla-master/demo/AspectJ/st_filenames/Top-1/Misleading/"

helpful_file_count = 0
misleading_file_count = 0
for filename in os.listdir(HELPFUL_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(HELPFUL_DATASET_PATH+filename,'r+')
        for line in file:
            if line != "\n":
                helpful_file_count += 1
        file.close()

for filename in os.listdir(MISLEADING_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(MISLEADING_DATASET_PATH+filename,'r+')
        for line in file:
            if line != "\n":
                misleading_file_count += 1
        file.close()
min_count = min(helpful_file_count,misleading_file_count)
print("minimum",min_count)
X=[]
y=[]
documents = []
for filename in os.listdir(HELPFUL_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(HELPFUL_DATASET_PATH+filename,'r+')
        for line in file.readlines():
            if len(documents) < min_count:
                feature,label=line.split(sep=',')
                documents.append((feature,1))
            else:
                break


for filename in os.listdir(MISLEADING_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(MISLEADING_DATASET_PATH+filename,'r+')
        for line in file.readlines():
            if len(documents) < (2*min_count):
                feature,label=line.split(sep=',')
                documents.append((feature,0))
            else:
                break

print(len(documents))
random.shuffle(documents)

for doc in documents:
    X.append(doc[0])
    y.append(doc[1])

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3,random_state=10)

tf_vectorizer = CountVectorizer()

X_train_tf = tf_vectorizer.fit_transform(X_train)


print("n_samples: %d, n_features: %d" % X_train_tf.shape)

X_test_tf = tf_vectorizer.transform(X_test)
print("n_samples: %d, n_features: %d" % X_test_tf.shape)

naive_bayes_classifier=MultinomialNB()
naive_bayes_classifier.fit(X_train_tf, y_train)
y_pred = naive_bayes_classifier.predict(X_test_tf)

print("Index : class name : Actual label : Predicted Label")

false_positives = []
false_negatives = []
for i in range(1,len(X_test)):
    if y_test[i] != y_pred[i]:
        #print(f'{i}:{X_test[i]}:{labelType(y_test[i])}:{labelType(y_pred[i])}')
        if y_pred[i]:
            false_positives.append([X_test[i],labelType(y_test[i]),labelType(y_pred[i])])
        else:
            false_negatives.append([X_test[i],labelType(y_test[i]),labelType(y_pred[i])])

print(len(false_positives),len(false_negatives))
print(y_pred)

score = metrics.accuracy_score(y_test, y_pred)
print("Accuracy: %.2f" % score)
print("Precision: %.2f" %metrics.precision_score(y_test, y_pred))
print("Recall: %.2f" %metrics.recall_score(y_test, y_pred))
print("F1 Score: %.2f" %metrics.f1_score(y_test, y_pred))


tn, fp, fn, tp =  metrics.confusion_matrix(y_test, y_pred).ravel()
print("Confusion Matrix(tn, fp, fn, tp) :", tn, fp, fn, tp )
