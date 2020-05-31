import numpy as np
import matplotlib.pyplot as plt

N = 13.95 * 100000000
T = 200

s = np.zeros([T])   #Susceptible
i = np.zeros([T])    # Infective
r =  np.zeros([T])   # Removal
e =  np.zeros([T])


lamda = 0.4     # contact rateN
gamma = 0.0821 # recover rate
sigma = 1/14   # exposed period

i[0] = 18.0/ N   # 初始感染人数为 from 1st Feb 2020
s[0] = N / N
e[0] = 32.0 / N

for t in range(T-1):
    s[t + 1 ] = s[t] - lamda * s[t] * i[t]
    e[t + 1 ] = e[t] + lamda * s[t] * i[t] - sigma * e[t]
    i[t + 1 ] = i[t] + sigma * e[t] - gamma * i[t]
    r[t + 1 ] = r[t] + gamma * i[t]


fig, ax = plt.subplots(figsize = (10,5))
ax.plot(s, c ='b',lw=2,label='S')
ax.plot(i, c ='r',lw=2,label='I')
ax.plot(r, c ='g',lw=2,label='R')
ax.plot(e, c ='y',lw=2,label='E')

ax.set_xlabel('Day',fontsize = 20)
ax.set_ylabel('Infective Ratio', fontsize=20)
ax.grid(1)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)


today = 18
for day in range(0,14):
    print( 'The '+ str(today+day) + ' Feb 2020: ' + str(i[today+day] * N))


plt.show()
