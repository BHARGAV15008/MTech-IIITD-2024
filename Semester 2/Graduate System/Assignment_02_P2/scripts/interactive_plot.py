# File: scripts/interactive_plot.py
import pandas as pd
import plotly.express as px
import os

def create_interactive_plot():
    os.makedirs("../plots", exist_ok=True)
    
    buffer_sizes = [10, 50, 100]
    dfs = []
    
    for buf_size in buffer_sizes:
        df = pd.read_csv(f"../report_outputs/thread_comparison_buffer_{buf_size}.csv")
        df['BufferSize'] = buf_size
        dfs.append(df)
    
    full_df = pd.concat(dfs)
    full_df['CacheMissRate'] = (full_df['CacheMisses'] / full_df['CacheReferences']) * 100

    fig = px.line(full_df, 
                 x="Threads", 
                 y="ExecutionTime",
                 color="BufferSize",
                 log_x=True,
                 title="Interactive Execution Time Analysis",
                 labels={"ExecutionTime": "Execution Time (seconds)"},
                 markers=True)
    
    fig.write_html("../plots/interactive_plot.html")

if __name__ == "__main__":
    create_interactive_plot()
