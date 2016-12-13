#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

# example data
x = [1,2,3]#np.arange(0.1, 4, 0.5)
y = [2,4,6]# np.exp(-x)
err = [0.1, 0.3, 0.3]
# First illustrate basic pyplot interface, using defaults where possible.
plt.figure()
lines = plt.errorbar(x, y, yerr=err)

# use keyword args
plt.setp(lines[0], marker='o', color='r', linewidth=2.0)
#plt.title("Title")
plt.xlabel('Bandwidth (Gbps)')
plt.ylabel('Makespan improvement (%)')
plt.axis([0, 4, 0, 7])
plt.show()