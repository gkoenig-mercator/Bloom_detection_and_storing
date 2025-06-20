import xarray as xr
import numpy as np
import os
import utils
import bloom_detection
import plankton_database

phytoplankton_species = ['CHL', 'DIATO', 'DINO','GREEN','HAPTO','MICRO','NANO','PICO','PROCHLO','PROKAR']

database_url, database_name, username, password = ('postgresql-989098.user-gkoenig', 'defaultdb','user-gkoenig','fk7bu9vwjexxyv1jh39o')

plankton_DB = plankton_database.planktonDB(database_url,database_name, username, password)
list_timestamps = utils.generate_timestamps('2025-06-02','2025-06-17')

for i in range(len(list_timestamps)-1):
    file_path, plankton_dataset = utils.getting_plankton_dataset_specific_date(list_timestamps[i], list_timestamps[i+1])

    global_mean_conc, global_std_conc = utils.determine_variable_statistics(plankton_dataset, 'CHL')

    for subdataset in utils.subdatasets_extractor(plankton_dataset, 4):
        bloom_detector = bloom_detection.BloomDetector(plankton_dataset,'CHL',
                                                       global_mean_conc=global_mean_conc,
                                                       global_std_conc=global_std_conc)

        if bloom_detector.detect_bloom():
            bloom_features =   {"Species":'Chl',
                                 "Date":list_timestamps[i],
                                 "Min_Lon": subdataset.longitude.min(),
                                 "Max_Lon": subdataset.longitude.max(),
                                 "Min_Lat": subdataset.latitude.min(),
                                 "Max_Lat": subdataset.latitude.max(),
                                 "Mean_Conc": bloom_detector.local_mean_conc,
                                 "Std_Conc": bloom_detector.local_std_conc
                                }
            plankton_DB.insert_data(bloom_features)
                                                       
        
    os.remove(file_path)


