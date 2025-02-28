# File: scripts/plot_metrics.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Configure style
    sns.set(style="whitegrid", palette="muted")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # Create plot directory
    os.makedirs("../plots", exist_ok=True)

    # Load data from CSV files
    buffer_sizes = [10, 50, 100]
    dfs = []
    
    for buf_size in buffer_sizes:
        df = pd.read_csv(f"../report_outputs/thread_comparison_buffer_{buf_size}.csv")
        df['BufferSize'] = buf_size
        dfs.append(df)
    
    full_df = pd.concat(dfs)

    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(18, 12))
    plt.suptitle("Producer-Consumer Performance Metrics", y=0.98)

    # Plot Execution Time
    sns.lineplot(data=full_df, x="Threads", y="ExecutionTime", hue="BufferSize", 
                ax=axs[0,0], marker="o", legend="full")
    axs[0,0].set_title("Execution Time vs Thread Count")
    axs[0,0].set_xscale("log", base=2)
    axs[0,0].set_ylabel("Time (seconds)")

    # Plot Throughput
    sns.lineplot(data=full_df, x="Threads", y="Throughput", hue="BufferSize",
                ax=axs[0,1], marker="s", legend="full")
    axs[0,1].set_title("Throughput vs Thread Count")
    axs[0,1].set_xscale("log", base=2)
    axs[0,1].set_ylabel("Items/sec")

    # Plot Context Switches
    sns.lineplot(data=full_df, x="Threads", y="ContextSwitches", hue="BufferSize",
                ax=axs[1,0], marker="^", legend="full")
    axs[1,0].set_title("Context Switches vs Thread Count")
    axs[1,0].set_xscale("log", base=2)
    axs[1,0].set_ylabel("Context Switches")

    # Plot Cache Miss Rate
    full_df['CacheMissRate'] = (full_df['CacheMisses'] / full_df['CacheReferences']) * 100
    sns.lineplot(data=full_df, x="Threads", y="CacheMissRate", hue="BufferSize",
                ax=axs[1,1], marker="d", legend="full")
    axs[1,1].set_title("Cache Miss Rate vs Thread Count")
    axs[1,1].set_xscale("log", base=2)
    axs[1,1].set_ylabel("Miss Rate (%)")

    plt.tight_layout()
    plt.savefig("../plots/python_metrics.png")
    plt.close()

if __name__ == "__main__":
    main()
