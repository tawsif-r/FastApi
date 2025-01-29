from controls.db_control import *
from controls.redis_control import *
from pydantic_models import *
from models import * 
from connection import DATABASE_URL




db = DBControl(DATABASE_URL)
db.make_engine(Base)
db.make_session()
# db.make_entry(Feature,{'name':'bed','description':'The patient will recieve bed facilities','price':1200.0,'is_active':True})
