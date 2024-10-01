import os
from typing import Literal

from werkzeug.utils import secure_filename

from app import socketio
from app.controller import controller
from configuration import DATASETS_FOLDER, clear_folder


def verify_extension(file) -> bool:
    """Verify file extension

    :param file: File name to be checked
    :return: True if the file extension is valid, False otherwise
    """
    valid_extensions = [".mat"]
    name, extension = os.path.splitext(file)
    return extension in valid_extensions


def import_dataset_file(request):
    """Import the dataset

    :param request: Flask request
    """
    try:
        if "dataset" in request.files:
            file = request.files.get("dataset")

            # Clear dataset folder
            clear_folder(DATASETS_FOLDER)

            filename = secure_filename(file.filename)

            if verify_extension(filename):
                filepath = os.path.join(DATASETS_FOLDER, filename)
                file.save(filepath)
                controller.dataset = filepath
            else:
                notify("Apenas arquivos .mat são permitidos", "error")
                return

            notify("Dataset importado com sucesso")
        else:
            notify("Sem dataset para importar", "warning")
    except Exception as e:
        notify(f"Erro inesperado {e}", "error")
        clear_folder(DATASETS_FOLDER)


def notify(message: str, category: Literal["success", "warning", "error"] = "success"):
    """Send a notification through socket io to the frontend

    :param message: Notification message
    :param category: If is a notification of success, warning or error
    """
    socketio.emit("notify", {"message": message, "category": category})
