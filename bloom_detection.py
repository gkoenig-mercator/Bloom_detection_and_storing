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

    def __init__(self, dataset, variable, hard_threshold_detection = hard_threshold_detection,
                 global_mean_conc = None, global_std_conc = None):
        self.dataset = dataset
        self.variable = variable
        self.hard_threshold_detection = hard_threshold_detection
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

    def detect_bloom(self):
        if self.hard_threshold_detection:
            return detect_bloom_hard_threshold()
        else:
            return detect_bloom_statistically()

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