import csv
import numpy as np
import matplotlib.pyplot as plt


counter = 0

sFileName = "wuhan_virus/source_data/SIR_data_source/data.csv"

with open("data.csv",newline='',encoding='UTF-8') as csvfile:
    rows=csv.reader(csvfile)

    T= 55

    s = np.zeros([T])  # Susceptible
    i = np.zeros([T])  # Infective
    r = np.zeros([T])  # Removal
    e = np.zeros([T])


    for row in rows:
        print(row)
        if counter == 0:
            counter = counter + 1
            continue

        s[counter]  = int(row[1]) - int(row[4])
        # e[counter] = row[2]
        #i[counter] = row[1]
        r[counter] = row[4]
        counter = counter + 1

print(s)


fig, ax = plt.subplots(figsize = (10,5))
ax.plot(s, c ='b',lw=2,label='S')
#ax.plot(i, c ='r',lw=2,label='I')
#ax.plot(r, c ='g',lw=2,label='R')
#ax.plot(e, c ='y',lw=2,label='E')

ax.set_xlabel('Day',fontsize = 20)
ax.set_ylabel('Infectived person', fontsize=20)
ax.grid(1)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.show()


