import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Google Sheets URL (Replace with your own Sheet URL with export format CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1NUaTvo0sFL8ipS4nD56tigPI8X0buMePyrRJXHDj6_k/export?format=csv&gid=692498170"

def fetch_data():
    try:
        df = pd.read_csv(SHEET_URL, on_bad_lines="skip", encoding='utf-8')
        df['Meal time'] = pd.to_datetime(df['Meal time'], errors='coerce')
        df['Hour'] = df['Meal time'].dt.floor('H').dt.hour
        df['Weekday'] = df['Meal time'].dt.day_name()
        df['Hour Interval'] = df['Hour'].astype(str) + " - " + (df['Hour'] + 1).astype(str)  # Creating 1-hour intervals
        df['Hour Interval'] = df['Hour Interval'].apply(lambda x: x.zfill(5))  # Ensure formatting is correct
        df = df.sort_values(by='Hour', ascending=True)  # Ensure proper ordering from morning to night
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Initialize Dash App
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.Div([
        html.Span("01", style={'font-size': '32px', 'color': '#D3D3D3', 'font-weight': 'bold'}),
        html.Span(" meal frequency", style={'font-size': '32px', 'font-style': 'italic', 'color': '#5A4D41'}),
    ], style={'margin-bottom': '20px'}),
    
    dcc.Graph(id='meal-frequency-chart', style={'height': '500px'}),
    
    html.Div([
        html.Span("02", style={'font-size': '32px', 'color': '#D3D3D3', 'font-weight': 'bold'}),
        html.Span(" most common cooking methods", style={'font-size': '32px', 'font-style': 'italic', 'color': '#5A4D41'}),
    ], style={'margin-top': '50px'}),
    
    dcc.Slider(1, 10, 1, value=5, id='cooking-method-slider'),
    dcc.Graph(id='cooking-method-chart', style={'height': '400px'}),
    
    html.Div([
        html.Span("03", style={'font-size': '32px', 'color': '#D3D3D3', 'font-weight': 'bold'}),
        html.Span(" average meal times by weekday", style={'font-size': '32px', 'font-style': 'italic', 'color': '#5A4D41'}),
    ], style={'margin-top': '50px'}),
    
    # Dropdown to select meal type for comparison
    dcc.Dropdown(
        id='meal-type-dropdown',
        options=[
            {'label': 'Breakfast', 'value': 'Breakfast'},
            {'label': 'Lunch', 'value': 'Lunch'},
            {'label': 'Dinner', 'value': 'Dinner'}
        ],
        value='Breakfast',  # Default meal type
        style={'width': '50%', 'margin-top': '20px', 'font-family': 'Arial, sans-serif'}  # Added margin and font-family
    ),
    
    dcc.Graph(id='average-meal-time-chart', style={'height': '400px'}),
], style={'backgroundColor': '#F6F6F7', 'padding': '50px', 'max-width': '800px', 'margin': '0 auto'})

# Callbacks
@app.callback(
    Output('meal-frequency-chart', 'figure'),
    Input('meal-frequency-chart', 'id')
)
def update_meal_frequency(_):
    df = fetch_data()
    if df.empty:
        return px.bar(title='No Data Available')
    df['Meal type'] = df['Meal type'].fillna("Unknown")
    df = df[(df['Hour'] >= 8) | (df['Hour'] == 0)]  # Keep hours from 8 AM to Midnight
    df['Hour'] = df['Hour'].replace(0, 24)  # Shift midnight to the right of 23
    df = df[df['Meal type'] != 'Snack']  # Remove Snack
    grouped_df = df.groupby(['Hour Interval', 'Meal type']).size().reset_index(name='Count')
    fig = px.bar(grouped_df,
                 x='Hour Interval', y='Count', color='Meal type',
                 labels={'Hour Interval': '', 'Count': ''},  # Removed axis titles
                 color_discrete_sequence=px.colors.qualitative.Pastel, barmode='stack', opacity=0.9)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Arial", size=10, color='darkgrey'),  # Font size smaller, color dark grey
        showlegend=True, 
        legend=dict(orientation='h', yanchor='bottom', y=1.1, xanchor='center', x=0.5),
        xaxis=dict(tickangle=90, tickfont=dict(size=10)),
        shapes=[dict(type='line', x0=0, x1=1, y0=-0.1, y1=-0.1, line=dict(color='grey', width=2))]  # Grey line separating graph
    )
    return fig

