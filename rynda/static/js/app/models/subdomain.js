// Subdomain for one crysis

var subdomain = Backbone.Model.extend({
    initialize: function(attributes){

    },

    url: function(){
        return this.get("title");
    },

    getClass: function(){

    }
});
