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
    const kp_input = document.getElementById("kp");
    const ti_input = document.getElementById("ti");
    const td_input = document.getElementById("td");

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

    if (tune.value === "Manual") {
        kp_input.disabled = false;
        ti_input.disabled = false;
        td_input.disabled = false;
    } else if (!kp_input.disabled) {
        kp_input.disabled = true;
        ti_input.disabled = true;
        td_input.disabled = true;
    }

    overshoot.checked = false;
    lambda.value = 0;
}

socketio.on("chosenMethod", (data) => {
    const k = document.getElementById("k");
    const tau = document.getElementById("tau");
    const theta = document.getElementById("theta");
    const smith_ol_mse = document.getElementById("smith-ol-mse");
    const smith_cl_mse = document.getElementById("smith-cl-mse");
    const sundaresan_ol_mse = document.getElementById("sundaresan-ol-mse");
    const sundaresan_cl_mse = document.getElementById("sundaresan-cl-mse");

    k.value = data.k;
    tau.value = data.tau;
    theta.value = data.theta;
    smith_ol_mse.value = data.smith_ol_mse;
    smith_cl_mse.value = data.smith_cl_mse;
    sundaresan_ol_mse.value = data.sundaresan_ol_mse;
    sundaresan_cl_mse.value = data.sundaresan_cl_mse;

    smith_ol_mse.dispatchEvent(new Event("change"));
    sundaresan_ol_mse.dispatchEvent(new Event("change"));
})

function activeAfterImport() {
    const identificationMethod = document.getElementById("method");
    const tune = document.getElementById("tune-methods");
    const pade = document.getElementById("pade");
    const overshoot = document.getElementById("with-overshoot");
    const lambda = document.getElementById("lambda");
    const reloadButton = document.getElementById("reload-tune-button")
    const downloadButton = document.getElementById("save-charts")

    pade.disabled = false;
    identificationMethod.disabled = false;
    tune.disabled = false;
    overshoot.disabled = false;
    lambda.disabled = false;
    reloadButton.disabled = false;
    downloadButton.disabled = false;
}

function downloadChart(chartId, fileName) {
    const canvas = document.getElementById(chartId);
    const dataUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = fileName;
    link.click();
}

function saveCharts() {
    downloadChart("open-loop", "malha_aberta.png");
    downloadChart("close-loop", "malha_fechada.png");
    downloadChart("pid-tune", "pid.png");
}