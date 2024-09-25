from flask import render_template

from app.pid import bp


@bp.route("/")
def index():
    return render_template("pid.html")
