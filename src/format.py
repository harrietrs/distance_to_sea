from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def clean_distance_to_sea(
    distance_to_sea: pd.DataFrame, write: bool = False
) -> pd.DataFrame:
    """_summary_

    Args:
        distance_to_sea (pd.DataFrame): Data including distance to sea

    Returns:
        _type_: _description_
    """
    distance_to_sea.rename(
        columns={"distance to sea km": DISTANCE_TO_SEA_FIELD_NAME}, inplace=True
    )

    if write:
        write_output(distance_to_sea, file_name=DISTANCE_TO_SEA_FILE)

    return distance_to_sea


def write_output(df: pd.DataFrame, file_name: str):
    df.to_csv(
        Path("./output").joinpath(f"{file_name}"),
        index=False,
    )

    print("Distance to sea has been cleaned and saved")
