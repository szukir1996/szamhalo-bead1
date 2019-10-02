import sys

sites = []
temp = []

with open(sys.argv[1]) as myfile:
    for x in myfile:
        temp.append(x)

for x in range(10):
    sites.append(temp[0:10][x].split(',')[1].split('\n')[0])
    sites.append(temp[-10:][x].split(',')[1].split('\n')[0])

print(sites)