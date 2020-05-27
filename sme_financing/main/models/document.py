"""Document database model."""

from datetime import datetime

from .. import db


class Document(db.Model):
    """Document Model for storing Document related details."""

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.String(10), nullable=True)

    sme_id = db.Column(db.Integer, db.ForeignKey("smes.id"), nullable=True)
    # sme = db.relationship("SME", backref="documents")

    funding_detail_id = db.Column(
        db.Integer, db.ForeignKey("funding_details.id"), nullable=True
    )
    # funding_detail = db.relationship("FundingDetail", backref="documents")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<Document '{self.name}'>"
