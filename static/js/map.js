// Map-specific JavaScript
function initMap(center, locations) {
    const map = L.map('map').setView([center.lat, center.lng], center.zoom);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add MMU marker
    const mmuIcon = L.icon({
        iconUrl: '{{ url_for("static", filename="Image/mmu-marker.png") }}',   //MMU logo
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
    
    L.marker([center.lat, center.lng], {icon: mmuIcon}).addTo(map)
        .bindPopup('<strong>MMU Campus</strong><br>Main Location')
        .openPopup();
    
    // Add scan locations
    const scanIcon = L.icon({
        iconUrl: '{{ url_for("static", filename="Image/scan-marker.png") }}',    //image of marker
        iconSize: [24, 24],
        iconAnchor: [12, 24],
        popupAnchor: [0, -24]
    });
    
    locations.forEach(loc => {
        L.marker([loc.lat, loc.lng], {icon: scanIcon}).addTo(map)
            .bindPopup(`
                <strong>Scan Location</strong><br>
                Time: ${loc.time}<br>
                IP: ${loc.ip}
            `);
    });
    
    // Add campus boundary if available
    if (center.bounds) {
        L.rectangle(center.bounds, {color: "#0062ff", weight: 2}).addTo(map);
    }
}