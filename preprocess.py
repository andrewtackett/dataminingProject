import pickle
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('bert-base-nli-mean-tokens')

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

dictNames = ['classLabel', 'subject', 'speaker','speakerJob','state','speakerParty','context']

allDicts = dict()

for dictName in dictNames:
    with open('labelData/' + dictName + '_label_dict') as f:
        allDicts[dictName] = json.load(f)

for file in files:
    print("now preprocessing: " + str(file))
    lines = [line.strip() for line in open(file + '.tsv')]
    curRow = 1
    with open('preprocessedData/' + file + '.tsv','w') as f:
        with open('preprocessedData/' + file + '_pickleData','wb') as f2:
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

                classLabel = allDicts['classLabel'][classLabel]
                subject = allDicts['subject'][subject]
                speaker = allDicts['speaker'][speaker]
                speakerJob = allDicts['speakerJob'][speakerJob]
                state = allDicts['state'][state]
                speakerParty = allDicts['speakerParty'][speakerParty]
                context = allDicts['context'][context]

                text_vector = model.encode([rawText])
                #text_vector_string = np.array2string(text_vector[0]).replace('\n','|')
                #text_vector_string = text_vector[0].dumps()

                newRowData = [classLabel,subject,speaker,speakerJob,state,speakerParty,barelyTrue,falseOutcome,halfTrue,mostlyTrue,pantsOnFire,context]

                newRow = "\t".join(str(data) for data in newRowData) + '\n'

                f.write(newRow)

                pickle.dump(text_vector,f2)

                curRow = curRow + 1

print("Done!")
