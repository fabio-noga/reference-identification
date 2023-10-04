import os

import pandas as pd

values = []
n=0
with open(os.path.join("../..", "output", "training_file.txt"), "r", encoding='utf-8') as f:
    for line in f:
        phrase = line.split("\t")[1]
        if line.split(("\t"))[0] != "TP":
            continue
        # if len(phrase)>1000:
        #     print("Outlier length: " + str(len(phrase)))
        #     continue
        values.append(len(phrase))
        n += len(phrase)


import matplotlib.pyplot as plt
import statistics

print(len(values))
print("Mean: " + str(n/len(values)))
print("Median: " + str(statistics.median(values)))

# fig = plt.figure(figsize=(10, 7))
fig, ax = plt.subplots()

# Creating plot
B=plt.boxplot(values, vert=False)

def get_box_plot_data(bp):
    rows_list = []

    for i in range(1):
        dict1 = {}
        dict1['lower_whisker'] = bp['whiskers'][i*2].get_xdata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_xdata()[1]
        dict1['median'] = bp['medians'][i].get_xdata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_xdata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i*2)+1].get_xdata()[1]
        rows_list.append(dict1)

    return pd.DataFrame(rows_list)

print(get_box_plot_data(B))
# a = str(get_box_plot_data(B).values.tolist()[0])
# labels = ["0", "50.0", "125.0", "199.0", "309.0", "585.0"]
labels = ["0", "56.0", "207.25", "349.0", "628.25", "995.0"]

ax.set_xticklabels(labels)

#0            6.0            81.0   169.0           283.0          586.0
#"0", "56.0", "207.25", "349.0", "628.25", "995.0"
# show plot
plt.show()
