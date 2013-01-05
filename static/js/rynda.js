var Rynda = (function(){
    var version = "1.0";

    function sameheight(group){
        var tallest = 0;
        group.each(function(){
            var h = $(this).height();
            if (tallest < h){
                tallest = h;
            }
        });
        group.height(tallest);
    }

    return {
        version: version,
        sameheight: sameheight
    }
})();


Rynda.map = (function(){

    var map;
    

    function createMap(domElement){
       var cloudmade = new L.TileLayer(
            'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            { maxZoom: 18,
              minZoom: 3,
              attribution: 'карта &copy; OpenStreetMap, рендер &copy; CloudMade'
            }
        );

        this.map = new L.map(domElement,
            { center: new L.LatLng(64,95),
              zoom: 4,
              layers:[cloudmade]
            }
        );

    }

    function fetch(){
        var that = this;
        var icons = {
            '1' : '/static/img/nh_icon.png',
            '2' : '/static/img/wh_icon.png',
            '3' : '/static/img/nh_icon.png'
        };
        $.ajax({
            url: '/api/internal/mapmessages/',
            success: function(data){
                _.each(data, function(i){
                var m = new L.Marker(
                    new L.LatLng(i.lat, i.lon),
                    {title: i.title, icon: new L.Icon({iconUrl: icons[i.messageType]}) }
                );
                m.addTo(that.map);
                });
            }
        });
    }

    function toggleMap(){
        $(this.map.getContainer()).toggle();
    }

    return  {
        fetch: fetch,
        createMap: createMap,
        toggleMap: toggleMap
    }
})();


