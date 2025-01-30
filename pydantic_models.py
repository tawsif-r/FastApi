from datetime import datetime
from pydantic import BaseModel


class Features(BaseModel):
    id :int
    name : str
    description :str
    price : float
    is_active : bool

class FeatureUpdate(BaseModel):
    name : str
    description: str
    price : float
    is_active: bool

class CreateFeature(BaseModel):
    name : str
    description: str
    price : float
    is_active: bool
