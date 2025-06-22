import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import joblib
import yaml

def read_cluster_input(data_path, chunksize=100000, usecols=["pickup_latitude","pickup_longitude"]):
    df_reader = pd.read_csv(data_path, chunksize=chunksize, usecols=usecols)
    return df_reader

def save_model(model,save_path):
    joblib.dump(model,save_path)

def read_params(save_path):
    with open(save_path,"r") as file:
        params = yaml.safe_load(file)
    return params    

if __name__ == "__main__":
    current_path = Path(__file__)
    root_dir = current_path.parent.parent.parent
    data_path = root_dir/"data"/"interim"/"cleaned_data.csv"
    model_output_path = root_dir/"models"

    reader_object = read_cluster_input(data_path)
    scaler = StandardScaler()

    for chunk in reader_object:
        scaler.partial_fit(chunk)

    save_model(scaler,model_output_path/"scaler.joblib")

    reader_object = read_cluster_input(data_path)
    params = read_params(root_dir/"params.yaml")
    mb_kmeans = MiniBatchKMeans(**params["extract_features"]["mini_batch_kmeans"])

    for chunk in reader_object:
        scaled_chunk = scaler.transform(chunk)
        mb_kmeans.partial_fit(scaled_chunk)

    save_model(mb_kmeans,model_output_path/"mini_batch_kmeans.joblib")    

    df = pd.read_csv(data_path,parse_dates=["tpep_pickup_datetime"])
    location_subset = df[["pickup_longitude","pickup_latitude"]]
    df["region"] = mb_kmeans.predict(scaler.transform(location_subset))

    df.drop(columns=["pickup_latitude","pickup_longitude"],inplace=True)

    df["15min_bins"] = df["tpep_pickup_datetime"].dt.floor("15T")

    df = df.groupby(["region","15min_bins"]).size().reset_index(name="total_pickups")

    df["avg_pickups"] = df.groupby("region")["total_pickups"].ewm(**params["extract_features"]["ewma"]).mean().round().values

    save_path = root_dir/"data"/"processed"/"features.csv"

    df.to_csv(save_path,index=False)