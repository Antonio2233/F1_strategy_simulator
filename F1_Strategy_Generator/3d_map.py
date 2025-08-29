import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ast

# limit number of strats 
num_strats=2000
df = pd.read_csv("simulations.csv", nrows=num_strats)

# df = pd.read_csv("simulations.csv")


# Function to convert "mm:ss.mmm" into total seconds
def time_to_seconds(t):
    minutes, sec_milli = t.split(":")
    seconds, millis = sec_milli.split(".")
    return int(minutes) * 60 + int(seconds) + int(millis) / 1000

df["Total_seconds"] = df["Total"].apply(time_to_seconds)  # convert Total to seconds
df["Pit in Laps"] = df["Pit in Laps"].apply(lambda x: ast.literal_eval(x))  # convert string "[23, 44]" into a list

x_vals = [pits[0] if len(pits) > 0 else None for pits in df["Pit in Laps"]]  # first pit stop lap
z_vals = [pits[1] if len(pits) > 1 else None for pits in df["Pit in Laps"]]  # second pit stop lap (if exists)
y_vals = df["Total_seconds"]  # total race time in seconds
strategies = df["Strategy"]   # strategy names for legend

# 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Color points 
scatter = ax.scatter(x_vals, z_vals, y_vals, c=range(len(df)), cmap="tab10", s=60)

# Axis labels
ax.set_xlabel("Pit Stop 1 (lap)")
ax.set_ylabel("Pit Stop 2 (lap)")
ax.set_zlabel("Total Time (s)")
ax.set_title("Pit Stop Strategy Comparison")

# Add legend with strategy names
legend_labels = [strategies.iloc[i] for i in range(len(df))]

legend_labels = [strategies.iloc[i] for i in range(len(df))]
ax.legend(
    scatter.legend_elements()[0],
    legend_labels,
    title="Strategies",
    bbox_to_anchor=(1.2, 1),  # move legend outside plot (to the right)
    loc="upper left"
)

plt.show()
