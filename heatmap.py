import numpy as np
import matplotlib.pyplot as plt

# Define the win rate data as a 2D array
data = np.array([[0, 0.4975, 0.4975, 0.4975, 0.4955, 0.4975, 0.7588],
                 [0.5125, 0, 0.8318, 0.9019, 0.4755, 0.4975, 0.7868],
                 [0.3639, 0.1391, 0, 0.5946, 0.4884, 0.4884, 0.5065],
                 [0.3639, 0.1151, 0.4014, 0, 0.3, 0.3, 0.5395],
                 [0.4662, 0.5045, 0.4884, 0.7, 0, 0.4955, 0.4888],
                 [0.5035, 0.5035, 0.4884, 0.7, 0.5055, 0, 0.4888],
                 [0.7588, 0.2412, 0.5065, 0.4605, 0.5116, 0.5116, 0]])

# Normalize the data between 0 and 1
data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))

# Define the x and y labels for the heatmap
labels = ['rl', 'random', 'naive', 'risky',
          'montecarlo', 'minmax', 'evolutive']

# Create a heatmap using Matplotlib
fig, ax = plt.subplots()
im = ax.imshow(data_norm, cmap='viridis')

# Show the colorbar and set the tick labels
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1'])

# Set the x and y axis tick labels
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

# Rotate the x axis tick labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over the data and create annotations for each cell
for i in range(len(labels)):
    for j in range(len(labels)):
        text = ax.text(j, i, "{:.2f}".format(data_norm[i, j]),
                       ha="center", va="center", color="w")

# Add a title to the heatmap
ax.set_title("Win Rate Heatmap")

# Show the heatmap
plt.show()
