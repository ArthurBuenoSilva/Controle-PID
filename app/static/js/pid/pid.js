document.addEventListener("DOMContentLoaded", () => {
    const tune = document.getElementById("tune-methods");
    checkTune(tune)

    tune.addEventListener("change", () => {
        checkTune(tune)
    })
})

function checkTune(tune) {
    const overshoot = document.getElementById("with-overshoot");
    const lambda = document.getElementById("lambda");

    if (tune.value === "IMC") {
        lambda.parentElement.classList.remove("hidden");
    } else if (!lambda.parentElement.classList.contains("hidden")) {
        lambda.parentElement.classList.add("hidden");
    }

    if (tune.value === "CHR") {
        overshoot.parentElement.classList.remove("hidden");
    } else if (!overshoot.parentElement.classList.contains("hidden")) {
        overshoot.parentElement.classList.add("hidden");
    }

    overshoot.checked = false;
    lambda.value = 0;
}

socketio.on("chosenMethod", (data) => {
    const method = document.getElementById("method")
    const k = document.getElementById("k");
    const tau = document.getElementById("tau");
    const theta = document.getElementById("theta");

    method.value = data.method;
    k.value = data.k;
    tau.value = data.tau;
    theta.value = data.theta;
})

function activeAfterImport() {
    const tune = document.getElementById("tune-methods");
    const overshoot = document.getElementById("with-overshoot");
    const lambda = document.getElementById("lambda");
    const reloadButton = document.getElementById("reload-tune-button")

    tune.disabled = false;
    overshoot.disabled = false;
    lambda.disabled = false;
    reloadButton.disabled = false;
}