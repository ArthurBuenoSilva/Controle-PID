from flask import Blueprint

bp = Blueprint("pid", __name__)

from app.pid import routes
