import pandas as pd
from pathlib import Path
import joblib
import mlflow
from sklearn.metrics import mean_absolute_percentage_error
import json

import dagshub
dagshub.init(repo_owner='InshaKhan6593', repo_name='uber-demand-prediction', mlflow=True)

mlflow.set_tracking_uri("https://dagshub.com/InshaKhan6593/uber-demand-prediction.mlflow")

mlflow.set_experiment("DVC pipeline")

def save_run_information(run_id,artifact_path,model_uri,path):
    run_information = {
        "run_id": run_id,
        "artifact_path": artifact_path,
        "model_uri": model_uri
    }

    with open(path,"w") as file:
        json.dump(run_information,file,indent=4)

if __name__ == "__main__":
    current_path = Path(__file__)
    root_dir = current_path.parent.parent.parent
    
    data_path = root_dir/"data"/"processed"

    test_df = pd.read_csv(data_path/"test.csv",parse_dates=["15min_bins"]
                          ,index_col="15min_bins")
    
    X_test = test_df.drop(columns="total_pickups")
    y_test = test_df["total_pickups"]

    transformer = joblib.load(root_dir/"models"/"transformer.joblib")

    X_test_encoded = transformer.transform(X_test)

    model = joblib.load(root_dir/"models"/"model.joblib")

    y_pred = model.predict(X_test_encoded)

    loss = mean_absolute_percentage_error(y_test,y_pred)

    with mlflow.start_run(run_name="model"):    
        # log the model parameters
        mlflow.log_params(model.get_params())
        
        # log the mertic
        mlflow.log_metric("MAPE", loss)
        
        # converts the datasets into mlfow datasets
        training_data = mlflow.data.from_pandas(pd.read_csv(data_path/"train.csv", parse_dates=["15min_bins"]).set_index("15min_bins"), targets="total_pickups")
        
        validation_data = mlflow.data.from_pandas(pd.read_csv(data_path/"test.csv", parse_dates=["15min_bins"]).set_index("15min_bins"), targets="total_pickups")
        
        # log the datasets
        mlflow.log_input(training_data, context="training")
        mlflow.log_input(validation_data, context="validation")
        
        # model signature
        model_signature = mlflow.models.infer_signature(X_test_encoded, y_pred)
        
        # log sklearn model
        logged_model = mlflow.sklearn.log_model(model, "demand_prediction", 
                                 signature=model_signature,
                                 pip_requirements="requirements.txt")
        

    run_id = logged_model.run_id
    artifact_path = logged_model.artifact_path
    model_uri = logged_model.model_uri 

    json_file_save_path = root_dir / "run_information.json"
    save_run_information(run_id=run_id,
                         artifact_path=artifact_path,
                         model_uri=model_uri,
                         path=json_file_save_path)
    