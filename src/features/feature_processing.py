from pathlib import Path
import pandas as pd

if __name__ == "__main__":
    current_path = Path(__file__)
    root_dir = current_path.parent.parent.parent
    data_path = root_dir/"data"/"processed"/"features.csv"

    df = pd.read_csv(data_path,parse_dates=["15min_bins"])

    df["day_of_week"] = df["15min_bins"].dt.day_of_week
    df["month"] = df["15min_bins"].dt.month

    df.sort_values(by=["region","15min_bins"],inplace=True)

    for lag in [1,2,3,4]:
        df[f"lag{lag}"] = df.groupby("region")["total_pickups"].shift(lag)

    df.dropna(inplace=True)
    df.set_index("15min_bins",inplace=True)

    train_data = df.loc[df["month"].isin([1,2]),:].drop(columns="month")    
    test_data = df.loc[df["month"] == 3,:].drop(columns="month")

    train_data.to_csv(root_dir/"data"/"processed"/"train.csv",index=True)
    test_data.to_csv(root_dir/"data"/"processed"/"test.csv",index=True)



    