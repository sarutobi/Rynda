(function(){

    var Rynda ={
        widgets:{}
    };

    Rynda.BaseWidget = {
        instantiate: function(widget){
            var w = new Rynda.BaseWidget(widget);
            _.extend(w, Backbone.Event);
            Rynda.widgets[widget] = w;
            return w;
        }
    }
    window.Rynda = Rynda;
})();

var cloudmade = new L.TileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    { maxZoom: 18,
      minZoom: 3,
      attribution: 'карта &copy; OpenStreetMap, рендер &copy; CloudMade'
    }
);
var map = new L.map('locationMapCanvas',
    { center: new L.LatLng(64,95),
      zoom: 4,
      layers:[cloudmade]
    }
);
