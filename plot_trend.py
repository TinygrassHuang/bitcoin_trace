import matplotlib.pyplot as plt
import pandas as pd

addr = "1ArJTD4iR3SCwjuyiP3H6pbwvPBHduX6WB"
depth =  [4,5,6,7,8,9,10,12,15,20] # [4,5,6,7,8,9,10,12,15,20]
min_amount = 0.005
col = ['exchanges', 'pool', 'services_others', 'gambling', 'darknet']
data = []

for d in depth:
    df = pd.read_csv(f"result/{addr}_{d}_{min_amount}.csv")
    label_amount = df.groupby(["label"]).sum()["amount"]
    temp_dic = {}
    for i in col:
        if i in label_amount:
            temp_dic[i] = label_amount[i]
        else:
            temp_dic[i] = 0
    values = list(temp_dic.values())
    fraction = [i*100 / sum(values) for i in values]
    data.append(fraction)


print("--------------")
print(data)
print([row[1] for row in data])

fig,ax = plt.subplots()

for i in range(5):
    plt.plot(depth, [row[i] for row in data], label=col[i], marker='.')


plt.title(addr)
plt.xlabel("Tracing depth")
plt.ylabel("Composition (%)")
plt.legend()
plt.show()

fig.savefig(f"result/trend_{addr}_{min_amount}.jpg")
