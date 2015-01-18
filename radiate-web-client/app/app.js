'use strict';

angular
  .module('radiateApp', [
  	'ui.router',
  ])
 .config(function ($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/');

    $stateProvider
      .state('main', {
        url: '/',
        views: {
          "right": {
              templateUrl: 'features/tkl_lissu_scraper/bus_next.html',
              controller: 'BusNextCtrl'
          },
          "left": {
              template: "<h1>Weather to be done</h1>"
          }
        }
      })
  });
