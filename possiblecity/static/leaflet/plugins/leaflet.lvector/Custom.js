lvector.Custom = lvector.GeoJSONLayer.extend({
    initialize: function(options) {
        
        // Check for required parameters
        for (var i = 0, len = this._requiredParams.length; i < len; i++) {
            if (!options[this._requiredParams[i]]) {
                throw new Error("No \"" + this._requiredParams[i] + "\" parameter found.");
            }
        }
        
        // Extend Layer to create Custom
        lvector.Layer.prototype.initialize.call(this, options);
        
        // _globalPointer is a string that points to a global function variable
        // Features returned from a JSONP request are passed to this function
        this._globalPointer = "Custom_" + Math.floor(Math.random() * 100000);
        window[this._globalPointer] = this;
        
        // Create an array to hold the features
        this._vectors = [];
        
        
        if (this.options.map) {
            if (this.options.scaleRange && this.options.scaleRange instanceof Array && this.options.scaleRange.length === 2) {
                var z = this.options.map.getZoom();
                var sr = this.options.scaleRange;
                this.options.visibleAtScale = (z >= sr[0] && z <= sr[1]);
            }
            this._show();
        }
    },
    
    options: {
        url: null
    },

    _requiredParams: ["url"],

    
    _getFeatures: function() {
        
        // fire dataloading event
        this.options.map.fire("dataloading");
        
        // Build URL
        var url = this.options.url
        url += "?format=jsonp" + // JSON please
               "&callback=" + this._globalPointer + "._processFeatures"; // Need this for JSONP
        if (!this.options.showAll) {
            url += "&bbox=" + this.options.map.getBounds().toBBoxString(); // Build bbox geometry
        }
        // JSONP request
        this._makeJsonpRequest(url);
        
    }   
}); 
