from pathlib import Path

import pandas as pd
from bng_latlon import OSGB36toWGS84

from src import calc, params


def clean_pwc(raw_file: str = params.LSOA_PWC_file):
    """
    Cleans populated weighted centroids file and saves a clean copy.

    Parameters
    ----------
    raw_file : str, optional
        The name of the PWC file.
        The default comes from params.py

        coastline.dropna(subset=["geometry"], inplace=True)
        coastline["geometry"] = coastline.apply(
            lambda row: row["geometry"].boundary, axis=1
        )

    """
    # used to convert X & Y coords to latitude and longitude
    # for use in sea distance
    LSOA_pwc = pd.read_csv(Path("./data").joinpath(raw_file))

    def _convert_to_latlon(row):
        """Convert X & Y coords to latitude and longitude"""
        lat, lon = OSGB36toWGS84(row["X"], row["Y"])
        return pd.Series({"lat": lat, "lon": lon})

    print("Converting population-weighted centroids to geometry")
    LSOA_pwc[["lat", "lon"]] = LSOA_pwc.apply(_convert_to_latlon, axis=1)
    LSOA_pwc = remove_wales_lsoas(LSOA_pwc)

    return LSOA_pwc


def clean_distance_to_sea(
    calculate: bool = False, raw_file: str = params.distance_to_sea_file
):
    """
    Cleans distance to sea file and saves a clean copy.

    Parameters
    ----------
    calculate: bool, optional
        Whether to calculate the distances.
    raw_file : str, optional
        The name of the distance to sea file.
        The default is params.distance_to_sea_file.

    Returns
    -------
    None.

    """
    if calculate:
        distance_to_sea = calc.calc_distance_to_sea()
    else:
        distance_to_sea = pd.read_csv(Path("./data").joinpath(raw_file))

    distance_to_sea.rename(
        columns={"distance to sea km": params.distance_to_sea_field_name}, inplace=True
    )

    distance_to_sea = remove_wales_lsoas(distance_to_sea)
    distance_to_sea.to_csv(
        Path("./output").joinpath(f"{raw_file}"),
        index=False,
    )

    print("Distance to sea has been cleaned and saved")

    return None


def remove_wales_lsoas(
    df: pd.DataFrame, lsoa_field_name: str = params.LSOA_code
) -> pd.DataFrame:
    """
    Filters out LSOAs that are within Wales.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing all LSOAs.
    lsoa_field_name : str, optional
        The LSOA code to use, e.g. "LSOA22CD".
        The default is params.LSOA_code.

    Returns
    -------
    df_england : pd.DataFrame
        DataFrame with only England LSOAs.

    """
    df_england = df[df[lsoa_field_name].str.startswith("E")].copy()

    return df_england
