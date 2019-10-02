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

with open("ping.json", "w") as write_file_ping:
    with open("traceroute.json", "w") as write_file_traceroute:
        dicPing = {}
        dicTrace = {}
        sp = []
        for i in range(len(sites)):
            p1 = Popen(["ping", '-n', '10', sites[i]], stdout=PIPE)
            p2 = Popen(["tracert", sites[i]], stdout=PIPE)
            sp.append(p1)
            sp.append(p2)
            for x in sp:
                x.wait()

            dicPing[sites[i]] = f"{p1.communicate()}"
            dicTrace[sites[i]] = f"{p2.communicate()}"

        json_data_ping = getjsondata("pings", dicPing)
        json_data_trace = getjsondata("traces", dicTrace)

        json.dump(json_data_ping, write_file_ping, indent=2)
        json.dump(json_data_trace, write_file_traceroute, indent=2)
