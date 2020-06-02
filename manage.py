"""Application entry point."""

import os
import unittest
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from sme_financing.main import create_app, db
from sme_financing.main.api_v1 import blueprint as api_v1
from sme_financing.main.models import (
    client,
    document,
    fund_disbursement,
    funding_application,
    funding_criteria,
    funding_detail,
    funding_project,
    investor,
    project_milestone,
    sme,
    user,
)

app = create_app(os.getenv("FLASK_ENV") or "development")

app.register_blueprint(api_v1)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)


@app.before_first_request
def create_tables():
    db.create_all()


@manager.command
def insert():
    db.session.add(
        user.User(
            email="herve@gmail.com",
            active=True,
            admin=False,
            public_id="herve",
            username="herve",
        )
    )
    db.session.add(
        client.Client(
            lastname="herve",
            firstname="herve",
            gender="male",
            postal_address="12 po box 78",
            residential_address="Accra",
            telephone="+233358569587",
            nationality="Ghana",
            education_level="Masters Degree",
            position="CTO",
            user_id=1,
        )
    )
    db.session.add(
        sme.SME(
            name="Short stay Accra",
            postal_address="12 po box 78",
            location="Accra",
            telephone="+23369584587",
            email="stay@gmail.com",
            description="Yeah it''s a hotel",
            sector="Hotel Business",
            principal_product_service="Hotel",
            other_product_service="Restaurant",
            age="More than 24 months",
            establishment_date=datetime.strptime("2019-07-11", "%Y-%m-%d").date(),
            ownership_type="LLC",
            bank_account_details="789568521524",
            employees_number="24",
            client_id=1,
        )
    )
    db.session.add(
        funding_application.FundingApplication(
            name="Cool Funding Application 233235", status="Active", sme_id=1
        )
    )
    db.session.add(
        investor.Investor(
            name="Bank of Africa",
            postal_address="12 PO BO",
            street_address="25 STreet",
            city="Accra",
            telephone="+23358696584",
            email="boa@gmail.com",
            investor_type="Bank",
        )
    )
    db.session.commit()


@manager.command
def run():
    """Runs app from the command line."""
    app.run()


# @manager.command
# def run_container():
#     """Runs app on port PORT from the command line."""
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover("tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
