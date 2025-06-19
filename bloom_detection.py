import xarray as xr
import numpy as np


def determine_variable_statistics(dataset, variable):
    return dataset[variable].mean(), dataset[variable].std()

def detect_bloom(local_mean, local_std, global_mean, global_std):
    if local_mean > global_mean + global_std and local_std < global_std:
        return True
    else :
        return False

def gather_bloom_features(sub_dataset, variables):

    return {"min_lat": float(sub_dataset.latitude.min()),
            "max_lat": float(sub_dataset.latitude.max()),
            "min_lon": float(sub_dataset.longitude.min()),
            "max_lon": float(sub_dataset.longitude.max()),
            "mean_conc": float(sub_dataset[variable].mean()),
            "std_conc": float(sub_dataset[variable].std())
            }

def scan_regions_for_blooms(dataset, variable, number_lat, number_lon):
    
    global_mean, global_std = determine_variable_statistics(dataset, variable)

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
            local_mean, local_std = determine_variable_statistics(sub_dataset, variable)
            
            if detect_bloom(local_mean, local_std, global_mean, global_std): 

                min_lat = float(sub_dataset.latitude.min())
                max_lat = float(sub_dataset.latitude.max())
                min_lon = float(sub_dataset.longitude.min())
                max_lon = float(sub_dataset.longitude.max())


                blooms_features.append(gather_bloom_features(sub_dataset, variable))

    return blooms_features