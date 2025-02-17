import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = "perf_analysis.csv"  # Update with actual path if needed
df = pd.read_csv(file_path)

# Check data structure
print(df.info())
print(df.head())

# Set Seaborn style
sns.set(style="whitegrid")

# Plot CPU, IO, and Mixed Workload against Threads
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="Threads", y="Total_CPU_Workload", marker="o", label="CPU Workload")
sns.lineplot(data=df, x="Threads", y="Total_IO_Workload", marker="s", label="IO Workload")
sns.lineplot(data=df, x="Threads", y="Total_Mixed_Workload", marker="^", label="Mixed Workload")

# Customize the plot
plt.title("Performance Analysis by Thread Count")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.show()

