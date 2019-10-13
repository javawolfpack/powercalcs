import csv

e1={
    "baseline":400.2,
    "Tier1":{
        "price":0.167,
        "percentage":1.0
    },
    "Tier2":{
        "price":0.19824,
        "percentage":4.0
    },
    "Tier3":{
        "price":0.252
    }
}

summer=[6,7,8,9]

toub={
    "peak_hours":5,
    "summer":{
        "peak":0.39064,
        "off_peak":0.28758
    },
    "winter":{
        "peak":0.39064,
        "off_peak":0.28758
    }
}

eva={
    "peak_hours":5,
    "part_peak_hours":4,
    "summer":{
        "peak":0.53476,
        "part_peak":0.2817,
        "off_peak":0.13578
    },
    "winter":{
        "peak":0.37313,
        "part_peak":0.22641,
        "off_peak":0.13913
    }
}


total_costs=[]
with open('powerwall.csv') as csvfile:  
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    first=True     
    for row in spamreader:
        if not first:
            consumption = float(row[2])+ float(row[5])
            solar = float(row[5])
            grid = float(row[2])
            # print(consumption)
            month = int(row[1].split("/")[0])
            hourly = consumption/30/24
            costs={}
            eva_cost=0
            # print(month)
            if month in summer:
                eva_cost=eva["summer"]["peak"]*hourly*eva["peak_hours"]
                eva_cost+=eva["summer"]["part_peak"]*hourly*eva["part_peak_hours"]
                eva_cost+=eva["summer"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                # print("summer")
            else:
                eva_cost=eva["winter"]["peak"]*hourly*eva["peak_hours"]
                eva_cost+=eva["winter"]["part_peak"]*hourly*eva["part_peak_hours"]
                eva_cost+=eva["winter"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                # print("winter")
            # print(hourly)
            costs["eva"]=eva_cost*30
            eva_cost=0
            # print(month)
            powerwall=13.5*2
            if month in summer:
                left = powerwall-hourly*eva["peak_hours"]
                if left < 0:
                    eva_cost=eva["summer"]["peak"]*(hourly*eva["peak_hours"]-powerwall)
                    eva_cost+=eva["summer"]["part_peak"]*hourly*eva["part_peak_hours"]
                    eva_cost+=eva["summer"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                else:
                    left = left-hourly*eva["part_peak_hours"]
                    if left < 0:
                        eva_cost+=eva["summer"]["part_peak"]*(hourly*eva["part_peak_hours"]-left)
                        eva_cost+=eva["summer"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                    else:
                        left = left-hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                        if left < 0:
                            eva_cost+=eva["summer"]["off_peak"]*(hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])-left)
                # print("summer")
            else:
                left = powerwall-hourly*eva["peak_hours"]
                if left < 0:
                    eva_cost=eva["winter"]["peak"]*(hourly*eva["peak_hours"]-powerwall)
                    eva_cost+=eva["winter"]["part_peak"]*hourly*eva["part_peak_hours"]
                    eva_cost+=eva["winter"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                else:
                    left = left-hourly*eva["part_peak_hours"]
                    if left < 0:
                        eva_cost+=eva["winter"]["part_peak"]*(hourly*eva["part_peak_hours"]-left)
                        eva_cost+=eva["winter"]["off_peak"]*hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                    else:
                        left = left-hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])
                        if left < 0:
                            eva_cost+=eva["winter"]["off_peak"]*(hourly*(24-eva["part_peak_hours"]-eva["peak_hours"])-left)
            costs["eva_solar"]=eva_cost
            costs["daily"]=hourly*24

            e1_cost = 0
            if consumption < e1["Tier1"]["percentage"]*e1["baseline"]:
                e1_cost=consumption*e1["Tier1"]["price"]
            elif consumption < e1["Tier2"]["percentage"]*e1["baseline"]:
                e1_cost=e1["Tier1"]["price"]*e1["baseline"]
                e1_cost+=(consumption-e1["baseline"])*e1["Tier2"]["price"]
            else:
                e1_cost=e1["Tier1"]["price"]*e1["baseline"]
                e1_cost+=(e1["baseline"]*e1["Tier2"]["percentage"]-e1["baseline"])*e1["Tier2"]["price"]
                e1_cost+=(consumption-e1["baseline"]*e1["Tier2"]["percentage"])*e1["Tier3"]["price"]
            costs["e1"]=e1_cost
            e1_cost_solar = 0
            consumption=consumption-solar
            if consumption < e1["Tier1"]["percentage"]*e1["baseline"]:
                e1_cost_solar=consumption*e1["Tier1"]["price"]
            elif consumption < e1["Tier2"]["percentage"]*e1["baseline"]:
                e1_cost_solar=e1["Tier1"]["price"]*e1["baseline"]
                e1_cost_solar+=(consumption-e1["baseline"])*e1["Tier2"]["price"]
            else:
                e1_cost_solar=e1["Tier1"]["price"]*e1["baseline"]
                e1_cost_solar+=(e1["baseline"]*e1["Tier2"]["percentage"]-e1["baseline"])*e1["Tier2"]["price"]
                e1_cost_solar+=(consumption-e1["baseline"]*e1["Tier2"]["percentage"])*e1["Tier3"]["price"]
            # print(e1_cost_solar)
            costs["e1_solar"]=e1_cost_solar
            # print(costs)
            total_costs+=[costs]
        else:
            first=False

savings = 0
for cost in total_costs:
    savings+=cost["e1_solar"]-cost["eva_solar"]
years=float(len(total_costs))/12.0
total=savings
save_year=savings/years
print(save_year)
powerwall_cost = 14100
payoff=powerwall_cost/save_year
print(payoff)
    