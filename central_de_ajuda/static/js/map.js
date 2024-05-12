var map = L.map('map' ,{
    center: [-30.0331, -51.2300],
    zoom: 09
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

var marker = L.marker([-30.0331, -51.2300]).addTo(map);
marker.bindPopup('Porto Alegre, capital do Rio Grande do Sul');

// Localização não funciona em http
// map.locate({ setView: true, maxZoom: 19 });