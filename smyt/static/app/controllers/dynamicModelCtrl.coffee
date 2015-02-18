controllers = angular.module('app.controllers')

controllers.controller('dynamicModelCtrl', ['$scope', '$rootScope', '$resource', (s, rs, r) ->
  s.errors = {}
  s.datepickerOptions =
    format: 'dd.mm.yyyy'
    autoclose: true

  s.table = {}
  s.instance = null
  TableMetaRes = r('/js_api/table/meta', {}, {
    post: {method: 'POST', isArray: true}
  })
  TableRes = r('/js_api/table/:table_name', {}, {
    query: {url: '/js_api/table/:table_name/list', isArray: true}
    update: {url: '/js_api/table/:table_name/:pk', method:'PUT'}
    remove: {url: '/js_api/table/:table_name/:pk', method:'DELETE'}
  })

  s.setTable = (table) ->
    s.errors = {}
    s.table = rs.table = table
    s.instance = new TableRes()

    TableMetaRes.post({name: table.name}, (headers) ->
      s.table.headers = headers
      s.table.fields = headers.map((header) -> header.name)
    ).$promise.then(() ->
      TableRes.query({table_name: table.name}, (rows) ->
        table_rows = []
        for row in rows
          fields = []
          instance = new TableRes()
          for field_name in s.table.fields
            type = null
            s.table.headers.filter((value) ->
              if value.name == field_name
                type = value.type
            )
            instance[field_name] = row[field_name]
            fields.push({name: field_name, value: row[field_name], type: type, instance: instance})
          table_rows.push(fields)
        s.table.rows = table_rows
      )
    )


  s.addRow = (form) ->
    s.errors = {}
    if form.$valid
      s.instance.$save({table_name: s.table.name}, (row) ->
        fields = []
        instance = angular.copy(s.instance)
        s.instance = new TableRes()
        for field_name in s.table.fields
            type = null
            s.table.headers.filter((value) ->
              if value.name == field_name
                type = value.type
            )
            fields.push({name: field_name, value: row[field_name], type: type, instance: instance})
        s.table.rows.unshift(fields)
      , (resp) ->
        angular.extend(s.errors, resp.data)
      )
    else
      console.log form, s.errors
      for key, value of form
        if key and angular.isObject(value)
          if key.indexOf('$') != 0
            if value.$dirty and value.$invalid
              s.errors[value.$name] = []
  return
])

controllers.controller('rowCtrl', ['$scope', '$rootScope', '$resource', (s, rs, r) ->
  s.errors = {}
  s.edit = false

  s.update = (form, instance) ->
    if form.$valid
      instance.$update({table_name: rs.table.name, pk: instance.id}, () ->
        s.errors = {}
        s.edit = false
      , (resp) ->
        angular.extend(s.errors, resp.data)
      )
    else
      for key, value of s.form
        if key and angular.isObject(value)
          if key.indexOf('$') != 0
            if value.$dirty and value.$invalid
              s.errors[value.$name] = [true]
  return
])