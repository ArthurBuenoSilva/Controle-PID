const socketio = io();
const input_file = document.getElementById("dataset");

function click_on_datasets_input() {
    input_file.click();
}

function import_dataset() {
    const form = document.getElementById("datasetsForm");
    const formData = new FormData(form);

    fetch("/import_datasets", {
        method: "POST",
        body: formData,
    })
        .then(() => {
            form.reset();
            socketio.emit("plot", (response) => {
                activeAfterImport();
            });
        })
        .catch(error => console.log(error));
}

socketio.on("notify", (data) => {
    notify(data.message, data.category);
})
