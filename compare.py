import csv

e1={
    "baseline":400.2,
    "Tier1":{
        "price":0.167,
        "percentage":100
    },
    "Tier2":{
        "price":0.19824,
        "percentage":400
    },
    "Tier3":{
        "price":0.252
    }
}



with open('powerwall.csv') as csvfile:  
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    first=True     
    for row in spamreader:
        if not first:
            consumption = float(row[2])+ float(row[5])
            solar = float(row[5])
            grid = float(row[2])
            print(consumption)
            e1_cost = 0
            if consumption < e1["Tier1"]["percentage"]*e1["baseline"]/100:
                e1_cost=consumption*e1["Tier1"]["price"]
            else:
                e1_cost=e1["Tier1"]["percentage"]*e1["baseline"]/100*consumption*e1["Tier1"]["price"]
            print(e1_cost)
        else:
            first=False