var VueSidebar = {
  el: "#vue-sidebar",

  data: {
  },

  methods: {

    applyFlowFilters: function() {
      ShowNodeFlows(CurrentNodeDetails);
    },
  
    flowFiltersKeys: function() {
      var query = "G.V('"+CurrentNodeDetails.ID+"').Flows().Keys()";
      return $.ajax({
        dataType: "json",
        url: '/api/topology',
        data: JSON.stringify({"GremlinQuery": query}),
        method: 'POST',
        error: function(e) {
          $.notify({
            message: 'Gremlin request error: ' + e.responseText
          },{
            type: 'danger'
          });
        }
      });
    },

    flowFiltersValues: function(key) {
      var query = "G.V('"+CurrentNodeDetails.ID+"').Flows().Values('"+key+"').Dedup()";
      return $.ajax({
        dataType: "json",
        url: '/api/topology',
        data: JSON.stringify({"GremlinQuery": query}),
        method: 'POST',
        error: function(e) {
          $.notify({
            message: 'Gremlin request error: ' + e.responseText
          },{
            type: 'danger'
          });
        }
      }).then(function(data) {
        return data.map(function(v) {
          return v.toString();
        });
      });
    },

  }

};
