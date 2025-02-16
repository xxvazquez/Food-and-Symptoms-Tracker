# data.py
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1NUaTvo0sFL8ipS4nD56tigPI8X0buMePyrRJXHDj6_k/export?format=csv&gid=692498170"

def fetch_data():
    try:
        df = pd.read_csv(SHEET_URL, on_bad_lines="skip", encoding='utf-8')
        df['Meal time'] = pd.to_datetime(df['Meal time'], errors='coerce')
        df['Hour'] = df['Meal time'].dt.floor('H').dt.hour
        df['Weekday'] = df['Meal time'].dt.day_name()
        df['Hour Interval'] = df['Hour'].astype(str) + " - " + (df['Hour'] + 1).astype(str)
        df['Hour Interval'] = df['Hour Interval'].apply(lambda x: x.zfill(5))
        df = df.sort_values(by='Hour', ascending=True)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def fetch_data_distribution():
    try:
        df = pd.read_csv(SHEET_URL, on_bad_lines="skip", encoding='utf-8')
        df['Meal time'] = pd.to_datetime(df['Meal time'], errors='coerce')
        df = df.dropna(subset=['Meal time', 'Meal type'])
        df = df[df['Meal type'] != 'Snack']
        df['Hour'] = df['Meal time'].dt.hour
        df = df[df['Hour'].between(9, 23)]
        df['Hour Interval'] = df['Hour'].astype(str) + ':00 - ' + (df['Hour'] + 1).astype(str) + ':00'
        hour_intervals = [f"{h}:00 - {h+1}:00" for h in range(9, 24)]
        df['Hour Interval'] = pd.Categorical(df['Hour Interval'], categories=hour_intervals, ordered=True)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
