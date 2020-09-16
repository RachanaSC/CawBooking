import uuid
from typing import Dict,List
from common.database import Database

class Screen:
    collection = "screen"
    def __init__(self, price, movie_id, city, total_seats, booked_seats, start_time, end_time, isfull,_id=None):
        self.isfull = isfull
        self.price = price
        self.movie_id = movie_id
        self.total_seats = total_seats
        self.booked_seats = booked_seats
        self.city = city
        self.start_time = start_time
        self.end_time = end_time
        self._id = _id or uuid.uuid4().hex

    def json(self) -> Dict:
        return{
            '_id': self._id,
            'movie_id': self.movie_id,
            'total_seats': self.total_seats,
            'booked_seats': self.booked_seats,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'price': self.price,
            'isfull': self.isfull,
            'city': self.city
        }

    def save_to_mongo(self):
        Database.insert(self.collection, self.json())


    def update_seats(seats):
       return Database.update("screen", {'_id': _id})


    @classmethod
    def get_by_id(cls, id):
        item_json = Database.find_one(cls.collection,{'_id': id})
        return cls(**item_json)

    @classmethod
    def get_by_city(cls, city):
        item_json = Database.find(cls.collection, {'city': city})
        return [cls(**item) for item in item_json]

    @classmethod
    def update_seats(cls,id, seats):
        return Database.update(cls.collection,{'_id': id},{'booked_seats': seats})


    @classmethod
    def all(cls)->List:
        items_from_db = Database.find(cls.collection,{})
        return [cls(**item) for item in items_from_db]