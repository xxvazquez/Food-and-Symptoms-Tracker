from dash import Input, Output
import plotly.express as px
from data import fetch_data, fetch_data_distribution
from charts import (get_cooking_methods_chart, get_average_meal_time_chart, get_meal_distribution_chart)
from app import app  # Import the app instance

# Callback for Section 01: Meal Distribution Chart (now our first chart)
@app.callback(
    Output('meal-distribution-chart', 'figure'),
    Input('meal-distribution-chart', 'id')  # Dummy input
)
def update_meal_distribution(_):
    df = fetch_data_distribution()
    if df.empty:
        return px.bar(title='No Data Available')
    return get_meal_distribution_chart(df)

# Callback for Section 02: Cooking Methods Chart
@app.callback(
    Output('cooking-method-chart', 'figure'),
    Input('cooking-method-slider', 'value')
)
def update_cooking_methods(n):
    df = fetch_data()
    if df.empty:
        return px.bar(title='No Data Available')
    return get_cooking_methods_chart(df, n)

# Callback for Section 03: Average Meal Time Chart
@app.callback(
    Output('average-meal-time-chart', 'figure'),
    Input('average-meal-time-chart', 'id')  # Dummy input
)
def update_average_meal_time(_):
    df = fetch_data()
    if df.empty:
        return px.bar(title='No Data Available')
    return get_average_meal_time_chart(df)
