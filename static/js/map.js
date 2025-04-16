// Map-specific JavaScript
function initMap(mapData) {
    const map = L.map('map', {
        maxBounds: mapData.bounds,
        maxBoundsViscosity: 1.0  // Makes it harder to drag outside bounds
    }).setView([mapData.center.lat, mapData.center.lng], mapData.center.zoom);
    
    // Restrict view to campus area
    map.setMaxBounds(mapData.bounds);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add campus boundary rectangle 
    L.rectangle(mapData.bounds, {
        color: "orange",
        weight: 1,
        fillOpacity: 0.1
    }).addTo(map).bindPopup("MMU Cyberjaya Campus Boundary");
    
    // Add MMU campus polygon (blue outline)
    const mmuPolygon = L.polygon([
        [2.933639, 101.637861],  // NW corner
        [2.933639, 101.646833],  // NE corner
        [2.9220, 101.646833],  // SE corner
        [2.9220, 101.637861]   // SW corner
    ], {
        color: "blue",
        weight: 2,
        fillOpacity: 0.05
    }).addTo(map).bindPopup('MMU Cyberjaya Campus');

    // Add scan locations
    mapData.locations.forEach(loc => {
        L.marker([loc.lat, loc.lng]).addTo(map)
            .bindPopup(`Scanned: ${loc.time}<br>IP: ${loc.ip}`);
    });
}