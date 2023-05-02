import numpy as np
import matplotlib.pyplot as plt
from players import PLAYERS

# Thanks ChatGPT

# Define the win rate data as a 2D array
data = np.load("tournaments/all_tournament.npy")
# Normalize the data between 0 and 1
data_norm = data / 100

# Define the x and y labels for the heatmap
labels = [k for k in PLAYERS.keys() if k != 'random']

# Create a heatmap using Matplotlib
fig, ax = plt.subplots(figsize=(10, 9))
im = ax.imshow(data_norm, cmap='viridis')

# Show the colorbar and set the tick labels
cbar = ax.figure.colorbar(im, ax=ax, use_gridspec=True)
cbar.ax.set_yticklabels(
    ['0', '0.2', '0.4', '0.6', '0.8', '1'])

# Set the x and y axis tick labels
ax.set_ylabel("Player 0", fontsize=14)
ax.set_xlabel("Player 1", fontsize=14)
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
plt.savefig("images/all_tournaments.png", dpi=600)
plt.show()
