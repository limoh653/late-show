from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class Episode(db.Model,SerializerMixin):

    serialize_rules=('-appearance.episode',)
    __tablename__='episodes'

    id= db.Column(db.Integer,primary_key=True)
    date= db.Column(db.String)
    number= db.Column(db.Integer)

    appearance =db.relationship('Appearance',back_populates='episode')

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }

class Guest(db.Model,SerializerMixin):

    serialize_rules=('-appearance.guest',)

    __tablename__='guests'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    occupation= db.Column(db.String)

    appearance=db.relationship('Appearance',back_populates='guest')

class Appearance(db.Model,SerializerMixin):

    serialize_rules=('-episode.appearance','-guest.appearance')

    __tablename__='appearances'

    id= db.Column(db.Integer,primary_key=True)
    rating=db.Column(db.Integer,nullable=False)
    episode_id=db.Column(db.Integer,db.ForeignKey('episodes.id'),nullable=False)
    guest_id=db.Column(db.Integer,db.ForeignKey('guests.id'),nullable=False)

    episode=db.relationship('Episode',back_populates='appearance')
    guest=db.relationship('Guest',back_populates='appearance')

    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError('Rating must be between 1 and 5 (inclusive).')
        return rating