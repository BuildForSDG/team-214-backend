from datetime import datetime

from .. import db


class Investor(db.Model):
    """ Investor Model for storing Investor related details ."""

    __tablename__ = "investors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    postal_address = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    investor_type = db.Column(db.String(255), unique=True, nullable=False)

    # funding_criterion = db.relationship("FundingCriteria", backref="investor")
    # funding_applications = db.relationship(
    #     "FundingApplication",
    #     secondary=funding_application_investors,
    #     backref=db.backref("investors"),
    # )
    # funding_projects = db.relationship("FundingProject", backref="investor")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<Investor '{self.name} - {self.type_of_investor}'>"
