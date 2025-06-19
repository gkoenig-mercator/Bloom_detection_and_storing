from sqlalchemy import insert, Table, Column, Integer, String, MetaData, Float, inspect, create_engine
import pandas as pd
import copernicusmarine
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
import os

def generate_timestamps(start_date_str, end_date_str):
    """
    Generate a list of timestamps from start_date to end_date (inclusive).
    Timestamps are in the format: 'YYYY-MM-DD 00:00:00'
    
    Args:
        start_date_str (str): Start date in 'YYYY-MM-DD' format.
        end_date_str (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        List[str]: List of timestamp strings.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    timestamps = []
    current = start_date
    while current <= end_date:
        timestamps.append(current.strftime("%Y-%m-%d 00:00:00"))
        current += timedelta(days=1)

    return timestamps

def connect_to_database(database_url,database_name, username, password):
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{database_url}:5432/{database_name}')
    return engine

database_url, database_name, username, password = ('postgresql-989098.user-gkoenig', 'defaultdb','user-gkoenig','fk7bu9vwjexxyv1jh39o')

def return_list_tables(engine):
    inspector = inspect(engine)
    return inspector.get_table_names(schema="public")

def get_table(engine, table_name):
    metadata = MetaData()
    return Table(table_name, metadata, autoload_with=engine)

def create_table(engine, name):
    metadata = MetaData()
    
    table = Table(
    name, metadata,
    Column('id',Integer, primary_key = True),
    Column('Species', String),
    Column('Date', String),
    Column('Min_Lon',Integer),
    Column('Max_Lon',Integer),
    Column('Min_Lat',Integer),
    Column('Max_Lat',Integer),
    Column('Mean_Conc',Float),
    Column('Std_Conc',Float))

    metadata.create_all(engine)
    
    return table

def insert_data(engine, table, species, date, min_lon, max_lon, min_lat, max_lat, mean_conc, std_conc):
    data =  {"Species":species,
             "Date":date,
             "Min_Lon": min_lon,
             "Max_Lon": max_lon,
             "Min_Lat": min_lat,
             "Max_Lat": max_lat,
             "Mean_Conc": mean_conc,
             "Std_Conc": std_conc }
    
    with engine.connect() as conn:
        conn.execute(insert(table), data)
        conn.commit()

def getting_plankton_dataset_specific_date(date_timestamp_beginning, date_timestamp_end):
    algae_dataset = copernicusmarine.subset(dataset_id="cmems_obs-oc_atl_bgc-plankton_nrt_l3-multi-1km_P1D",
                                            start_datetime=date_timestamp_beginning,
                                            end_datetime=date_timestamp_end)
    return algae_dataset.file_path, xr.open_dataset(algae_dataset.file_path)

def determine_variable_statistics(dataset, variable):
    return dataset[variable].mean(), dataset[variable].std()

def detect_bloom(dataset, variable, mean, std):
    if dataset[variable].mean() > mean + std and dataset[variable].std() < std:
        return True
    else :
        return False

def scan_regions_for_blooms(dataset, variable, number_lat, number_lon):
    
    mean_var, std_var = determine_variable_statistics(dataset, variable)

    size_lat = int(dataset.latitude.size / number_lat)
    size_lon = int(dataset.longitude.size / number_lon)

    outputs = np.zeros((number_lat, number_lon))
    blooms_features = []

    for i in range(number_lat):
        for j in range(number_lon):
            lat_start = i * size_lat
            lat_end = (i + 1) * size_lat
            lon_start = j * size_lon
            lon_end = (j + 1) * size_lon

            sub_dataset = dataset.isel(
                latitude=slice(lat_start, lat_end),
                longitude=slice(lon_start, lon_end)
            )

            if detect_bloom(sub_dataset, variable, mean_var, std_var): 

                min_lat = float(sub_dataset.latitude.min())
                max_lat = float(sub_dataset.latitude.max())
                min_lon = float(sub_dataset.longitude.min())
                max_lon = float(sub_dataset.longitude.max())

                mean_conc, std_conc = determine_variable_statistics(sub_dataset, variable)

                blooms_features.append({
                    "i": i,
                    "j": j,
                    "min_lat": min_lat,
                    "max_lat": max_lat,
                    "min_lon": min_lon,
                    "max_lon": max_lon,
                    "mean_conc": float(mean_conc.data),
                    "std_conc": float(std_conc.data)
                    })

    return blooms_features

engine = connect_to_database(database_url,database_name, username, password)
list_timestamps = generate_timestamps('2025-06-02','2025-06-17')

for i in range(len(list_timestamps)-1):
    file_path, plankton_dataset = getting_plankton_dataset_specific_date(list_timestamps[i], list_timestamps[i+1])
    blooms_CHL = scan_regions_for_blooms(plankton_dataset.isel(time=0), 'CHL', 10, 10)
    os.remove(file_path)

    for bloom in blooms_CHL:
        insert_data(engine,bloom_table,'CHL',
                    list_timestamps[i],
                    bloom['min_lon'], 
                    bloom['max_lon'], 
                    bloom['min_lat'], 
                    bloom['max_lat'], 
                    bloom['mean_conc'], 
                    bloom['std_conc'])
    
