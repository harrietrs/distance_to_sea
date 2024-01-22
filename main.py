import timeit

import yaml

from distance_to_sea.calc import calc_distance_to_sea
from distance_to_sea.format import clean_distance_to_sea
from distance_to_sea.process import process_pwc

with open("config.yml", "r") as yamlfile:
    cfg = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Config loaded")
print(cfg)


def main() -> None:
    "Main function to run pipeline"
    print(f"\n{'-'*60}\nPipeline starting\n")
    print(f"\n{'-'*60}\nCleaning Data\n")
    pwc = process_pwc(cfg["files"]["centroids"])
    distances = calc_distance_to_sea(
        pwc,
        coast_boundaries=cfg["files"]["boundaries"],
        area_code=cfg["fields"]["area_code"],
        distance_to_sea_field=cfg["fields"]["output_field"],
    )
    clean_distance_to_sea(
        distances,
        distance_to_sea_field_name=cfg["fields"]["output_field_name"],
        distance_to_sea_file=cfg["files"]["output"],
        write=True,
    )


if __name__ == "__main__":
    print("Running create_publication script")
    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    total_minutes = int(total_time / 60)
    total_leftover_seconds = round(total_time % 60)
    print(
        f"""
        Running time of create_publication script:
        {total_minutes} minutes and {total_leftover_seconds} seconds.\n
        """
    )
