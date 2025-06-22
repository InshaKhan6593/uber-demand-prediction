from pathlib import Path
import pandas as pd

if __name__ == "__main__":
    current_path = Path(__file__)
    root_dir = current_path.parent.parent.parent
    data_path = root_dir/"processed"/"features.csv"

    df = pd.read_csv(data_path,parse_dates=["15min_bins"])

    df["day_of_week"] = df["15min_bins"].dt.day_of_week

    df.set_index("15min_bins",inplace=True)

    region_grp = df.groupby("region")

    