from flask import jsonify, render_template, request

from app.pid import bp
from app.pid.forms import DatasetForm
from app.pid.views import import_dataset_file


@bp.route("/")
def index():
    context = {"dataset_form": DatasetForm()}

    return render_template("pid.html", context=context)


@bp.route("/import_datasets", methods=["POST"])
def import_datasets():
    import_dataset_file(request)
    return jsonify(), 200
