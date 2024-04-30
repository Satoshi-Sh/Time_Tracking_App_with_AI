import streamlit as st
st.set_page_config(page_title="Activity Stats", page_icon="📈", layout="wide")
import plotly.graph_objects as go
import pandas as pd

## referred to https://github.com/andfanilo/social-media-tutorials/blob/master/20230816-stdashboard/streamlit_app.py

def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 22,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    ## True is better but indicator numbers cannot be centered
    st.plotly_chart(fig, use_container_width=False)

def plot_bar_chart(df):
   # Group by 'Task' and calculate the sum of 'Time' for each task
    task_times = df.groupby('Task')['Time'].sum()

    # Sort the result in descending order of 'Time'
    sorted = task_times.sort_values(ascending=False)
    sorted = pd.concat([sorted[sorted.index != 'Break'], sorted[sorted.index == 'Break']])
    # Define colors for each bar
    colors = ['#fd0' if task == 'Break' else '#1ac853' for task in sorted.index]

    # Create a custom bar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sorted.index, y=sorted.values, marker_color=colors))

    # Update the layout
    fig.update_layout(title='Time Spent on Tasks',
                    xaxis_title='Task',
                    yaxis_title='Time',
                    plot_bgcolor='rgba(0,0,0,0)',
                    )
    st.plotly_chart(fig,use_container_width=True)
   


df = st.session_state["task_time_df"]

if len(df)>0:
    # Separate Break and non-Break tasks
    total = df['Time'].sum()
    break_time_ratio = round(df[df['Task'] == 'Break']['Time'].sum() / total * 100) 
    non_break_time_ratio = round(df[df['Task'] != 'Break']['Time'].sum() /total * 100)

    col1, col2 = st.columns(2)
    with col1:
      plot_gauge(non_break_time_ratio,"#1ac853","%","Working", 100)
    with col2:
      plot_gauge(break_time_ratio,"#fd0", "%","Break", 100)
    
    plot_bar_chart(df)