'use strict';

angular
  .module('radiateApp', [
  	'ngRoute',
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/bus_stop', {
        templateUrl: 'views/bus_stop.html',
        controller: 'BusStopCtrl'
      })
      .when('/bus', {
        templateUrl: 'views/bus_next.html',
        controller: 'BusNextCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
