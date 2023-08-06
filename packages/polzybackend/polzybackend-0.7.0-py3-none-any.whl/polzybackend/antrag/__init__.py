from flask import Blueprint

bp = Blueprint('antrag', __name__)

from polzybackend.antrag import routes