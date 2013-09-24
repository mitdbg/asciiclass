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
#    if (len(c) > 2):
#        print set1,set2,c,float(len(c)) / (len(set1) + len(set2) - len(c))
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


falsePos = 0
truePos = 0
falseNeg = 0
trueNeg = 0
thresh = .1
for r1 in buyAr:
    bestMatch = 0
    bestVal = []
    j = 0
    for r2 in abtAr:
        s = jaccard_score(r1,r2,"name")
        if (s > bestMatch):
            bestMatch = s
            bestVal = r2
    if (bestMatch > thresh):
        #        print "Best match: ",r1["name"],bestVal["name"],"score=",bestMatch
        if (gtBuyMap[r1["id"]] == bestVal["id"]):
            truePos = truePos + 1
        else:
            falsePos = falsePos + 1

precision = truePos / float(truePos + falsePos)
recall = truePos / float(len(buyAr))
fmeas = (2.0 * precision * recall) / (precision + recall)

print "THRESH = ",thresh,"TP = ",truePos,"FP = ",falsePos,"PREC = ",precision,"RECALL = ",recall,"F = ",fmeas
