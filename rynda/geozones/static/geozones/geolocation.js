$(document).ready(function(){
if (jQuery != undefined){
    var django = {
        'jQuery': jQuery
    }
}

(function($){
    var $latitudeField = $('#id_location_0'),
        $longitudeField = $('#id_location_1'),
        $mapContainer = $('div.geolocation-map'),
        latitude = $latitudeField.val() || 0,
        longitude = $longitudeField.val() || 0,
        mapCenter = new L.LatLng(latitude, longitude),
        cloudmade = new L.TileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            { maxZoom: 18,
              minZoom: 3,
              attribution: 'карта &copy; OpenStreetMap, рендер &copy; CloudMade'
            }
        ),
        map = new L.Map($mapContainer.get(0),{
            center: mapCenter,
            zoom: 4,
            layers:[cloudmade]
        }),
        marker = new L.Marker(mapCenter);

        marker.addTo(map);

        new L.Control.GeoSearch({
            provider: new L.GeoSearch.Provider.Google()
        }).addTo(map);
})(django.jQuery);
});
