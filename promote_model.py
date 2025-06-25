import mlflow
from mlflow.client import MlflowClient

import dagshub
dagshub.init(repo_owner='InshaKhan6593', repo_name='uber-demand-prediction', mlflow=True)

mlflow.set_tracking_uri("https://dagshub.com/InshaKhan6593/uber-demand-prediction.mlflow")

model_name = "uber_demand_prediction"
promote_stage = "Production"
client = MlflowClient()

latest_versions = client.get_latest_versions(name = model_name,stages=["Staging"])
latest_version = latest_versions[0].version


client.transition_model_version_stage(
    name = model_name,
    version = latest_version,
    stage = promote_stage,
    archive_existing_versions=True
)