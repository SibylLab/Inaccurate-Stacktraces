import os
import nltk.classify.util
import random
from nltk.classify import NaiveBayesClassifier

HELPFUL_DATASET_PATH = "D:/IS/infozilla-master/infozilla-master/demo/Birt/st_filenames/Top-10/Helpful/"
MISLEADING_DATASET_PATH = "D:/IS/infozilla-master/infozilla-master/demo/Birt/st_filenames/Top-10/Misleading/"


def feature_set(word):
    return {word: True}


documents = []
for filename in os.listdir(HELPFUL_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(HELPFUL_DATASET_PATH + filename, 'r+')
        for line in file.readlines():
            feature, label = line.split(sep=',')
            documents.append((feature_set(feature), label.replace('\n', '')))
for filename in os.listdir(MISLEADING_DATASET_PATH):
    if filename.endswith(".txt"):
        file = open(MISLEADING_DATASET_PATH + filename, 'r+')
        for line in file.readlines():
            feature, label = line.split(sep=',')
            documents.append((feature_set(feature), label.replace('\n', '')))

random.shuffle(documents)

limit = int(len(documents) * 0.7)

train_set = documents[:limit]
test_set = documents[limit:]

classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.util.accuracy(classifier, test_set)

print("Accuary for Model(with 70% Training & 30% testing set) is", accuracy * 100)
print("Testing model ", classifier.classify(feature_set('SWT.java')))
