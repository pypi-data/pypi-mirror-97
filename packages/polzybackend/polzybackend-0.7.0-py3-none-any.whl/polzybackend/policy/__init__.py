from flask import Blueprint

bp = Blueprint('policy', __name__)

from polzybackend.policy import routes