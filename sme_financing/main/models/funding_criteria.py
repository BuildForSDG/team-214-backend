from datetime import datetime

from .. import db


class FundingCriteria(db.Model):
    """FundingCriteria Model for storing FundingCriteria related details."""

    __tablename__ = "funding_criteria"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"))
    # investor = db.relationship("Investor", backref="funding_criterion")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<FundingCriteria '{self.name}'>"
