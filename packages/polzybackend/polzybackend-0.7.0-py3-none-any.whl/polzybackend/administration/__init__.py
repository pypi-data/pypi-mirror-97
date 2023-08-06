from flask import Blueprint

bp = Blueprint('admin', __name__)

from polzybackend.administration import routes