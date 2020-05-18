from datetime import datetime

from .. import db


class SME(db.Model):
    """ SME Model for storing SME related details """

    __tablename__ = "smes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    postal_address = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    telephone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    sector = db.Column(db.String(255), nullable=False)
    principal_product_service = db.Column(db.String(255), nullable=False)
    other_product_service = db.Column(db.String(255), nullable=True)
    age = db.Column(db.String(50), nullable=False)
    establishment_date = db.Column(db.DateTime, nullable=True)
    ownership_type = db.Column(db.String(50), nullable=False)
    bank_account_details = db.Column(db.String(255), nullable=True)
    employees_number = db.Column(db.Integer, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    # documents = db.relationship("Document", backref="sme")
    # funding_applications = db.relationship("FundingApplication", backref="sme")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<SME {self.name}>"
