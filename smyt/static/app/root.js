// Generated by CoffeeScript 1.6.3
(function() {
  var app;

  app = angular.module('smyt', ['ngResource', 'ngCookies', 'app.factories', 'app.constants', 'app.controllers', 'app.directives']);

  app.config([
    '$httpProvider', '$interpolateProvider', '$locationProvider', function($httpProvider, $interpolateProvider, $locationProvider) {
      $locationProvider.html5Mode(true);
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $interpolateProvider.startSymbol('{$');
      return $interpolateProvider.endSymbol('$}');
    }
  ]);

  app.run([
    '$rootScope', function($rootScope) {
      return $rootScope.JSON = JSON;
    }
  ]);

  angular.module('app.controllers', []);

  angular.module('app.directives', []);

  angular.module('app.factories', []);

  angular.module('app.constants', []);

}).call(this);

/*
//@ sourceMappingURL=root.map
*/
