from datetime import datetime
from enum import Enum

from .. import db


class EducationLevel(Enum):
    doctorate_degree = "Doctorate Degree"
    masters_degree = "Masters Degree"
    bachelors_degree = "Bachelors Degree"
    hnd = "HND"


class Client(db.Model):
    """Client Model for storing client related details."""

    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    postal_address = db.Column(db.String(255), nullable=True)
    residential_address = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    education_level = db.Column(
        db.Enum(EducationLevel, values_callable=lambda obj: [el.value for el in obj]),
        nullable=False,
        default=EducationLevel.bachelors_degree.value,
    )
    position = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    user = db.relationship("User", backref="client")

    smes = db.relationship("SME", backref="client", lazy="dynamic")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<Client '{self.lastname} {self.firstname}'>"
