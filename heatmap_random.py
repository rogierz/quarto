import matplotlib.pyplot as plt
import numpy as np
from players import PLAYERS

# Define the win rate data as a 2D array
data = np.load("tournaments/all_vs_random_tournament.npy")
# Normalize the data between 0 and 1
data_norm = data / 100

# Define the x and y labels for the heatmap
labels = [k for k in PLAYERS.keys() if k != 'random']

# Create a heatmap using Matplotlib
fig, ax = plt.subplots(figsize=(10, 9))
im = ax.imshow(data_norm, cmap='viridis')

# Show the colorbar and set the tick labels
cbar = ax.figure.colorbar(im, ax=ax, use_gridspec=True)

# Set the x and y axis tick labels
ax.set_ylabel("Players", fontsize=14)
ax.set_xticks(np.arange(2))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(['Player First', 'Player Second'])
ax.set_yticklabels(labels)

# Rotate the x axis tick labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over the data and create annotations for each cell
for i in range(2):
    for j in range(len(labels)):
        text = ax.text(i, j, "{:.2f}".format(data_norm[j, i]),
                       ha="center", va="center", color='w')

# Add a title to the heatmap
ax.set_title("Win Rate Against Random Player Heatmap")

# Show the heatmap
plt.savefig("images/all_vs_random_tournaments.png", dpi=600)
plt.show()
