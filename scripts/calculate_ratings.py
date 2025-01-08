from operator import itemgetter
import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from app.containers import Container
from utils import connect_database, disconnect_database, generate_utc_timestamp


def calculate_ratings():
    channel_service = Container().channel_service()
    sorted_csv = channel_service.calculate_ratings()
    print(f"restult: {sorted_csv}")
    time_stamp = generate_utc_timestamp()
    with open("./scripts/rating_reports/ratings_" + time_stamp + ".csv", "w") as file:
        for key, value in sorted_csv.items():
            file.write("%s, %s\n" % (key, value))


if __name__ == "__main__":
    connect_database()
    calculate_ratings()
    disconnect_database()
