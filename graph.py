import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

# set height of bar
InputThroughput = [0.9945,  4.9507 , 4.4561 , 4.4481 , 25.9352]
OutputThroughput = [0.9895,  4.8202 , 4.399 , 4.3918 , 24.8827]

# Set position of bar on X axis
br1 = np.arange(len(OutputThroughput))
br2 = [x + barWidth for x in br1]

# Make the plot
plt.bar(br1, InputThroughput, color ='r', width = barWidth,
		edgecolor ='grey', label ='input')
plt.bar(br2, OutputThroughput, color ='g', width = barWidth,
		edgecolor ='grey', label ='output')

# Adding Xticks
plt.xlabel('Configurations', fontweight ='bold', fontsize = 15)
plt.ylabel('Throughput(per second)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(OutputThroughput))],
		['2Clients 1Server', '2Clients 1Server Group', '3Clients 2Servers 1Groups' , '3Clients 3Servers MinLoad', '10Clients 1Server'])

plt.legend()
plt.show()
