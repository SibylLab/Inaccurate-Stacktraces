import matplotlib.pyplot as plt
import numpy as np


labels =  ['AspectJ','Birt','Eclipse_Platform_UI','JDT']

"""
top1_means = [.53, .71, .9, .75]
top5_means = [.67, .63, .63, .61]
top10_means = [.58, .68, .63, .62]

top1_means = [.83, 1, .37, .17]
top5_means = [.55, .8, .83, .77]
top10_means = [.59, .46, .87, .8]

top1_means = [.64, .83, .53, .27]
top5_means = [.6, .71, .72, .68]
top10_means = [.59, .55, .73, .7]

"""
top1_means = [.5, .96, .66, .54]
top5_means = [.62, .69, .63, .66]
top10_means = [.57, .61, .62, .65]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, top1_means, width, label='Top 1')
rects2 = ax.bar(x , top5_means, width, label='Top 5')
rects3 =  ax.bar(x + width, top10_means, width, label='Top 10')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Accuracy')
#ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)

fig.tight_layout()

plt.show()
