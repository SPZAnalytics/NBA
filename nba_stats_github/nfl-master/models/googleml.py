from __future__ import print_function
import random

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from scipy.spatial import distance
import tensorflow as tf
from tensorflow.contrib import learn


def euc(a,b):
    return distance.euclidean(a,b)

class ScrappyKNN(object):
    
    def closest(self, row):
        best_dist = euc(row, self.X_train[0])
        best_index = 0
        for i in range(1, len(self.X_train)):
            dist = euc(row, self.X_train[i])
            if dist < best_dist:
                best_dist = dist
                best_index = i
        return self.y_train[best_index]

    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
        
    def predict(self, X_test):
        return [self.closest(row) for row in X_test]
        
if __name__ == '__main__':
    #iris = load_iris()
    #X = iris.data
    #y = iris.target
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5)
    #clf = ScrappyKNN()
    #clf.fit(X_train, y_train)
    #predictions = clf.predict(X_test)
    #print predictions
    #print accuracy_score(y_test, predictions)
    iris = learn.datasets.load_dataset('iris')
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=.2, random_state=42)
    classifier = learn.DNNClassifier(hidden_units=[10,20,10], feature_columns=feature_columns, n_classes=3)
    classifier.fit(x_train, y_train, steps=1000)
    #score = accuracy_score(y_test, classifier.predict(x_test))
    
    score = classifier.evaluate(x=x_test, y=y_test)["accuracy"]
    print('Accuracy: {0:f}'.format(score))
    
