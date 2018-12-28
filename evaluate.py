# /usr/bin/python3

from sys import argv
import gzip
import json

def fmeasure(beta, precision, recall):
    if precision + recall != 0.0:
        return (1 + beta * beta) * precision * recall / (beta * beta * precision + recall)
    else:
        return 0.0

occupations = ['Q82955', 'Q937857', 'Q36180', 'Q33999', 'Q1650915', 'Q1028181', 'Q1930187', 'Q177220', 'Q1622272', 'Q49757', 'Q36834', 'Q40348', 'Q47064', 'Q639669', 'Q10800557', 'Q201788', 'Q2526255', 'Q43845', 'Q28389', 'Q42973', 'Q10871364', 'Q39631', 'Q193391', 'Q482980', 'Q483501', 'Q11513337', 'Q3665646', 'Q12299841', 'Q19204627', 'Q16533', 'Q81096', 'Q11774891', 'Q188094', 'Q1281618', 'Q333634', 'Q189290', 'Q250867', 'Q33231', 'Q2259451', 'Q42603', 'Q628099', 'Q37226', 'Q2309784', 'Q901', 'Q2066131', 'Q6625963', 'Q10798782', 'Q2374149', 'Q170790', 'Q4610556', 'Q185351', 'Q486748', 'Q3055126', 'Q753110', 'Q4964182', 'Q169470', 'Q158852', 'Q1234713', 'Q14089670', 'Q10873124', 'Q3282637', 'Q593644', 'Q947873', 'Q13414980', 'Q131524', 'Q11338576', 'Q15117302', 'Q488205', 'Q14467526', 'Q183945', 'Q10843402', 'Q13382576', 'Q13141064', 'Q214917', 'Q855091', 'Q644687', 'Q19595175', 'Q121594', 'Q2865819', 'Q16010345', 'Q1231865', 'Q2405480', 'Q350979', 'Q3400985', 'Q13365117', 'Q10833314', 'Q3621491', 'Q15981151', 'Q212980', 'Q16145150', 'Q1792450', 'Q15296811', 'Q15627169', 'Q2306091', 'Q4263842', 'Q806798', 'Q5716684', 'Q2516866', 'Q3387717', 'Q131512']
occupations = frozenset(occupations)

if len(argv) != 4:
    print("Usage : evaluation.py goldstandard student debug")
    exit()

goldstandard_file = argv[1]
student_file = argv[2]
if argv[3] == "1":
    debug = True
else:
    debug = False

# Dictionaries
goldstandard = dict()
student = dict()

def readFile(filename, result, key):
    with gzip.open(filename, 'rt') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'title' not in data:
                    raise ValueError("'title' key missing in: %s" % line)
                if key == 'prediction' and 'prediction' not in data:
                    raise ValueError("'prediction' key missing in: %s" % line)
                if key != 'prediction' and debug:
                    result[data['title']] = frozenset()
                    continue
                if not hasattr(data[key], '__iter__'):
                    raise ValueError('%s object is not iterable' % key)
                oc = frozenset(data[key])
                if not oc <= occupations:
                    raise ValueError('invalid occupation(s): %s' % str(oc - occupations))
                result[data['title']] = oc
            except:
                if debug:
                    raise
                else:
                    continue

readFile(goldstandard_file, goldstandard, 'occupations')
readFile(student_file, student, 'prediction')

precision = 0.
recall = 0.
accuracy = 0.

if debug:
    for key in student:
        if key not in goldstandard:
            raise ValueError("'%s' article in answer but not in test set" % key)
    print("Correctly read %d predictions on %d examples" % (len(student), len(goldstandard)))
else:
    for key in student:
        if key in goldstandard:
            tp = len(student[key] & goldstandard[key])
            if tp:
                accuracy += 1.*tp / len(student[key] | goldstandard[key])
                precision += 1.*tp / len(student[key])
                recall += 1.*tp / len(goldstandard[key])
    accuracy /= len(goldstandard)
    recall /= len(goldstandard)
    precision /= len(student)
    f1 = fmeasure(1, precision, recall)
    grade = accuracy

    print("Comment :=>> Correctly read %d predictions on %d examples" % (len(student), len(goldstandard)))
    print("Comment :=>>", "Precision:", precision)
    print("Comment :=>>", "Recall:", recall)
    print("Comment :=>>", "F1:", f1)
    print("Comment :=>>", "Grade:", grade)
    print("Grade :=>>", grade)
