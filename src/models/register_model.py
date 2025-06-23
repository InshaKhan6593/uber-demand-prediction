import dagshub
import mlflow
from mlflow.client import MlflowClient
import json

mlflow.set_tracking_uri("https://dagshub.com/InshaKhan6593/uber-demand-prediction.mlflow")
import dagshub
dagshub.init(repo_owner='InshaKhan6593', repo_name='uber-demand-prediction', mlflow=True)

with open("run_information.json","r") as file:
    model_info = json.load(file)


model_uri = model_info["model_uri"]

version = mlflow.register_model(model_uri=model_uri,name="uber_demand_prediction")

client = MlflowClient()

stage = "Staging"

client.transition_model_version_stage(
    name = version.name,
    version = version.version,
    stage = stage,
    archive_existing_versions=False
)

