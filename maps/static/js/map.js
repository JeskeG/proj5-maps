$.getJSON("/setup",
    function(data){
    var lat = data.results.lat;
    console.log(lat);
    var lng = data.results.lng;
    console.log(lng);
    var mymap = L.map('mapid').setView([lat, lng], 13);


    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiamdsZW5uIiwiYSI6ImNqOTYzcmlxNTAwZGEyd29sY2hobWF1a2cifQ.YZHt-1RCTxtz1zpK1MVHEg'
    })
    .addTo(mymap);


    var popup = L.popup();

    function onMapClick(e) {
    $.getJSON("/clicked", {lat: e.latlng.lat, lng: e.latlng.lng},
    function(data) {
    var address = data.results;
        popup
            .setLatLng(e.latlng)
            .setContent(address.address)
            .openOn(mymap);}
    )}
    $.getJSON("/places",
    function(data){
    console.log(data);
    data.results.forEach(function(x){
    console.log(x.name);
    var marker = L.marker([x.geometry.location.lat, x.geometry.location.lng])
    .bindPopup(x.name + '<br>' + x.vicinity)
    .addTo(mymap);
    })
    })
mymap.on('click', onMapClick);
})
