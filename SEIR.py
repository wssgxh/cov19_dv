import numpy as np
import matplotlib.pyplot as plt

first_day_infective  = 15
first_day_removed = 3
first_day_exposed = 30
population = 1e7

N =  population + first_day_infective + first_day_removed
T = 200

s = np.zeros([T])   #Susceptible ratio
i = np.zeros([T])    # Infective ratio
e =  np.zeros([T])  #exposed ratio
r =  np.zeros([T])   # Removal ratio


lamda = 0.4     # contact rateN
gamma = 0.0821 # recover rate
sigma = 2/14   # exposed period

i[0] = first_day_infective / N
s[0] = population  /  N
e[0] = first_day_exposed / N

for t in range(T-1):
    s[t + 1] = s[t] - lamda * s[t] * i[t]
    e[t + 1] = e[t] + lamda * s[t] * i[t] - sigma * e[t]
    i[t + 1] = i[t] + sigma * e[t] - gamma * i[t]
    r[t + 1] = r[t] + gamma * i[t]


fig, ax = plt.subplots(figsize=(10,6))
ax.plot(s, c='b', lw=2, label='S')
ax.plot(e, c='orange', lw=2, label='E')
ax.plot(i, c='r', lw=2, label='I')
ax.plot(r, c='g', lw=2, label='R')
ax.set_xlabel('Day',fontsize=20)
ax.set_ylabel('Infective Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend();

plt.show()
