from fastapi import FastAPI
from controls.db_control import *
from controls.redis_control import *
from pydantic_models import *
from models import * 
from connection import DATABASE_URL
from db_query import db
import uvicorn



app = FastAPI()






@app.get("/")
def get_features():
    features = db.make_query_all(Feature)
    return {"features": features}

@app.post("/update_feature/")
def update_features(feature_id: int, feature_data: FeatureUpdate):
    # get the feature matching the feature id
    feature = db.make_query(Feature, feature_id) 
    if feature:
        # Convert the Pydantic model to a dict preparing for dumping into model
        update_data = feature_data.model_dump()
        result = db.update_query(Feature, feature_id, update_data)
        return {"message": result}
    else:
        return {"error": "Feature not found"}

@app.post("/add_feature/")
def add_feature(feature_data: CreateFeature):
    # Convert the Pydantic model to a dict preparing for dumping into model
    new_feature_data = feature_data.model_dump()
    result = db.make_entry(Feature,new_feature_data)
    return {"message": result}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)