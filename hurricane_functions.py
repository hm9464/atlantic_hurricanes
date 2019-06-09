import os
import re
import folium
import pandas as pd
import numpy as np
import datetime
from urllib.request import urlretrieve
from tqdm import tqdm_notebook as tqdm

def get_all_hurricanes(records):
    """
    The raw records from hurdat2 is a list of lists. We want 
    to parse this into a neat dataframe for easy analysis.
    """
    hurr_list = []
    for hurricane in tqdm(records, total=len(records)):
        year = hurricane[0].split(',')[0][-4:]
        hurr_id = hurricane[0].split(',')[0]
        hurr_list.append(hurr_id)
            
    num_hurr = len(hurr_list)
    records_for_yr = records[-num_hurr:]
    
    return records_for_yr

def create_hurricane_df(records):
    """
    The raw data from NOAA is a text file. This function parses that
    text file into a nice, readable Pandas dataframe for easy manipulation.
    """
    records_df = pd.DataFrame()
    idx = 0

    for record in records:
        hurricane_id = record[0].split(',')[0]
        hurricane_name = record[0].split(',')[1].strip()

        for datapoint in record[1]:
            data_list = [x.strip() for x in datapoint.split(',')]
            record_date = data_list[0]
            time = data_list[1]
            storm_status = data_list[3]
            lat = data_list[4]
            lon = data_list[5]
            max_wind = data_list[6]
            min_pressure = data_list[7]

            # Add to df
            records_df.loc[idx, 'id'] = hurricane_id
            records_df.loc[idx, 'name'] = hurricane_name
            records_df.loc[idx, 'date'] = record_date
            records_df.loc[idx, 'time'] = time
            records_df.loc[idx, 'dt'] = datetime.datetime.strptime(record_date+time,'%Y%m%d%H%M')        
            records_df.loc[idx, 'storm_status'] = storm_status
            records_df.loc[idx, 'lat'] = convert_lat_lon(lat, 'lat')
            records_df.loc[idx, 'lon'] = convert_lat_lon(lon, 'lon')
            records_df.loc[idx, 'max_wind'] = float(max_wind)
            records_df.loc[idx, 'min_pressure'] = float(min_pressure)

            idx +=1
            
    return records_df


def convert_lat_lon(value, col):
    """
    Lat/lon is encoded with the numeric value plus E/W/N/S. We want to 
    convert this into an absolute decimal value for folium to interpret.
    """
    if col=='lon':
        amount = -float(re.sub('[EW]', '', value)) if 'W' in value else float(re.sub('[EW]', '', value))
    elif col=='lat':
        amount = -float(re.sub('[NS]', '', value)) if 'S' in value else float(re.sub('[NS]', '', value))
    
    return amount

def plot_path(df, folium_map):
    """
    Generates a tuple comprising of lat/lon for the 
    folium map to plot.
    """
    # Folium requires an array of tuples
    points = df[['lat', 'lon']]
    tuple_points = [tuple(x) for x in points.values]
    return tuple_points

def hurr_category(max_wind):
    """
    Defining storm category at a point in time.
    """
    if max_wind <= 73:
        cat = 'TS'
    if (74 <= max_wind <= 95):
        cat = 1
    if (96 <= max_wind <= 110):
        cat = 2
    if (111 <= max_wind <= 129):
        cat = 3
    if (130 <= max_wind <= 156):
        cat = 4
    if max_wind >= 157:
        cat = 5
    return cat

def plot_paths_for_year(df, folium_map):
    """
    Plots hurricane path for all hurricanes in the dataframe
    where lines are color coded for the intensity (category) at that
    point in time.
    """
    # Map colors of path based on category level
    path_colors = {1: '#ffb3b3',
                   2: '#ff8080',
                   3: '#e60000',
                   4: '#ff0000',
                   5: '#580808',
                  'TS': '#ffe6e6'}
    
    for name in df['name'].unique():
        name_df = df[df['name']==name]
        for i, dt in name_df.iterrows():
            day_df = name_df.ix[i:i+1, :]
            day_points = plot_path(day_df, folium_map)
            date = name_df.loc[i, 'date']
            time = name_df.loc[i, 'time']
            category = hurr_category(name_df.loc[i, 'max_wind'])
            maxwind = name_df.loc[i, 'max_wind']
            hurr_info = f"""
            Storm:    {name}
            Date:     {date}
            Time:     {time}
            Category: {category}
            Max Wind: {maxwind}mph
            """
            folium.PolyLine(day_points, tooltip=name, popup=hurr_info, color=path_colors[category]).add_to(folium_map)
            
    return

def get_highest_category(input_df):
    """
    Each row is a hurricane at a point in time. Category will vary
    depending on wind speed at the time. We want to have an identifier
    for what each hurricane's max recorded category was.
    """
    df = input_df.copy(deep=True)
    for hurricane in df['id'].unique():
        hurr_df = df[df['id']==hurricane]
        try:
            max_cat = max(hurr_df[hurr_df['category']!='TS']['category'])
        except ValueError:
            max_cat = 'TS'
        df_indexes = hurr_df.index
        df.loc[df_indexes, 'category_highest'] = max_cat
        
    return df