from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth
import os
from polzybackend.messenger import Messenger
import flask_monitoringdashboard as dashboard


# initialization
db = SQLAlchemy()
migrate = Migrate()
auth = HTTPTokenAuth(scheme='Bearer')
messenger = Messenger()


def create_app(config=None):
    # create application
    app = Flask(__name__)
    # set default config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='secret!key')
    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'polzy.db'),
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config)

    # policy store
    app.config['POLICIES'] = {}
    app.config['ANTRAGS'] = {}

    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from polzybackend.authenticate import bp as bp_auth
    app.register_blueprint(bp_auth)

    from polzybackend.general import bp as bp_general
    app.register_blueprint(bp_general)

    from polzybackend.policy import bp as bp_policy
    app.register_blueprint(bp_policy)

    from polzybackend.antrag import bp as bp_antrag
    app.register_blueprint(bp_antrag)

    from polzybackend.administration import bp as bp_admin
    app.register_blueprint(bp_admin)

    from polzybackend.gamification import bp as bp_gamification
    app.register_blueprint(bp_gamification)

    from polzybackend.announce import bp as bp_announce
    app.register_blueprint(bp_announce)

    # -----------> DEBUG BLUEPRINT
    from polzybackend.debug import bp as bpDebug
    app.register_blueprint(bpDebug)

    # setup monitoring dashboard
    if app.config.get('DASHBOARD_CONFIG'):
        dashboard.config.init_from(file=app.config['DASHBOARD_CONFIG'])
    if app.config.get('DASHBOARD_DATABASE_URI'):
        dashboard.config.database_name = app.config['DASHBOARD_DATABASE_URI']
    dashboard.bind(app)

    return app


from polzybackend import models
