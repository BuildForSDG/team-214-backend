from datetime import datetime

from .. import db

funding_application_investors = db.Table(
    "funding_application_investors",
    db.Column(
        "funding_application_id", db.Integer, db.ForeignKey("funding_applications.id")
    ),
    db.Column("investor_id", db.Integer, db.ForeignKey("investors.id")),
)


class FundingApplication(db.Model):
    """FundingApplication Model for storing related details."""

    __tablename__ = "funding_applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    sme_id = db.Column(db.Integer, db.ForeignKey("smes.id"))
    sme = db.relationship("SME", backref="funding_applications")

    investors = db.relationship(
        "Investor",
        secondary=funding_application_investors,
        backref=db.backref("funding_applications"),
    )
    funding_projects = db.relationship("FundingProject", backref="funding_application")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<FundingApplication '{self.name} - {self.status}'>"
