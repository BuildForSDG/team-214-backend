from datetime import datetime

from .. import db


class FundingDetail(db.Model):
    """FundingDetail Model for storing FundingDetail related details."""

    __tablename__ = "funding_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    documents = db.relationship("Document", backref="funding_detail")

    funding_project_id = db.Column(db.Integer, db.ForeignKey("funding_projects.id"))
    # funding_project = db.relationship("FundingProject", backref="funding_details")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns FundingDetail class representation."""
        return f"<FundingDetail '{self.title}'>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def add_document(self, document):
        self.documents.append(document)
