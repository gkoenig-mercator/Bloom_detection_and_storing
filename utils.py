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