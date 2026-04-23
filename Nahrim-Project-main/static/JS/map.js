const mapKedah = L.map("map", {
    minZoom: 5,
    maxZoom: 18,
    maxBounds: [[1.0, 99.0], [6.5, 104.5]],
    maxBoundsViscosity: 1.0
}).setView([6.12, 100.37], 9)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapKedah);

const mapSelangor = L.map("map2", {
    minZoom: 5,
    maxZoom: 18,
    maxBounds: [[1.0, 99.0], [6.5, 104.5]],
    maxBoundsViscosity: 1.0
}).setView([3.07, 101.51], 9)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapSelangor);

fetch('/hospitals')
    .then(response => response.json())
    .then(function(hospitals) {
        hospitals.forEach(function(h) {
            L.marker([h.lat, h.lng])
            .addTo(mapKedah)
            .bindPopup('<b>' + h.name + '</b></br>' + h.type)
            L.marker([h.lat, h.lng])
            .addTo(mapSelangor)
            .bindPopup('<b>' + h.name + '</b></br>' + h.type);
        });
    });

var heatmapLayer1 = null;
var heatmapLayer2 = null;
var heatmapDisplay = false;

function toggleHeatmap() {
    if (heatmapDisplay) {
        if (heatmapLayer1) mapKedah.removeLayer(heatmapLayer1);
        heatmapDisplay = false;
        if (heatmapLayer2) mapSelangor.removeLayer(heatmapLayer2);
        heatmapDisplay = false;
        document.getElementById('heatmapBtn').textContent = 'Show Heatmap';
    } else {
        fetch('/heatmap')
            .then(response => response.json())
            .then(function(data){
                var kedahPoints = data.kedah.map(d => [parseFloat(d.lat), parseFloat(d.lon), parseFloat(d.intensity)]);
                var selangorPoints = data.selangor.map(d => [parseFloat(d.lat), parseFloat(d.lon), parseFloat(d.intensity)]);
                heatmapLayer1 = L.heatLayer(kedahPoints, { 
                    radius: 30, 
                    blur: 20,
                    max: 1.0,
                    minOpacity: 0.5,
                    gradient: {
                        0.2: 'blue',  
                        0.5: 'lime', 
                        0.8: 'yellow', 
                        1.0: 'red'
                    }
                }).addTo(mapKedah);
                heatmapLayer2 = L.heatLayer(selangorPoints, { 
                    radius: 30, 
                    blur: 20,
                    max: 1.0,
                    minOpacity: 0.5,
                    gradient: {
                        0.2: 'blue',  
                        0.5: 'lime', 
                        0.8: 'yellow', 
                        1.0: 'red'
                    }
                }).addTo(mapSelangor);
                heatmapDisplay = true;
                document.getElementById('heatmapBtn').textContent = 'Hide Heatmap';
            });
    }
}