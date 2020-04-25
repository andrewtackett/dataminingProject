import json
import re

files = ['test','valid','train']
#files = ['mytest']

#['13270.json', 0
# 'barely-true', 1
# 'We know that more than half of Hillary Clintons meetings while she was secretary of state were given to major contributors to the Clinton Foundation.', 2
# 'foreign-policy', 3
# 'mike-pence', 4
# 'Governor', 5
# 'Indiana', 6
# 'republican', 7
# '8', 8
# '10', 9
# '12', 10
# '5', 11
# '0', 12
# 'comments on "Meet the Press"'] 13

classLabelSet = set()
subjectSet = set()
speakerSet = set()
speakerJobSet = set()
stateSet = set()
speakerPartySet = set()
contextSet = set()

allSets = [(classLabelSet,'classLabel'), (subjectSet,'subject'), (speakerSet,'speaker'), (speakerJobSet,'speakerJob'), (stateSet,'state'), (speakerPartySet,'speakerParty'), (contextSet,'context')]

def convertToLabels(inputSet):
    size = len(inputSet)
    output = dict()
    for i in range(0,size):
        nextSymbol = inputSet.pop()
        output[nextSymbol] = i
    return output

for file in files:
    print("now preprocessing: " + str(file))
    lines = [line.strip() for line in open(file + '.tsv')]
    curRow = 1
    for line in lines:
        row = re.split(r'\t', line)
        if curRow % 500 == 0:
            print('curRow #: ' + str(curRow))
        #id = row[0]
        classLabel = row[1]
        rawText = row[2]
        subject = row[3]
        speaker = row[4]
        speakerJob = row[5]
        state = row[6]
        speakerParty = row[7]
        barelyTrue = row[8]
        falseOutcome = row[9]
        halfTrue = row[10]
        mostlyTrue = row[11]
        pantsOnFire = row[12]
        if len(row) >= 14:
            context = row[13]
        else:
            context = ''

        classLabelSet.add(classLabel)
        subjectSet.add(subject)
        speakerSet.add(speaker)
        speakerJobSet.add(speakerJob)
        stateSet.add(state)
        speakerPartySet.add(speakerParty)
        contextSet.add(context)
        curRow = curRow + 1

for curSet,curLabel in allSets:
     labels = convertToLabels(curSet)
     with open('labelData/' + curLabel + '_label_dict','w') as file:
         file.write(json.dumps(labels))

print("Done!")
