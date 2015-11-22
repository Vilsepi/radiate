angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', '$filter', function($scope, $http, $interval, $filter) {

    var apiUrl = "/api/openweathermap";
    //var apiUrl = "/static/test/weather-combined-2015-11-22.json";
    
    $scope.getWeatherData = function(){
      $http.get(apiUrl).then(
        function successCallback(response) {
          $scope.weatherData = response.data;
        },
        function errorCallback(response) {
          console.log("Failed to get data from backend");
        });
    };

    $scope.getWeatherData();
    $interval($scope.getWeatherData, 30000);

  }]);
