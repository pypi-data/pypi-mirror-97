from flask import Blueprint

bp = Blueprint('general', __name__)

from polzybackend.general import routes