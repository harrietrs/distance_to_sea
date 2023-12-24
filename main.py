import timeit

from src.clean import clean_distance_to_sea


def main() -> None:

    print(f"\n{'-'*60}\nPipeline starting\n")
    # Create output folder
    print(f"\n{'-'*60}\nCleaning Data\n")
    clean_distance_to_sea()


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
