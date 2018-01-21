import random
from datetime import timedelta, datetime
from google.appengine.ext import ndb
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired 
from slugify import slugify

SECONDS_PER_DAY = 24*60*60
MAX_AGE = 7 * SECONDS_PER_DAY # 1week

class Raffle(ndb.Model):
    choices = ndb.StringProperty(repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    max_age = ndb.IntegerProperty()
    result = ndb.StringProperty()
    
    @classmethod
    def get_key(cls, raffle_id):
        return ndb.key(cls, raffle_id)

    @classmethod
    def create(cls, raffle_id, choices):
        raffle_id = slugify(raffle_id)
        if cls.retrieve(raffle_id) is not None:
            raise Exception("raffle already exists")
        key = cls.get_key(raffle_id)
        result = random.choice(choices)
        raffle = cls(choices=choices, result=result, key=key)
        raffle.put()
        return raffle

    @classmethod
    def retrieve(cls, raffle_id):
        key = cls.get_key(raffle_id)
        raffle = key.get()
        if raffle is not None and raffle.expired:
            raffle.delete()
            return None
        return raffle

    @property
    def expiry(self):
        return self.timestamp + timedelta(seconds=self.max_age)

    @property
    def expired(self):
        return datetime.utcnow() > self.expiry