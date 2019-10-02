import json
import platform
import sys
from collections import OrderedDict
from datetime import date
from subprocess import Popen, PIPE
from time import sleep

sites = []
temp = []
system = platform.system().lower()
today = date.today().strftime("%Y%m%d")
dicprocess = {}
process = []
dicPing = {}
dicTrace = {}


def getjsondata(typeoftool, dictionary):
    json_data = OrderedDict([
        ('date', f'{today}'),
        ('system', f'{system}'),
        (f'{typeoftool}', [OrderedDict([
            ('target', t),
            ('output', o)
        ]) for t, o in dictionary.items()])
    ])
    return json_data


def startprocessping(number):
    for i in range(number):
        p = Popen(["ping", '-n', '10', sites[i]], stdout=PIPE)
        dicprocess[f"{p}"] = f"{sites[i]}"
        process.append(p)


def startprocesstrace(number):
    for i in range(number):
        p = Popen(["tracert", sites[i]], stdout=PIPE)
        dicprocess[f"{p}"] = f"{sites[i]}"
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

startprocessping(20)
running = 20
print("ping processek száma: "f"{running}")
for x in process:
    if not x is None:
        dicPing[dicprocess[f"{x}"]] = f"{x.communicate()}"
        x = None
        running = running - 1
        print("ping processek száma: "f"{running}")

with open("ping.json", "w") as write_file_ping:
    json_data_ping = getjsondata("pings", dicPing)
    json.dump(json_data_ping, write_file_ping, indent=2)

write_file_ping.close()

process = []
startprocesstrace(20)
running = 20
print("traceroute processek száma: "f"{running}")
for x in process:
    if not x is None:
        dicTrace[dicprocess[f"{x}"]] = f"{x.communicate()}"
        x = None
        running = running - 1
        print("traceroute processek száma: "f"{running}")

with open("traceroute.json", 'w') as write_file_traceroute:
    json_data_trace = getjsondata("traces", dicTrace)
    json.dump(json_data_trace, write_file_traceroute, indent=2)

write_file_traceroute.close()
