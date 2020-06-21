from datetime import datetime

from .. import db


class ProjectMilestone(db.Model):
    """ProjectMilestone Model for storing ProjectMilestone related details."""

    __tablename__ = "project_milestones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    funding_project_id = db.Column(db.Integer, db.ForeignKey("funding_projects.id"))
    funding_project = db.relationship("FundingProject", backref="project_milestones")

    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ProjectMilestone '{self.title} - {self.status}'>"
