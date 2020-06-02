from datetime import datetime

from .. import db


class FundingApplicationInvestor(db.Model):
    """FundingApplicationInvestor Model for storing the
    Investors interested in FundingApplication.
    """

    __tablename__ = "funding_application_investors"

    funding_application_id = db.Column(
        db.Integer, db.ForeignKey("funding_applications.id"), primary_key=True
    )
    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"), primary_key=True)
    message = db.Column(db.Text)
    funding_application = db.relationship(
        "FundingApplication",
        backref=db.backref(
            "funding_application_investors", cascade="all, delete-orphan"
        ),
    )
    investor = db.relationship(
        "Investor",
        backref=db.backref(
            "funding_application_investors", cascade="all, delete-orphan"
        ),
    )
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, funding_application=None, investor=None, message=None):
        self.funding_application = funding_application
        self.investor = investor
        self.message = message

    def __repr__(self):
        """Returns this class representation."""
        return f"""<FundingApplicationInvestor
                '{self.funding_application_id} - {self.investor_id}'>"""


class FundingApplication(db.Model):
    """FundingApplication Model for storing related details."""

    __tablename__ = "funding_applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    sme_id = db.Column(db.Integer, db.ForeignKey("smes.id"))
    sme = db.relationship("SME", backref="funding_applications")

    investors = db.relationship(
        "Investor", secondary="funding_application_investors", viewonly=True
    )
    funding_projects = db.relationship("FundingProject", backref="funding_application")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def add_investors(self, list_investors):
        for investor, message in list_investors:
            self.funding_application_investors.append(
                FundingApplicationInvestor(
                    funding_application=self, investor=investor, message=message
                )
            )

    def add_investor(self, investor, investor_message):
        fai = FundingApplicationInvestor(
            funding_application=self, investor=investor, message=investor_message
        )
        self.funding_application_investors.append(fai)

    def __repr__(self):
        """Returns this class representation."""
        return f"<FundingApplication '{self.name} - {self.status}'>"
