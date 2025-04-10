//P.S. this is for mobile tracking.


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;

                fetch(window.location.href, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({lat, lng})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        alert("Scan recorded successfully!");
                        window.location.href = `/item/${code}`;
                    } else {
                        alert("Scan could not be recorded. You must be on MMU campus!");
                    }
                });
            },
            error => {
                alert("Error getting location: " + error.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}


// Call this when QR Code is scanned
getLocation();