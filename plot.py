import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Benchmarking eqlog on the micro-benchmark')
parser.add_argument("--csvfile", default="benchmarks.csv")
parser.add_argument("--pdffile", default="benchmarks.pdf")
parser.add_argument("--no-viz", action='store_true')
args = parser.parse_args()

data = []
with open(args.csvfile, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append((int(row[0][9:]), row[1], float(row[2]), float(row[3])))

def smooth(data):
    for i in range(1, len(data)):
        data[i] = (data[i][0], max(data[i][1], data[i-1][1]))
    return data

X = 3
plt.figure(1)
eqlog = list(map(lambda x: (x[X], x[2]/1e9), filter(lambda x: x[1] == 'Eqlog', data)))
eqlog = smooth(eqlog)
eqlog_x = list(map(lambda x:x[0], eqlog))
eqlog_y = list(map(lambda x:x[1], eqlog))
plt.plot(eqlog_y, eqlog_x, label="EqLog")

eqlognaive = list(map(lambda x: (x[X], x[2]/1e9), filter(lambda x: x[1] == 'EqlogNaive', data)))
eqlognaive = smooth(eqlognaive)
eqlognaive_x = list(map(lambda x:x[0], eqlognaive))
eqlognaive_y = list(map(lambda x:x[1], eqlognaive))
plt.plot(eqlognaive_y, eqlognaive_x, label="EqLogNI")

egg = list(map(lambda x: (x[X], x[2]/1e9), filter(lambda x: x[1] == 'Egg', data)))
# egg = sorted(egg, key = lambda x: x[1])
egg = smooth(egg)
egg_x = list(map(lambda x:x[0], egg))
egg_y = list(map(lambda x:x[1], egg))
plt.plot(egg_y, egg_x, label="egg")
plt.xlabel("Time (s)")
plt.ylabel("E-node numbers")
plt.ylim((10**4, None))
plt.yscale('log')

plt.legend(loc='lower right')
plt.savefig(args.pdffile)

if not args.no_viz:
    plt.show()

naive_speedup = egg[-1][1] / eqlognaive[-1][1]
print("EqlogNaive speedup over egg: " + str(naive_speedup))
