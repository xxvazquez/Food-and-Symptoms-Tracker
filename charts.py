# charts.py
import plotly.express as px
import pandas as pd

def get_cooking_methods_chart(df, n):
    cooking_methods = df['Cooking method(s)'].dropna().str.split(', ').explode().value_counts().head(n).reset_index()
    cooking_methods.columns = ['Cooking Method', 'Count']
    fig = px.bar(cooking_methods, x='Cooking Method', y='Count',
                 color='Cooking Method', labels={'x': '', 'y': ''},
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 opacity=0.8,
                 pattern_shape_sequence=[])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=10, color='darkgrey'),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.1, xanchor='center', x=0.5),
        shapes=[dict(type='line', x0=0, x1=1, y0=-0.1, y1=-0.1,
                     line=dict(color='grey', width=2))],
        xaxis_title='',
        yaxis_title=''
    )
    return fig

def get_average_meal_time_chart(df):
    # Process timestamps and compute seconds since midnight
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Weekday'] = df['Timestamp'].dt.day_name()
    df['Meal time'] = pd.to_datetime(df['Meal time'], format='%H:%M', errors='coerce')
    df = df[(df['Meal time'].dt.hour >= 9) & (df['Meal time'].dt.hour < 24)]
    df['Meal Seconds'] = (df['Meal time'].dt.hour * 3600 +
                          df['Meal time'].dt.minute * 60 +
                          df['Meal time'].dt.second)
    avg_meal_times = df.groupby(['Weekday', 'Meal type'])['Meal Seconds'].mean().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_meal_times['Weekday'] = pd.Categorical(avg_meal_times['Weekday'], categories=weekday_order, ordered=True)
    avg_meal_times = avg_meal_times.sort_values('Weekday')
    avg_meal_times['Avg Meal Time'] = avg_meal_times['Meal Seconds'].apply(
        lambda s: pd.Timestamp('1900-01-01 00:00:00') + pd.Timedelta(seconds=s))
    def convert_seconds_to_time_str(s):
        hours = int(s // 3600)
        minutes = int(round((s % 3600) / 60))
        return f"{hours:02d}:{minutes:02d}"
    avg_meal_times['Avg Meal Time Str'] = avg_meal_times['Meal Seconds'].apply(convert_seconds_to_time_str)
    fig = px.line(avg_meal_times,
                  x='Weekday',
                  y='Avg Meal Time',
                  color='Meal type',
                  markers=True,
                  labels={'Avg Meal Time': '', 'Meal type': ''},
                  line_shape='spline',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    y_lower = pd.Timestamp('1900-01-01 09:00:00')
    y_upper = pd.Timestamp('1900-01-01 23:59:59')
    fig.update_yaxes(range=[y_lower, y_upper], tickformat='%H:%M')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=10, color='darkgrey'),
        xaxis=dict(categoryorder='array', categoryarray=weekday_order),
        legend=dict(orientation='h', yanchor='bottom', y=1.1, xanchor='center', x=0.5),
        xaxis_title=''
    )
    fig.update_traces(text=avg_meal_times['Avg Meal Time Str'], textposition='top center')
    return fig

def get_meal_distribution_chart(df):
    # Filter to include only Breakfast, Lunch, and Dinner
    df = df[df['Meal type'].isin(['Breakfast', 'Lunch', 'Dinner'])]
    grouped_df = df.groupby(['Hour Interval', 'Meal type']).size().reset_index(name='Count')
    color_map = {"Breakfast": "#A8D5BA", "Lunch": "#C3A2E5", "Dinner": "#F4C2C2"}
    
    fig = px.bar(grouped_df,
                 x='Count',
                 y='Hour Interval',
                 color='Meal type',
                 orientation='h',
                 color_discrete_map=color_map,
                 labels={'Count': '', 'Hour Interval': '', 'Meal type': ''},
                 barmode='stack',
                 pattern_shape_sequence=[])
    
    # Define our expected hour interval categories from 9:00 to 23:00
    categories = [f"{h}:00 - {h+1}:00" for h in range(9, 24)]
    
    # For each meal type, determine its maximum interval.
    max_intervals = {}
    for meal in grouped_df['Meal type'].unique():
        subset = grouped_df[grouped_df['Meal type'] == meal]
        if not subset.empty:
            max_interval = subset.loc[subset['Count'].idxmax(), 'Hour Interval']
            max_intervals[meal] = max_interval

    # We'll add one highlight per unique interval across meals.
    unique_intervals = set(max_intervals.values())
    for interval in unique_intervals:
        if interval in categories:
            i = categories.index(interval)
            # Using yref="y", Plotly maps categories to integer values:
            y0 = i - 0.5
            y1 = i + 0.5
            fig.add_shape(
                type="rect",
                xref="paper",
                yref="y",
                x0=-0.15,  # Highlight spans left of the plot (adjust as needed)
                x1=0,
                y0=y0,
                y1=y1,
                fillcolor="yellow",
                opacity=0.3,
                line_width=0,
                layer="below"
            )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=10, color='#444444'),
        xaxis=dict(title=None, showgrid=False, showticklabels=True),
        yaxis=dict(
            title=None,
            showgrid=True,
            tickmode='array',
            tickvals=categories,
            ticktext=categories,
            categoryorder='array',
            categoryarray=categories,
            showticklabels=True
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation='h', yanchor='bottom', y=1.1, xanchor='center', x=0.5)
    )
    return fig
