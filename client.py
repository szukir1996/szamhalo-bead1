import json
import platform
import sys
from collections import OrderedDict
from datetime import date
from subprocess import Popen, PIPE

sites = []
temp = []
system = platform.system().lower()
today = date.today().strftime("%Y%m%d")
dicprocess = {}
process = []
processoutput = []


def getjsondata(typeoftool, list):
    json_data = {
        "date": f'{today}',
        "system": f'{system}',
        f'{typeoftool}': []
    }
    for el in list:
        json_data[f'{typeoftool}'].append(el)
    return json_data


def startprocess(numberofprocesses, tool):
    for i in range(numberofprocesses):
        if (tool == "ping"):
            p = Popen(["ping", '-n', '10', sites[i]], stdout=PIPE)
        elif (tool == "traceroute"):
            p = Popen(["tracert", sites[i]], stdout=PIPE)
        else:
            return
        process.append(p)


with open(sys.argv[1]) as myfile:
    for x in myfile:
        temp.append(x)

if len(temp) >= 20:
    for x in range(10):
        sites.append(temp[0:10][x].split(',')[1].split('\n')[0])
        sites.append(temp[-10:][x].split(',')[1].split('\n')[0])
else:
    for x in range(len(temp)):
        sites.append(temp[0:len(temp)][x].split(',')[1].split('\n')[0])

startprocess(20, "ping")
running = 20
print("ping processek száma: "f"{running}")
for x in process:
    if not x is None:
        processoutput.append(f"{x.communicate()}")
        x = None
        running = running - 1
        print("ping processek száma: "f"{running}")

temp = [{"target": t, "output": s} for t, s in zip(sites, processoutput)]

with open("ping.json", "w") as write_file_ping:
    json_data_ping = getjsondata("pings", temp)
    json.dump(json_data_ping, write_file_ping, indent=2)
write_file_ping.close()

processoutput = []
process = []
startprocess(20, "traceroute")
running = 20
print("traceroute processek száma: "f"{running}")
for x in process:
    if not x is None:
        processoutput.append(f"{x.communicate()}")
        x = None
        running = running - 1
        print("traceroute processek száma: "f"{running}")

pings = [{"target": t, "output": s} for t, s in zip(sites, processoutput)]

with open("traceroute.json", 'w') as write_file_traceroute:
    json_data_trace = getjsondata("traces", pings)
    json.dump(json_data_trace, write_file_traceroute, indent=2)
write_file_traceroute.close()
