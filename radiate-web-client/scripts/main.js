'use strict';

angular
  .module('radiateApp', [
  ]);

angular.module('radiateApp')
  .controller('BusController', ['$scope', '$http', function($scope, $http) {

    $scope.apiUrl = "http://localhost:5000/api/tkl_lissu?stops=3733,3523,3737";
    $scope.busStopData = null;

    $http.get($scope.apiUrl).success(function(data){
      $scope.busStopData = data["stops"];
      console.log($scope.busStopData);
    });

  }]);
