from flask import Blueprint

bp = Blueprint('auth', __name__)

from polzybackend.authenticate import routes