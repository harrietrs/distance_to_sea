from pathlib import Path

import geopandas as gpd
from geopy.distance import distance
from pandas import DataFrame
from shapely.geometry import Point
from shapely.ops import nearest_points

from src import params


def distance_to_sea(
    pwc: DataFrame, coast_boundaries: str = params.coast_boundaries_file
):
    """distance_to_sea

    Args:
        pwc (DataFrame): Population-weighted centroid data
        coast_boundaries (str, optional): File containing coastal boundary data.
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

    pwc["geometry"] = pwc.apply(
        lambda row: Point(
            row["lon"],
            row["lat"],
        ),
        axis=1,
    )

    # Filter out rows with missing or invalid geometries from lsoa_centroids
    pwc.dropna(subset=["geometry"], inplace=True)

    # Find the closest point on the coastline to each LSOA centroid
    def _find_nearest_coast_point(row):
        coastline_geom = coastline["geometry"][0]
        nearest = nearest_points(row["geometry"], coastline_geom.boundary)
        if nearest[1] is not None:
            return nearest[1]
        return Point(row["geometry"].x, row["geometry"].y)

    print("Finding nearest coast point")
    pwc["nearest_coast_point"] = pwc.apply(_find_nearest_coast_point, axis=1)

    def _calc_distance_between_points(row):
        return distance(
            (row["lat"], row["lon"]),
            (row["nearest_coast_point"].y, row["nearest_coast_point"].x),
        ).km

    print("Calculating the distance to the coast")
    pwc[params.distance_to_sea_field_name] = pwc.apply(
        _calc_distance_between_points, axis=1
    )

    return pwc[[params.LSOA_code, params.distance_to_sea_field_name]]
