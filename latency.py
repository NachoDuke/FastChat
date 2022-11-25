import numpy as np
import matplotlib.pyplot as plt

# creating the dataset
data = {'2Clients1Server': 96992, '3clients2servers1groups':205574, '3clients1server1groups':57146,
		'3clients3servers':118359, '10clients1Server':32811}
courses = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize = (10, 5))

# creating the bar plot
plt.bar(courses, values, color ='maroon',
		width = 0.4)

plt.xlabel("Configurations")
plt.ylabel("Avg Latency in microseconds")
plt.title("Latency Distribution")
plt.show()
