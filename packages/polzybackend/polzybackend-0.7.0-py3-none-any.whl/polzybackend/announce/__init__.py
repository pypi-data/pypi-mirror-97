from flask import Blueprint

bp = Blueprint('announce', __name__)

from polzybackend.announce import routes