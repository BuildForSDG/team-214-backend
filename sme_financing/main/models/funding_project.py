from datetime import datetime

from .. import db


class FundingProject(db.Model):
    """FundingProject Model for storing FundingProject related details."""

    __tablename__ = "funding_projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(15), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    relevance = db.Column(db.Text, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    justification = db.Column(db.Text, nullable=False)
    work_plan = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    fund_amount = db.Column(db.Float, nullable=False)

    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    funding_application_id = db.Column(
        db.Integer, db.ForeignKey("funding_applications.id")
    )
    # funding_application = db.relationship(
    #     "FundingApplication", backref="funding_projects"
    # )

    investor_id = db.Column(db.Integer, db.ForeignKey("investors.id"))
    # investor = db.relationship("Investor", backref="funding_projects")

    funding_details = db.relationship("FundingDetail", backref="funding_project")
    fund_disbursements = db.relationship("FundDisbursement", backref="funding_project")
    project_milestones = db.relationship("ProjectMilestone", backref="funding_project")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """Returns this class representation."""
        return f"<FundingProject '{self.name} - {self.status}'>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def add_funding_detail(self, funding_detail):
        self.funding_details.append(funding_detail)
