import csv

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
