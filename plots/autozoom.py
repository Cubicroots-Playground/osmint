import numpy as np

def from_coordinates(max_lon: float, min_lon: float, max_lat: float, min_lat: float) -> float:
    max_bound = max(abs(max_lat-min_lat), abs(max_lon-min_lon)) * 111
    return 11.5 - np.log(max_bound)

def center_from_coordinates(max_lon: float, min_lon: float, max_lat: float, min_lat: float) -> tuple[float, float]:
    return [(max_lon + min_lon)/2, (max_lat + min_lat)/2]