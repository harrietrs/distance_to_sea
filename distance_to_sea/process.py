from pathlib import Path

import pandas as pd
from bng_latlon import OSGB36toWGS84

from distance_to_sea import params


def process_pwc(raw_file: str = params.pwc_file) -> pd.DataFrame:
    """
    Cleans populated weighted centroids file

    Parameters
    ----------
    raw_file : str, optional
        The name of the PWC file.
        The default comes from params.py
    """
    # used to convert X & Y coords to latitude and longitude
    pwc = pd.read_csv(Path("./data").joinpath(raw_file))

    def _convert_to_latlon(row) -> pd.Series:
        """Convert X & Y coords to latitude and longitude"""
        lat, lon = OSGB36toWGS84(row["x"], row["y"])
        return pd.Series({"lat": lat, "lon": lon})

    print("Converting population-weighted centroids to geometry")
    pwc[["lat", "lon"]] = pwc.apply(_convert_to_latlon, axis=1)

    return pwc
