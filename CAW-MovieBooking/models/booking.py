import uuid
from typing import Dict,List
from common.database import Database

class Booking:
    collection = "booking"
    def __init__(self,user_id,screen_id,movie_id,moviename,no_of_seats,total_price,_id:str=None):
        self._id =_id or uuid.uuid4().hex
        self.user_id = user_id
        self.screen_id = screen_id
        self.movie_id =  movie_id
        self.moviename = moviename
        self.no_of_seats = no_of_seats
        self.total_price = total_price


    def json(self)->Dict:
      return{
          "_id": self._id,
          "user_id": self.user_id,
          "screen_id": self.screen_id,
          "movie_id": self.movie_id,
          "moviename":self.moviename,
          "no_of_seats": self.no_of_seats,
          "total_price": self.total_price
      }

    def save_to_mongo(self):
        Database.insert(self.collection,self.json())

    @classmethod
    def get_by_id(cls, _id):
        item_json = Database.find_one("booking", {'_id': _id})
        return cls(**item_json)

    @classmethod
    def all(cls) -> List:
        items_from_db = Database.find(cls.collection, {})
        return [cls(**item) for item in items_from_db]

    @classmethod
    def user_all(cls,_id)->List:
       from_db = Database.find(cls.collection, {"user_id":_id})
       return [cls(**user) for user in from_db]