from __future__ import print_function
import random

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from scipy.spatial import distance
import tensorflow as tf
from tensorflow.contrib import learn

      
df = pd.read_csv('/home/sansbacon/qbmodel.csv')
qb = df[(df['AvgPts'] >= 12) & (df['ActualPoints'] >=5)]
qb['gtproj'] = np.where(qb.ActualPoints >= qb.AvgPts * 1.25, 2, np.where(qb.ActualPoints * 1.25 <= qb.AvgPts, 0, 1))
features = qb[qb.columns[0:21]]
labels = qb[qb.columns[22]]
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=21)]

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=.25, random_state=13)
classifier = learn.DNNClassifier(
    hidden_units=[10,20,10], 
    feature_columns=feature_columns, 
    n_classes=3,
)

classifier.fit(x_train, y_train, steps=2000)
score = classifier.evaluate(x=x_test, y=y_test)["accuracy"]
print('Accuracy: {0:f}'.format(score))
