from datetime import datetime
from .. import db


class FundingProject(db.Model):
    """ FundingProject Model for storing FundingProject related details """

    __tablename__ = "funding_projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end = db.Column(db.DateTime, nullable=True)

    funding_application_id = db.Column(
        db.Integer, db.ForeignKey("funding_applications.id")
    )
    funding_application = db.relationship(
        "FundingApplication", backref="funding_projects"
    )

    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"))
    investor = db.relationship("Investor", backref="funding_projects")

    # funding_details = db.relationship("FundingDetail", backref="funding_project")
    # fund_disbursements = db.relationship("FundDisbursement",backref="funding_project")
    # project_milestones = db.relationship("ProjectMilestone",backref="funding_project")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FundingProject '{self.name} - {self.status}'>"
