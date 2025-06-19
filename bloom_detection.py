import xarray as xr
import numpy as np

class BloomDetector :

    phytoplankton_species_concentration = {'CHL' : {'baseline':0.02,
                                                      'bloom':1.0,
                                                    'duration':3},
                                           'DIATO': {'baseline': 0.2,
                                                     'bloom': 2.0,
                                                     'duration':3},
                                           'DINO': {'baseline': 0.5,
                                                    'bloom':1.0,
                                                    'duration':7},
                                           'GREEN': {'baseline': 0.3,
                                                     'bloom': 0.8,
                                                     'duration':2},
                                           'HAPTO': {'baseline':0.1,
                                                     'bloom':1.2,
                                                     'duration':7},
                                           'MICRO': {'baseline': 0.3,
                                                     'bloom': 2.0,
                                                     'duration':3},
                                           'NANO': {'baseline': 0.4,
                                                    'bloom': 0.8,
                                                    'duration':7},
                                           'PICO': {'baseline':0.2,
                                                    'bloom':0.5,
                                                    'duration':1},
                                           'PROCHLO': {'baseline':0.1,
                                                       'bloom':0.3,
                                                       'duration':7},
                                           'PROKAR': {'baseline':0.2,
                                                      'bloom':1.0,
                                                      'duration':7}
                                            }

    def __init__(self, dataset, global_mean_conc = None, global_std_conc = None, variable):
        self.dataset = dataset
        self.variable = variable
        self.bloom_features_list = []
        if global_mean_conc = None:
            self.global_mean_conc = phytoplankton_species_concentration[variable]['baseline']
        else:
            self.global_mean_conc = global_mean_conc

        if global_std_conc = None:
            self.global_std_conc = 0.0
        else:
            self.global_std_conc = global_std_conc

        self.local_mean_conc , self.local_std_conc = self.determine_variable_statistics()
                 
    def determine_variable_statistics(self):
        return dataset[variable].mean(), dataset[variable].std()

    def detect_bloom_statistically(self):
        if self.local_mean > self.global_mean_conc + 2*self.local_std_conc:
            return True
        else:
            return False

    def detect_bloom_hard_threshold(self):
        if self.local_mean > phytoplankton_species_concentration[self.variable]['bloom']:
            return True
        else:
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