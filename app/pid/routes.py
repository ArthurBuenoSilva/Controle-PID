from flask import jsonify, render_template, request

from app.controller import controller
from app.extensions import socketio
from app.pid import bp
from app.pid.forms import DatasetForm
from app.pid.views import import_dataset_file


@bp.route("/")
def index():
    context = {
        "dataset_form": DatasetForm(),
        "tune_methods": controller.tune_methods,
    }

    return render_template("pid.html", context=context)


@bp.route("/import_datasets", methods=["POST"])
def import_datasets():
    import_dataset_file(request)
    return jsonify(), 200


@socketio.on("plot")
def plot():
    controller.identification_method()
    controller.pid_tune("CHR")


@socketio.on("reloadTune")
def reload_tune(data: dict):
    method = data.get("method")
    overshoot = data.get("overshoot", False)
    lambda_val = data.get("lambda_val", 0)

    try:
        lambda_val = float(lambda_val)
    except ValueError:
        socketio.emit("notify", {"message": "Valor de lambda inválido", "category": "error"})
        return

    controller.pid_tune(method, overshoot, lambda_val)
