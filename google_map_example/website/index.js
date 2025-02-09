let map;
let infoWindow;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"),
        centerMapOnLocation(),
    );
    infoWindow = new google.maps.InfoWindow();

    // Function to center the map on the user's current location
    function centerMapOnLocation() {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    sendCoordinatesToServer(pos);
                    new google.maps.Marker({
                        position: pos,
                        map : map,
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: 10,
                            fillOpacity: 1,
                            strokeWeight: 2,
                            fillColor: '#5384ED',
                            strokeColor: '#ffffff',
                          },
                    });
                    map.setCenter(pos);
                    map.setZoom(14); // Set the zoom level to 14 (you can adjust this value as needed)
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    }
}
//{ lat: 53.30323370042453, lng: -6.256870048826886}
// Example function to send coordinates to the server
function sendCoordinatesToServer(coordinates) {
    fetch('http://127.0.0.1:8080/coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "coordinates": coordinates })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.nearby_houses); // Log response from server
        updateMapWithNearbyHouses(data.nearby_houses);
    })
    .catch(error => console.error('Error javaS:', error));
}

function updateMapWithNearbyHouses(nearbyHouses) {
    var props = document.getElementById("places");
    nearbyHouses.forEach(listing => {
        const latLng = { lat: listing.latitude, lng: listing.longitude };
        
        const marker = new google.maps.Marker({
            position: latLng,
            map: map, 
            title: listing.title,  
        });

        props.insertAdjacentHTML( 'beforeend',"<li>" + listing.title + " </li>");

        const infoWindow = new google.maps.InfoWindow({
            content: '<div><strong>' + listing.title + '</strong></div>' + '<a href="' + listing.link + '">More info</a>'
        })
        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
    });
}



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation.",
    );
    infoWindow.open(map);
}

var open = false;
// Function to open the sidebar
function openNav() {
    if (document.getElementById("sidebar").style.width = "0" && open == false){
        document.getElementById("sidebar").style.width = "250px";
        open = true;
    }
    else if (open==true){
        document.getElementById("sidebar").style.width = "0";
        open = false;
    }    
}

// Function to close the sidebar
function closeNav() {
    document.getElementById("sidebar").style.width = "0";
}

window.initMap = initMap;
