import xarray as xr
import numpy as np
import os

database_url, database_name, username, password = ('postgresql-989098.user-gkoenig', 'defaultdb','user-gkoenig','fk7bu9vwjexxyv1jh39o')

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
    
