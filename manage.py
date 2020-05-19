"""Application entry point."""

import os
import unittest

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


@manager.command
def run():
    """Runs app from the command line."""
    app.run()


@manager.command
def run_container():
    """Runs app on port PORT from the command line."""
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))


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
