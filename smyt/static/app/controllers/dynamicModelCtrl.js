// Generated by CoffeeScript 1.6.3
(function() {
  var controllers;

  controllers = angular.module('app.controllers');

  controllers.controller('dynamicModelCtrl', [
    '$scope', '$resource', function(s, r) {
      var TableMetaRes, TableRes;
      s.table = {};
      TableMetaRes = r('/js_api/table/meta', {}, {
        post: {
          method: 'POST',
          isArray: true
        }
      });
      TableRes = r('/js_api/table/:name', {}, {
        query: {
          url: '/js_api/table/:name/list',
          isArray: true
        }
      });
      return s.setTable = function(table_name) {
        var table_res;
        TableMetaRes.post({
          name: table_name
        }, function(headers) {
          return s.table.headers = headers;
        });
        table_res = new TableRes({
          name: table_name
        });
        return TableRes.query({
          name: table_name
        }, function(rows) {
          return s.table.rows = rows;
        });
      };
    }
  ]);

}).call(this);

/*
//@ sourceMappingURL=dynamicModelCtrl.map
*/