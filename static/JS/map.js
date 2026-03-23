const map = L.map("map", {
    minZoom: 5,
    maxZoom: 18,
    maxBounds: [[1.0, 99.0], [6.5, 104.5]],
    maxBoundsViscosity: 1.0
}).setView([4.5, 101.2], 7)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

fetch('/hospitals')
    .then(response => response.json())
    .then(function(hospitals) {
        hospitals.forEach(function(h) {
            L.marker([h.lat, h.lng])
            .addTo(map)
            .bindPopup('<b>' + h.name + '</b></br>' + h.type);
        });
    });