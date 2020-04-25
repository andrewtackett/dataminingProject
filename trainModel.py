import json
import re
import numpy as np
import pickle
from sklearn import svm
import csv

x = []
y = []

lines = [line.strip() for line in open('preprocessedData/train.tsv')]
f = open('LIWC2015_trainData_clean.csv','r')
f2 = open('preprocessedData/train_pickleData','rb')

csvreader = csv.reader(f)
for line in lines:
    row = re.split(r'\t', line)
    intRow = [int(item) for item in row]

    #text_vector = [float(item) for item in next(csvreader)]
    text_vector = list(pickle.load(f2)[0])

    #curX = intRow[1:] + text_vector
    #curX = text_vector
    curX = intRow[3:10] + text_vector

    # print(curX)
    # break

    curY = intRow[0]

    x.append(curX)
    y.append(curY)

f.close()

print('fitting model')

clf = svm.SVC(C=1000000.0)
clf.fit(x, y)

f = open('trainedModel','wb')

pickle.dump(clf,f)

print("Done!")