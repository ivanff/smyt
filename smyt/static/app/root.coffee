app = angular.module('smyt', [
  'ngResource'
  'ngCookies'

  'app.factories'
  'app.constants'
  'app.controllers'
  'app.directives'
])


app.config(['$httpProvider', '$interpolateProvider', '$locationProvider', ($httpProvider, $interpolateProvider, $locationProvider) ->
#  $resourceProvider.defaults.stripTrailingSlashes = false
  $locationProvider.html5Mode(true)
  #  $httpProvider.defaults.useXDomain = true
  #  delete $httpProvider.defaults.headers.common['X-Requested-With']
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
  $interpolateProvider.startSymbol('{$')
  $interpolateProvider.endSymbol('$}')
])

app.run(['$rootScope', ($rootScope) ->
  $rootScope.JSON = JSON
])

angular.module('app.controllers', [])
angular.module('app.directives', [])
angular.module('app.factories', [])
angular.module('app.constants', [])