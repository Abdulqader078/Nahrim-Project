var chart1  = null;
var chart2 = null;
var chart3 = null;
var visualData = null;
var openmeteoData = null;
var nahrimData = null;

fetch('/rainfall')
    .then(response => response.json())
    .then(function(data) {
        visualData = data;
        buildChart1(data.kedah, data.selangor);
    });

fetch('/rainfall/openmeteo')
    .then(response => response.json())
    .then(function(data) {
        openmeteoData = data;
        buildChart2(data.kedah, data.selangor);
    });

fetch('/rainfall/nahrim')
    .then(response => response.json())
    .then(function(data){
        nahrimData = data;
        buildChart3(data.kedah, data.selangor);
    });
function filterData(arr, interval) {
    return arr.filter((d, i) => i % interval === 0);
}

function buildChart1(kedah, selangor) {
    if (chart1) chart1.destroy();
    chart1 = new Chart(document.getElementById('visualChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: kedah.map(d => d.date),
            datasets: [
                {label: 'Kedah (mm)', data: kedah.map(d => parseFloat(d.rainfall)), borderColor: 'blue', backgroundColor: 'blue',fill: false, tension: 0.1, pointRadius: 2},
                {label: 'Selangor (mm)', data: selangor.map(d => parseFloat(d.rainfall)), borderColor: 'red', backgroundColor: 'red' ,fill: false, tension: 0.1, pointRadius: 2},
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: {title: { display: true, text: 'Visual Crossing Daily Rainfall'}}}
    });
}

function buildChart2(kedah, selangor) {
    if (chart2) chart2.destroy();
    chart2 = new Chart(document.getElementById('openmeteoChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: kedah.map(d => d.date),
            datasets: [
                {label: 'Kedah (mm)', data: kedah.map(d => parseFloat(d.rainfall)), borderColor: 'blue', backgroundColor: 'blue',fill: false, tension: 0.1, pointRadius: 2},
                {label: 'Selangor (mm)', data: selangor.map(d => parseFloat(d.rainfall)), borderColor: 'red', backgroundColor: 'red' ,fill: false, tension: 0.1, pointRadius: 2},
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: {title: { display: true, text: 'Open-Meteo Daily Rainfall'}}}
    });
}

function buildChart3(kedah, selangor) {
    if (chart3) chart3.destroy();
    chart3 = new Chart(document.getElementById('nahrimChart').getContext('2d'), {
        type: 'line',
        data: {
            labels: kedah.map(d => d.date),
            datasets: [
                {label: 'Kedah Average RCP', data: kedah.map(d => parseFloat(d.avg)), borderColor: 'blue', backgroundColor: 'blue',fill: false, tension: 0.1, pointRadius: 2},
                {label: 'Selangor Average RCP', data: selangor.map(d => parseFloat(d.avg)), borderColor: 'red', backgroundColor: 'red' ,fill: false, tension: 0.1, pointRadius: 2},
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: {title: { display: true, text: 'Nahrim Average RCP'}}}
    });
}

function updateCharts() {
    var interval = parseInt(document.getElementById('durationSelect').value);
    if (visualData) buildChart1(filterData(visualData.kedah, interval), filterData(visualData.selangor, interval));
    if (openmeteoData) buildChart2(filterData(openmeteoData.kedah, interval), filterData(openmeteoData.selangor, interval));
    if (nahrimData) buildChart3(filterData(nahrimData.kedah, interval), filterData(nahrimData.selangor, interval));
}