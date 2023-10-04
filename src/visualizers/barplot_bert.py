# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Read the CSV file
# df = pd.read_csv('output.csv')
#
# # Get the values from the DataFrame
# values1 = df.loc[df['Name'] == 'Values 1', 'Values'].values[0]
# values2 = df.loc[df['Name'] == 'Values 2', 'Values'].values[0]
#
#
# # Set the x-axis values as the indices of the lists
# x = range(len(values1))
#
# # Create the bar plot
# plt.bar(x, values1, width=0.4, label='Values 1')
# plt.bar(x, values2, width=0.4, label='Values 2')
#
# # Set the x-axis tick labels
# plt.xticks(x, ['Value 1', 'Value 2'])
#
# # Set the y-axis label
# plt.ylabel('Values')
#
# # Set the plot title
# plt.title('Comparison of Values 1 and Values 2')
#
# # Add a legend
# plt.legend()
#
# # Display the plot
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

# Read the CSV file
df = pd.read_csv('output.csv')

# Get the values from the DataFrame
# values1 = df.loc[df['Name'] == 'Values 1', 'Values'].values[0]
# values2 = df.loc[df['Name'] == 'Values 2', 'Values'].values[0]

# values1 = json.loads(values1)
# values2 = json.loads(values2)

# values2 = [2.473193645477295, 2.084282636642456, 2.3240301609039307]
# values1 = [0.38947582244873047, 0.26556396484375, 0.24612784385681152]


# values1 = df.loc[df['Name'] == 'a1', 'Accuracy'].values[0]
# values2 = df.loc[df['Name'] == 'Names and Patterns (with all names)', 'Accuracy', 'Precision', 'Recall', 'Specificity'].values[0]
# values2 = df.loc[df['Name'] == 'a2', 'Accuracy'].values[0]
# values3 = df.loc[df['Name'] == 'a3', 'Accuracy'].values[0]



# values1 = json.loads(values1)
# values2 = json.loads(values2)
# values3 = json.loads(values3)

values1= [98.79436467,63.1147541,63.63636364,99.38025065]
values2= [98.97046871,78.48101266,51.23966942,99.76587247]
values3= [98.74017881,64.28571429,52.0661157,99.51797273]


x = np.arange(len(values1))  # Create an array of indexes for the bars
# x = np.arange(1)  # Create an array of indexes for the bars


width = 0.2  # Width of the bars

fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, values1, width, label='Names', color='#0d518b')
# rects2 = ax.bar(x + width/2, values2, width, label='Patterns', color='#72b7f2')

rects1 = ax.bar(x - width, values1, width, label="Epoch 2", color='#117cd6')
rects2 = ax.bar(x, values2, width, label="Epoch 3", color='#0d518b')
rects3 = ax.bar(x + width, values3, width, label="Epoch 4", color='#05243e')

# difference = (np.array(values1) + np.array(values2)) / 2
# ax.plot(x, difference, color='#072742', linewidth=2)

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('')
ax.set_ylabel('%')
ax.set_title('')
ax.set_xticks(x)
ax.legend()

labels = ['Accuracy', 'Precision', 'Recall', 'Specificity']

ax.set_xticklabels(labels)

# Add values on top of each bar
for rect in rects1 + rects2 + rects3:
    height = rect.get_height()
    ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.show()