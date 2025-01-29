from pydantic import BaseModel


class features(BaseModel):
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
