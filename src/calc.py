from pathlib import Path

import geopandas as gpd
from geopy.distance import distance
from shapely.geometry import Point
from shapely.ops import nearest_points

from src import clean, params


def calc_distance_to_sea(coast_boundaries: str = params.coast_boundaries_file):
    """_summary_

    Args:
        coast_boundaries (str, optional): _description_.
        Defaults to params.coast_boundaries_file.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    print("Generating distances")
    coastline = gpd.read_file(Path("./data").joinpath(coast_boundaries))

    if coastline.empty or coastline["geometry"].isnull().any():
        raise ValueError("Coastline data is missing or invalid")

    lsoa_pwc = clean.clean_pwc()
    lsoa_pwc["geometry"] = lsoa_pwc.apply(
        lambda row: Point(
            row["lon"],
            row["lat"],
        ),
        axis=1,
    )

    # Filter out rows with missing or invalid geometries from lsoa_centroids
    lsoa_pwc.dropna(subset=["geometry"], inplace=True)

    # Find the closest point on the coastline to each LSOA centroid
    def _find_nearest_coast_point(row):
        coastline_geom = coastline["geometry"][0]
        nearest = nearest_points(row["geometry"], coastline_geom.boundary)
        if nearest[1] is not None:
            return nearest[1]
        return Point(row["geometry"].x, row["geometry"].y)

    print("Finding nearest coast point")
    lsoa_pwc["nearest_coast_point"] = lsoa_pwc.apply(_find_nearest_coast_point, axis=1)

    # Calculate distance from LSOA centroid to the closest point on the coastline
    def _calc_distance_to_coast(row):
        return distance(
            (row["lat"], row["lon"]),
            (row["nearest_coast_point"].y, row["nearest_coast_point"].x),
        ).km

    print("Calculating the distance to the coast")
    lsoa_pwc[params.distance_to_sea_field_name] = lsoa_pwc.apply(
        _calc_distance_to_coast, axis=1
    )

    return lsoa_pwc[[params.LSOA_code, params.distance_to_sea_field_name]]
