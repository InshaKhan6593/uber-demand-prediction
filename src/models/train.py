from pathlib import Path
import pandas as pd
import joblib
import yaml
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

def save_model(model,path):
    joblib.dump(model,path)

if __name__ == "__main__":
    current_path = Path(__file__)
    root_dir = current_path.parent.parent.parent
    data_path = root_dir/"data"/"processed"/"train.csv"

    df = pd.read_csv(data_path,parse_dates=["15min_bins"],index_col=["15min_bins"])
    
    X_train = df.drop(columns="total_pickups")
    y_train = df["total_pickups"]

    transformer = ColumnTransformer(transformers=[
       ("encoder", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"),
       ["day_of_week", "region"])
    ], remainder="passthrough", n_jobs=-1)

    transformer.fit(X_train)
    joblib.dump(transformer,root_dir/"models"/"transformer.joblib")

    X_train_encoded = transformer.transform(X_train)

    lin_reg = LinearRegression()
    lin_reg.fit(X_train_encoded,y_train)

    save_model(lin_reg,root_dir/"models/model.joblib")
    