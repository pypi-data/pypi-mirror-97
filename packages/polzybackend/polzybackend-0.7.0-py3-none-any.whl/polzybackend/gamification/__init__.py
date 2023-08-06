from flask import Blueprint

bp = Blueprint('gamification', __name__)

from polzybackend.gamification import routes