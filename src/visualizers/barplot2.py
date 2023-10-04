values1 = 2046.1727702617645
values2 = 1139.0861954689026
values3 = 1903.052444934845

# libraries
import matplotlib.pyplot as plt
import numpy as np

# create dataset
height = [1903.052444934845, 204.50084447860718, 4.820880889892578]
bars = ('BERT Iteration 3', 'Grammar Rules', 'Names and Patterns')
y_pos = np.arange(len(bars))
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_title('')
ax.legend()

x = np.arange(1)
width = 0.2
rects1 = ax.bar(x - width, height[0], width, label="Epoch 2", color='#117cd6')
rects2 = ax.bar(x, height[1], width, label="Epoch 3", color='#0d518b')
rects3 = ax.bar(x + width, height[2], width, label="Epoch 4", color='#05243e')
# Create horizontal bars
plt.barh(y_pos, height, color=['#05243e', '#0d518b', '#117cd6'])

for rect in rects1 + rects2 + rects3:
    height = rect.get_height()
    ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Create names on the x-axis
plt.yticks(y_pos, bars)

# Show graphic
plt.show()