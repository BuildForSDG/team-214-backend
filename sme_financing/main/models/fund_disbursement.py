from datetime import datetime

from .. import db


class FundDisbursement(db.Model):
    """FundingProject Model for storing  FundingProject related details."""

    __tablename__ = "fund_disbursements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    disbursement_date = db.Column(db.DateTime, nullable=False)
    bank_account_details_from = db.Column(db.String(255), nullable=True)
    bank_account_details_to = db.Column(db.String(255), nullable=True)
    cheque_details = db.Column(db.String(255), nullable=True)

    funding_project_id = db.Column(db.Integer, db.ForeignKey("funding_projects.id"))
    # funding_project=db.relationship("FundingProject",backref="funding_disbursements")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<FundDisbursement '{self.disbursement_date} - {self.status}'>"
