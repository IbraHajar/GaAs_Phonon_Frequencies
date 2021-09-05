import numpy as np
import os
from matplotlib import pyplot as plt

CWD = os.getcwd()
path_b1 = os.path.join(CWD, 'output/base_1.txt')
path_b2 = os.path.join(CWD, 'output/base_2.txt')
path_b3 = os.path.join(CWD, 'output/base_3.txt')

b1 = np.loadtxt(path_b1)
b2 = np.loadtxt(path_b2)
b3 = np.loadtxt(path_b3)

print(f'base 1:\n\tmean:{np.mean(b1)}\n\tstd dev:{np.std(b1)}')
print(f'base 2:\n\tmean:{np.mean(b2)}\n\tstd dev:{np.std(b2)}')
print(f'base 3:\n\tmean:{np.mean(b3)}\n\tstd dev:{np.std(b3)}')

a = plt.subplot(311)
a.hist(b1, bins=20)

a = plt.subplot(312)
a.hist(b2, bins=20)

a = plt.subplot(313)
a.hist(b3, bins=20)

plt.savefig('histogram_512.png')
