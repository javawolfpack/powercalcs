import csv
from dateutil.parser import parse
from datetime import datetime, time



from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
onlyfiles = [f for f in onlyfiles if "csv" in f]

data = []
for f in onlyfiles:
    with open(f) as csvfile:  
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        first=True 
        count=0    
        for row in spamreader:
            count+=1
            if count > 289:
                continue
            #     # print(str(f)+ " " + str(row))
            try:
                time_obj = parse(row[0])
                d = {
                    "datetime":time_obj,
                    "home":float(row[1]),
                    "solar":float(row[2]),
                    "powerwall":float(row[3]),
                    "grid":float(row[4]),
                    "file":f
                }
                data+=[d]
            except:
                if count != 1:
                    # print(str(count)+" " +str(f)+ " " + str(row))
                    continue

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



data = sorted(data, key=lambda k: k['datetime'])
start = parse("2019-12-28T00:00:00.000-08:00")
end = parse("2020-1-29T00:00:00.000-08:00")
cost=0
for d in data:
    if d["datetime"] >= start and d["datetime"] < end:
        if 0 <= d["datetime"].hour < 15:  #off-peak
            cost+=d["grid"]*eva["winter"]["off_peak"]/12
        elif 15 <= d["datetime"].hour < 16 or 21 <= d["datetime"].hour < 24: #partial peak
            cost+=d["grid"]*eva["winter"]["part_peak"]/12
        else:
            cost+=d["grid"]*eva["winter"]["peak"]/12
print(cost)