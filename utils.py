from datetime import datetime, timedelta

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