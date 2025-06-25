import pytest
import joblib
import mlflow
from mlflow.client import MlflowClient
from pathlib import Path
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error

import dagshub
dagshub.init(repo_owner='InshaKhan6593', repo_name='uber-demand-prediction', mlflow=True)

mlflow.set_tracking_uri("https://dagshub.com/InshaKhan6593/uber-demand-prediction.mlflow")

stage = "Staging"
model_name = "uber_demand_prediction"

current_path = Path(__file__)
root_dir = current_path.parent.parent

train_data_path = root_dir/"data"/"processed"/"train.csv"
test_data_path = root_dir/"data"/"processed"/"test.csv"

transformer = joblib.load(root_dir/"models"/"transformer.joblib")
model_uri = f"models:/{model_name}/{stage}"
model = mlflow.sklearn.load_model(model_uri=model_uri)

pipe = Pipeline([
    ("encoder",transformer),
    ("lin_reg",model)
])

@pytest.mark.parametrize(
    argnames="data_path, threshold",
    argvalues=[(train_data_path,0.15),
               (test_data_path,0.15)]
)

def test_performance(data_path,threshold):
    data = pd.read_csv(data_path,parse_dates=["15min_bins"],index_col=["15min_bins"])
    X = data.drop(columns="total_pickups")
    y = data["total_pickups"]

    y_pred = pipe.predict(X)
    error = mean_absolute_percentage_error(y,y_pred)

    assert error <= threshold, f"The model does not pass the performnance threshold of {threshold}"

                                        


