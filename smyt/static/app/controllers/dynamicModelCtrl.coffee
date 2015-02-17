controllers = angular.module('app.controllers')

controllers.controller('dynamicModelCtrl', ['$scope', '$resource', (s, r) ->
  s.table = {}
  TableMetaRes = r('/js_api/table/meta', {}, {
    post: {method: 'POST', isArray: true}
  })
  TableRes = r('/js_api/table/:name', {}, {
    query: {url: '/js_api/table/:name/list', isArray: true}
  })
  s.setTable = (table_name) ->
    TableMetaRes.post({name: table_name}, (headers) ->
      s.table.headers = headers
    )
    table_res = new TableRes({name: table_name})
    TableRes.query({name: table_name}, (rows) ->
      s.table.rows = rows
    )

])
