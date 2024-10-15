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
    controller.identification_method("smith")
    controller.pid_tune("smith", "CHR")


@socketio.on("reloadTune")
def reload_tune(data: dict):
    identification = data.get("identification")
    method = data.get("method")
    pade = data.get("pade", 20)
    overshoot = data.get("overshoot", False)
    lambda_val = data.get("lambda_val", 0)

    try:
        pade = int(pade)
    except ValueError:
        socketio.emit("notify", {"message": "Valor de pade inválido", "category": "error"})
        return

    try:
        lambda_val = float(lambda_val)
    except ValueError:
        socketio.emit("notify", {"message": "Valor de lambda inválido", "category": "error"})
        return

    if method == "Manual":
        kp = data.get("kp")
        ti = data.get("ti")
        td = data.get("td")

        try:
            kp = float(kp)
        except ValueError:
            socketio.emit("notify", {"message": "Valor de Kp inválido", "category": "error"})
            return

        try:
            ti = float(ti)
        except ValueError:
            socketio.emit("notify", {"message": "Valor de Ti inválido", "category": "error"})
            return

        try:
            td = float(td)
        except ValueError:
            socketio.emit("notify", {"message": "Valor de Td inválido", "category": "error"})
            return

        controller.manual_pid_tune(identification, pade, kp, ti, td)
    else:
        controller.pid_tune(identification, method, pade, overshoot, lambda_val)
