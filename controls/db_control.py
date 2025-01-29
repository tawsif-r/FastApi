from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker



class DBControl:
    def __init__(self,db_url:str)->None:
        self.db_url = db_url

    def make_engine(self,Base)->None:
        """This will create the engine 
            with present db
        """
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
    def make_session(self)->None:
        """
        Make a session with the engine
        returns:
            None
        """
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    def make_entry(self,model:object,data:dict):
        """
        Entry to a given table via the data passed

        Args:
            model (class):
            data (dict): A dictionary containing the entries.
                e.g {'fullname': 'tops rops', 'name': 'tops', 'id': 7}
        
        return : none
        """
        self.model = model
        entry = self.model(**data)
        self.session.add(entry)
        self.session.commit()

    def make_entries(self,model:object,data:list)->None:
        """
        Make Entries to a given table via the data passed

        
        Args:
            data (list): e.g data = [{
                                    'fullname':"rozer",
                                    'name':"morgan rozar",
                                    'nickname':"boris"

                                },{
                                    'fullname':"ozer",
                                    'name':"zorgan cozer",
                                    'nickname':'moris'
                                }]
        List of dictionaries containing entity data
            model (class): A class for the table 
        
        Returns:
            None
        """
        self.model = model
        for dict_entry in data:
            entry = self.model(**dict_entry)# unwinding the dictionary
            self.session.add(entry)
            self.session.commit()


   
    def make_query(self, model: object, id: int) -> dict:
        """
        Makes a query fetching an object by its ID.

        Args:
            model (class): Model for mapping the table.
            id (int): The ID of the object to fetch.

        Returns:
            dict: A dictionary representation of the object, or None if not found.
        """
        entry = self.session.query(model).filter_by(id=id).one_or_none()
        if entry:
            return entry.__dict__
        else:
            return None


    def make_query_all(self,model:object)->list:
        """
        makes a qery fetching all the objects

        Args:
            model (class): Model for mapping the table

        Returns: 
            list: A list of objects of the model

        """
        self.entries = []
        for entry in self.session.query(model).all():
            self.entries.append(entry)
        self.entries = [entry.__dict__ for entry in self.entries] # makes the contents dictionary
        return self.entries
    
    def delete_entry(self, model: object, field: str, val) -> str:
        """
        Removes an entry from the table.

        Args:
            model (object): The model class representing the table.
            field (str): The field name to match for removal.
            val (any): The value to match for removal.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            entry = self.session.query(model).filter(getattr(model, field) == val).one_or_none()
            # entry = self.session.query(model).filter(getattr(model, field) == val).all()
            if entry:
                self.session.delete(entry)
                self.session.commit()
                print(f"Entry with {field}={val} removed successfully.")
                return f"Entry with {field}={val} removed successfully."
            else:
                print(f"No entry found with {field}={val}.")
                return f"No entry found with {field}={val}."
        except Exception as e:
            self.session.rollback()
            return f"An error occurred: {str(e)}"



    def update_query(self, model: object, id: int, data: dict) -> str:
        """
        Updates an entry in the table.

        Args:
            model (class): Model for mapping the table.
            id (int): The ID of the object to update.
            data (dict): A dictionary containing the fields to update and their new values.

        Returns:
            str: A message indicating the result of the operation.
        """
        try:
            entry = self.session.query(model).filter_by(id=id).one_or_none()
            if entry:
                for key, value in data.items():
                    setattr(entry, key, value)
                self.session.commit()
                return f"Entry with id={id} updated successfully."
            else:
                return f"No entry found with id={id}."
        except Exception as e:
            self.session.rollback()
            return f"An error occurred: {str(e)}"


    def make_redis_worthy(self,data:list,fields:list=None)->list:
        """
        Filter data to include only specified fields.
        
        Args:
            data (list): List of dictionaries containing entity data
            fields (list, optional): List of field names to include in filtered data.
                                If None, defaults to ['fullname', 'name', 'id']
        
        Returns:
            list: Filtered data containing only specified fields
        """
        if fields is None:
            fields = ['fullname', 'name', 'id']
        
        filtered_data = []
        for entity in data:
            filtered_entity = {
                field: entity[field]
                for field in fields
                if field in entity
            }
            filtered_data.append(filtered_entity)
        
        return filtered_data










