import uuid
from flask import session
from common.database import Database
from models.booking import Booking
import datetime

class User:
    collection ="user"
    def __init__(self, name, email, password,_id=None):
         self.name = name
         self.email = email
         self.password = password
         self._id = _id or uuid.uuid4().hex

    def json(self):
         return {
                 "name": self.name,
                 "email": self.email,
                 "_id": self._id,
                 "password": self.password
                }


    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one(cls.collection,{"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(cls.collection, {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, name, email, password):
        user = cls.get_by_email(email) #checkifuserexsits
        if user is None:
            new_user = cls(name,email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            #user exists
            return False

    @staticmethod
    def login(user_email):
        #login valid has already been called
        session['email'] = user_email


    @staticmethod
    def logout():
        session['email'] = None


    def get_bookings(self):
        return Database.find("booking", {"user_id": self._id})


    @staticmethod
    def new_booking(screen_id,movie_id,no_of_seats,total_price):
        user_id =session['user_id']
        booking = Booking( user_id ,screen_id,movie_id,no_of_seats,total_price)
        booking.save_to_mongo()

    def save_to_mongo(self):
        Database.insert('user', self.json())