$.ajax({
    url: '/api/internal/mapmessages/',
    success: function(data){
        _.each(data, function(i){
            var m = new L.Marker(
                new L.LatLng(i.lat, i.lon),
                {title: i.title, icon: new L.Icon({iconUrl: '/static/img/nh_icon.png'}) }
            );
            m.addTo(map);
        });
    }
});
