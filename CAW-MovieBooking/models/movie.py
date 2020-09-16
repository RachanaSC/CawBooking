import uuid
from typing import Dict,List
from common.database import Database

class Movie:
    collection = "movie"
    def __init__(self,name, description ,_id=None):
        self.name= name
        self.description= description
        self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return{
            '_id': self._id,
            'name': self.name,
            'description': self.description

        }

    def save_to_mongo(self):
        Database.insert(self.collection, self.json())

    @classmethod
    def get_by_id(cls,_id):
        item_json = Database.find_one("movie", {'_id': _id})
        return cls(**item_json)

    @classmethod
    def all(cls)->List:
        items_from_db = Database.find(cls.collection,{})
        #print(items_from_db)
        return [cls(**item) for item in items_from_db]