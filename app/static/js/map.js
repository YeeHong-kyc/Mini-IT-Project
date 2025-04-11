// Initialize the map when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the map page
    if (document.getElementById('map')) {
        initMap();
    }
});

function initMap() {
    // Default to MMU center coordinates
    const defaultCenter = [3.063, 101.711];
    const defaultZoom = 17;
    
    // Initialize the map
    const map = L.map('map').setView(defaultCenter, defaultZoom);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add MMU campus boundary
    fetch('/api/mmubounds')
        .then(response => response.json())
        .then(bounds => {
            const rectangle = L.rectangle([
                [bounds.north, bounds.west],
                [bounds.south, bounds.east]
            ], {
                color: "#3498db",
                weight: 2,
                fillOpacity: 0.1
            }).addTo(map);
            
            // Add label for MMU campus
            L.marker([3.063, 101.711]).addTo(map)
                .bindPopup("<b>MMU Campus</b>")
                .openPopup();
            
            // Fit map to bounds if we have scan data
            if (window.scanData && window.scanData.length > 0) {
                const scanCoords = window.scanData.map(scan => [scan.lat, scan.lng]);
                const featureGroup = L.featureGroup([
                    rectangle,
                    ...scanCoords.map(coord => L.marker(coord))
                ]);
                map.fitBounds(featureGroup.getBounds());
            } else {
                map.fitBounds(rectangle.getBounds());
            }
        });
    
    // Add scan markers if available
    if (window.scanData) {
        window.scanData.forEach(scan => {
            const marker = L.marker([scan.lat, scan.lng]).addTo(map)
                .bindPopup(`<b>${scan.timestamp}</b><br>Scanned by: ${scan.scanner}`);
            
            // Add line connecting scans in chronological order
            if (window.scanData.length > 1) {
                const polyline = L.polyline(
                    window.scanData.map(s => [s.lat, s.lng]),
                    {color: '#e74c3c', weight: 2}
                ).addTo(map);
            }
        });
    }
    
    // Handle view on map clicks
    document.querySelectorAll('.view-on-map').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const lat = parseFloat(this.dataset.lat);
            const lng = parseFloat(this.dataset.lng);
            map.flyTo([lat, lng], 18);
            
            // Highlight the marker
            map.eachLayer(layer => {
                if (layer instanceof L.Marker && 
                    layer.getLatLng().lat === lat && 
                    layer.getLatLng().lng === lng) {
                    layer.openPopup();
                }
            });
        });
    });
}