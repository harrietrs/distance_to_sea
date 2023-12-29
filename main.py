import timeit

from src.calc import distance_to_sea
from src.format import clean_distance_to_sea
from src.process import process_pwc


def main() -> None:
    print(f"\n{'-'*60}\nPipeline starting\n")
    print(f"\n{'-'*60}\nCleaning Data\n")
    pwc = process_pwc()
    distances = distance_to_sea(pwc)
    clean_distance_to_sea(distances, write=True)


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
