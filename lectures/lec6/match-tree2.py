import csv
from sklearn import tree
import editdist
import re

def string_match_score(p1,p2,field):
    s1 = p1[field]
    s2 = p2[field]
    return editdist.distance(s1.lower(),s2.lower())/float(len(s1))

def jaccard_score(p1,p2,field):
    name1 = p1[field]
    name2 = p2[field]
    set1 = set(name1.lower().split())
    set2 = set(name2.lower().split())
    c = set1.intersection(set2)
    return float(len(c)) / (len(set1) + len(set2) - len(c))

def price_score(p1,p2,field):
    price1 = p1[field]
    if (len(price1) == 0): return 10000
    price2 = p2[field]
    if (len(price2) == 0): return 10000
    price1 = re.sub('[\$,]', '', price1)
    price2 = re.sub('[\$,]', '', price2)
    price1 = float(price1)
    price2 = float(price2)
    return abs(price1 - price2)

def generate_test_training(m1,m2,gt,fracTraining):
    numTraining = int(len(m1) * fracTraining)
    test1 = []
    training1 = []
    test2 = []
    training2 = []
    test_answers = {}
    training_answers = {}
    m2_map = {}
    for v in m2:
        m2_map[v["id"]] = v

    for i in xrange(0,numTraining):
        training1.append(m1[i])
        training2.append(m2_map[gt[m1[i]["id"]]])
        training_answers[m1[i]["id"]] = gt[m1[i]["id"]]
    for i in xrange(numTraining+1,len(m1)):
        test1.append(m1[i])
        test2.append(m2_map[gt[m1[i]["id"]]])
        test_answers[m1[i]["id"]] = gt[m1[i]["id"]]
    return (training1,training2,training_answers,test1,test2,test_answers)
    

print "Loading Data"

abtReader = csv.DictReader(open("Abt.csv","rU"))
buyReader = csv.DictReader(open("Buy.csv","rU"))
gtLines = csv.DictReader(open("abt_buy_perfectMapping.csv","rU"))
gtBuyMap = {}
gtAbtMap = {}
abtAr = []
buyAr = []

for r in abtReader:
    abtAr.append(r)

for r in buyReader:
    buyAr.append(r)

for r in gtLines:
    gtAbtMap[r["idAbt"]] = r["idBuy"]
    gtBuyMap[r["idBuy"]] = r["idAbt"]

print "Splitting into Test and Training"

(tr1,tr2,tr_ans,test1,test2,test_ans) = generate_test_training(buyAr,abtAr,gtBuyMap,.5)

print "Generating Feature Map"

X = []
Y = []
for r1 in tr1:
    bestId = {}
    bestMatch = 0
    bestVal = []
    j = 0
    for r2 in tr2:
        s = jaccard_score(r1,r2,"name")
        s2 = jaccard_score(r1,r2,"description")
        s3 = string_match_score(r1,r2,"name")
        if (s>=bestMatch):
            bestVal=[s,s2,s3]
            bestMatch=s
            bestId = r2
    X.append(bestVal)
    if (tr_ans[r1["id"]] == bestId["id"]):
        Y.append(1)
    else:
        Y.append(-1)

print "Training Classifier"

clf = tree.DecisionTreeClassifier(max_depth=5)
clf = clf.fit(X, Y)
print clf.get_params()
tree.export_graphviz(clf)

print "Testing Classifier"

X = []
idxs = []
i = 0
for r1 in test1:
    j = 0
    bestj = 0
    bestMatch = 0
    bestVal = []
    for r2 in test2:
        s = jaccard_score(r1,r2,"name")
        s2 = jaccard_score(r1,r2,"description")
        s3 = string_match_score(r1,r2,"name")
        if (s >= bestMatch):
            bestVal = [s,s2,s3]
            bestMatch = s
            bestj = j
        j = j + 1
    X.append(bestVal)
    idxs.append((i,bestj))

    i = i + 1

ans = clf.predict(X)


falsePos = 0
truePos = 0
falseNeg = 0
trueNeg = 0

for i in xrange(0,len(ans)):
    (x,y) = idxs[i]
    t1val = test1[x]
    t2val = test2[y]
    if (ans[i] == 1):
        if (test_ans[t1val["id"]] == t2val["id"]):
#            print t1val["price"],t2val["price"],X[i]
            truePos = truePos + 1
        else:
            falsePos = falsePos + 1
    else:
        if (test_ans[t1val["id"]] == t2val["id"]):
            falseNeg = falseNeg + 1
        else:
            trueNeg = trueNeg + 1
    
print "TN = ",trueNeg,"TP = ",truePos,"FN = ",falseNeg,"FP = ",falsePos
precision = truePos / float(truePos + falsePos)
recall = truePos / float(len(buyAr))
fmeas = (2.0 * precision * recall) / (precision + recall)
print "PREC = ",precision,"RECALL = ",recall,"F = ",fmeas