@app.callback(
    Output('cooking-method-chart', 'figure'),
    Input('cooking-method-slider', 'value')
)
def update_cooking_methods(n):
    df = fetch_data()
    if df.empty:
        return px.bar(title='No Data Available')
    cooking_methods = df['Cooking method(s)'].dropna().str.split(', ').explode().value_counts().head(n).reset_index()
    cooking_methods.columns = ['Cooking Method', 'Count']
    fig = px.bar(cooking_methods, x='Cooking Method', y='Count',
                 color='Cooking Method', labels={'x': '', 'y': ''},  # Removed axis titles
                 color_discrete_sequence=px.colors.qualitative.Pastel, opacity=0.8)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Arial", size=10, color='darkgrey'),  # Font size smaller, color dark grey
        showlegend=True, 
        legend=dict(orientation='h', yanchor='bottom', y=1.1, xanchor='center', x=0.5),
        shapes=[dict(type='line', x0=0, x1=1, y0=-0.1, y1=-0.1, line=dict(color='grey', width=2))]  # Grey line separating graph
    )
    return fig

@app.callback(
    Output('average-meal-time-chart', 'figure'),
    Input('meal-type-dropdown', 'value')  # This callback now depends on the selected meal type
)
def update_average_meal_time(selected_meal_type):
    df = fetch_data()
    if df.empty:
        return px.bar(title='No Data Available')

    # Filter data for the selected meal type
    df_filtered = df[df['Meal type'] == selected_meal_type]

    # Convert 'Timestamp' to datetime format and extract the weekday
    df_filtered['Timestamp'] = pd.to_datetime(df_filtered['Timestamp'], errors='coerce')
    df_filtered['Weekday'] = df_filtered['Timestamp'].dt.day_name()  # Extract the weekday from the timestamp

    # Convert 'Meal time' to hours and minutes
    df_filtered['Meal time'] = pd.to_datetime(df_filtered['Meal time'], format='%H:%M', errors='coerce')
    df_filtered['Meal Hour'] = df_filtered['Meal time'].dt.hour + df_filtered['Meal time'].dt.minute / 60  # Convert to decimal hours

    # Group by weekday, calculating the average meal time
    avg_meal_times = df_filtered.groupby(['Weekday'])['Meal Hour'].mean().reset_index()

    # Order weekdays properly: Monday to Sunday
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    avg_meal_times['Weekday'] = pd.Categorical(avg_meal_times['Weekday'], categories=weekday_order, ordered=True)

    # Sort the values to ensure proper order of weekdays
    avg_meal_times = avg_meal_times.sort_values(by=['Weekday'])

    # Create the line chart for the selected meal type with smooth lines and pastel colors
    fig = px.line(avg_meal_times, x='Weekday', y='Meal Hour', markers=True,
                  labels={'Weekday': '', 'Meal Hour': ''},  # Removed axis titles
                  title=f'Average {selected_meal_type} Time Across the Week',
                  line_shape='spline',  # Smooth lines
                  color_discrete_sequence=px.colors.qualitative.Pastel)  # Pastel colors

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Arial", size=10, color='darkgrey'),
        xaxis=dict(tickmode='array', tickvals=weekday_order, ticktext=weekday_order),
        shapes=[dict(type='line', x0=0, x1=1, y0=-0.1, y1=-0.1, line=dict(color='grey', width=2))]  # Grey line separating graph
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
