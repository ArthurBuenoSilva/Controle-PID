let openLoopChart = null;
let closeLoopChart = null;
let pidChart = null;

const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            ticks: {
                callback: function(value) {
                    return parseFloat(value).toFixed(1);
                }
            }
        }
    },
    plugins: {
        title: {
            display: true,
            text: "",
            color: "#FFF",
            font: {
                weight: "bold",
            }
        }
    }
}

socketio.on("plotIdentificationMethod", (data) => {
    plotOpenLoop(data)
    plotCloseLoop(data)
})

function plotOpenLoop(data) {
    const ctx = document.getElementById('open-loop');

    const power = data.power;
    const smith = data.smith.openLoop;
    const sundaresan = data.sundaresan.openLoop;

    if (openLoopChart) {
        openLoopChart.data.labels = smith.time;
        openLoopChart.data.datasets[0].data = smith.response;
        openLoopChart.data.datasets[1].data = sundaresan.response;
        openLoopChart.update();
        return
    }

    openLoopChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: smith.time,
            datasets: [
                {
                    label: "Power",
                    data: power,
                    borderWidth: 1,
                    pointBorderWidth: 1,
                },
                {
                    label: "Smith",
                    data: smith.response,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
                {
                    label: "Sundaresan",
                    data: sundaresan.response,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
            ]
        },
        options: {
            ...options,
            plugins: {
                title: {
                    display: true,
                    text: "Malha Aberta",
                    color: "#FFF",
                    font: {
                        weight: "bold",
                    }
                }
            }
        },
    });
}

function plotCloseLoop(data) {
    const ctx = document.getElementById('close-loop');

    const power = data.power;
    const smith = data.smith.closeLoop;
    const sundaresan = data.sundaresan.closeLoop;

    if (closeLoopChart) {
        closeLoopChart.data.labels = smith.time;
        closeLoopChart.data.datasets[0].data = smith.response;
        closeLoopChart.data.datasets[1].data = sundaresan.response;
        closeLoopChart.update();
        return
    }

    closeLoopChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: smith.time,
            datasets: [
                {
                    label: "Power",
                    data: power,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
                {
                    label: "Smith",
                    data: smith.response,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
                {
                    label: "Sundaresan",
                    data: sundaresan.response,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
            ]
        },
        options: {
            ...options,
            plugins: {
                title: {
                    display: true,
                    text: "Malha Fechada",
                    color: "#FFF",
                    font: {
                        weight: "bold",
                    }
                }
            }
        },
    });
}

socketio.on("tune", (data) => {
    const method = data.method;
    const time = data.time;
    const response = data.response;
    const k = data.k;
    const tau = data.tau;
    const theta = data.theta;
    const kp = data.kp;
    const ti = data.ti;
    const td = data.td;
    const overshoot = data.overshoot;
    const rise_time = data.rise_time;

    plotTune(method, time, response);
    fillPIDParams(k, tau, theta, kp, ti, td, overshoot, rise_time);
})

function plotTune(method, time, response) {
    const ctx = document.getElementById('pid-tune');

    if (pidChart) {
        pidChart.data.labels = time;
        pidChart.data.datasets[0].label = method;
        pidChart.data.datasets[0].data = response;
        pidChart.options.plugins.title.text = method;
        pidChart.update();
        return
    }

    pidChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: time,
            datasets: [
                {
                    label: method,
                    data: response,
                    borderWidth: 1,
                    pointBorderWidth: 1
                },
            ]
        },
        options: {
            ...options,
            plugins: {
                title: {
                    display: true,
                    text: method,
                    color: "#FFF",
                    font: {
                        weight: "bold",
                    }
                },
                legend: {
                    display: false,
                }
            },
        },
    });
}

function reloadTune() {
    const method = document.getElementById("method");
    const tune = document.getElementById("tune-methods");
    const pade = document.getElementById("pade");
    const overshoot = document.getElementById("with-overshoot");
    const lambda = document.getElementById("lambda");

    const kp_input = document.getElementById("kp");
    const ti_input = document.getElementById("ti");
    const td_input = document.getElementById("td");

    socketio.emit("reloadTune", {
        "identification": method.value,
        "method": tune.value,
        "pade": pade.value,
        "overshoot": overshoot.checked,
        "lambda_val": lambda.value,
        "kp": kp_input.value,
        "ti": ti_input.value,
        "td": td_input.value
    })
}

function fillPIDParams(k, tau, theta, kp, ti, td, overshoot, rise_time) {
    const k_input = document.getElementById("k");
    const tau_input = document.getElementById("tau");
    const theta_input = document.getElementById("theta");
    const kp_input = document.getElementById("kp");
    const ti_input = document.getElementById("ti");
    const td_input = document.getElementById("td");
    const overshoot_input = document.getElementById("overshoot");
    const rise_time_input = document.getElementById("rise-time");

    k_input.value = k;
    tau_input.value = tau;
    theta_input.value = theta;
    kp_input.value = kp;
    ti_input.value = ti;
    td_input.value = td;
    overshoot_input.value = `${overshoot} (%)`;
    rise_time_input.value = `${rise_time} (ms)`;
}