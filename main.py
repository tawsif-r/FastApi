from fastapi import FastAPI
from controls.db_control import *
from controls.redis_control import *
from pydantic_models import *
from models import * 
from connection import DATABASE_URL
from db_query import db
import uvicorn



app = FastAPI()




features = db.make_query_all(Feature)

@app.get("/")
def get_features():
    return {"features": features}

@app.post("/update_feature/")
def update_features(feature_id: int, feature_data: FeatureUpdate):
    feature = db.make_query(Feature, feature_id)
    if feature:
        for key, value in feature_data.items():
            setattr(feature, key, value)
        db.update_query(Feature,feature)
        return {"message": "Feature updated successfully"}
    else:
        return {"error": "Feature not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)