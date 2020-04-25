import pickle
from sklearn import svm
import re
import numpy as np
import csv
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

f = open('trainedModel','rb')

model = pickle.load(f)

x = []
y = []

lines = [line.strip() for line in open('preprocessedData/test.tsv')]
f = open('LIWC2015_testData_clean.csv','r')
f2 = open('preprocessedData/test_pickleData','rb')
csvreader = csv.reader(f)
for line in lines:
    row = re.split(r'\t', line)
    intRow = [int(item) for item in row]

    #text_vector = [float(item) for item in next(csvreader)]
    text_vector = list(pickle.load(f2)[0])

    #curX = intRow[1:] + text_vector
    curX = intRow[3:10] + text_vector
    #curX = text_vector
    curY = intRow[0]

    x.append(curX)
    y.append(curY)

f.close()

print('got data')

predictedY = model.predict(x)

totalY = len(y)
correctY = 0

predictedCounts = dict()

for i in range(0,totalY):
    curY = y[i]
    curPredictedY = predictedY[i]
    if curPredictedY not in predictedCounts:
        predictedCounts[curPredictedY] = 0
    predictedCounts[curPredictedY] = predictedCounts[curPredictedY] + 1
    # if curY != curPredictedY:
    #     print("curY: " + str(curY))
    #     print("predictedY: " + str(curPredictedY))
    #     break
    if curY == curPredictedY:
        correctY = correctY + 1

print("predicted counts: " + str(predictedCounts))

print("total: " + str(totalY))
print("correct: " + str(correctY))

accuracy = accuracy_score(y,predictedY)
f1 = f1_score(y,predictedY,average='weighted')

print("Accuracy: " + str(accuracy))
print("F1 Score: " + str(f1))

print("Done!")
