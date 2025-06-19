import copernicusmarine
from datetime import datetime, timedelta
import xarray as xr


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


def getting_plankton_dataset_specific_date(date_timestamp_beginning, date_timestamp_end):
    algae_dataset = copernicusmarine.subset(dataset_id="cmems_obs-oc_atl_bgc-plankton_nrt_l3-multi-1km_P1D",
                                            start_datetime=date_timestamp_beginning,
                                            end_datetime=date_timestamp_end)
    return algae_dataset.file_path, xr.open_dataset(algae_dataset.file_path)

def gather_bloom_features(sub_dataset, variables):

    return {"min_lat": float(sub_dataset.latitude.min()),
            "max_lat": float(sub_dataset.latitude.max()),
            "min_lon": float(sub_dataset.longitude.min()),
            "max_lon": float(sub_dataset.longitude.max()),
            "mean_conc": float(sub_dataset[variable].mean()),
            "std_conc": float(sub_dataset[variable].std())
            }

def subdatasets_extractor(dataset, resolution):

    number_step_lat = int(dataset.latitude.size / resolution)
    number_step_lon = int(dataset.longitude.size / resolution)

    for i in range(number_step_lat-1):
        for j in range(number_step_lon-1):

        yield dataset.isel( latitude=slice(i*resolution, (i+1)*resolution),
                             longitude=slice(j*resolution, (j+1)*resolution)
            )
    
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]