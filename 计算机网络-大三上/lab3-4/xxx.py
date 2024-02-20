import matplotlib.pyplot as plt
import numpy as np

# Data from the table
trace_files = ["perlbench", "astar", "omnetpp", "lbm", "bwaves", "sphinx3", "mcf"]
lru_rates = [28.74, 3.2, 63.99, 60.85, 89.48, 80.45, 28.12]
hawkeye_rates = [28.95, 3.08, 66.81, 57.06, 89.48, 54.39, 24.70]
glider_rates = [27.86, 3.07, 62.03, 58.03, 89.48, 59.06, 24.34]

# Calculating the percentage decrease compared to LRU
hawkeye_decrease = [(l - h) / l * 100 for h, l in zip(hawkeye_rates, lru_rates)]
glider_decrease = [(l - g) / l * 100 for g, l in zip(glider_rates, lru_rates)]

# Setting up the bar plot
bar_width = 0.35
index = np.arange(len(trace_files))

# Creating the plot with revised values and title
plt.figure(figsize=(10, 6))
bar1 = plt.bar(index, hawkeye_decrease, bar_width, label="Hawkeye")
bar2 = plt.bar(index + bar_width, glider_decrease, bar_width, label="Glider")

# Adding labels and revised title
plt.xlabel("Trace Files")
plt.ylabel("Miss Rate Reduction over LRU (%)")
plt.title("Miss rate reduction for benchmarks.")
plt.xticks(index + bar_width / 2, trace_files)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
