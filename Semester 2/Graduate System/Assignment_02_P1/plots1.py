import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("cache_misses_vs_threads.csv")

plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="Threads", y="Cache_Misses", marker="o", label="Cache Misses")
sns.lineplot(data=df, x="Threads", y="Cache_References", marker="s", label="Cache References")

plt.title("Cache Misses vs. Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Count")
plt.legend()
plt.grid(True)
plt.show()
