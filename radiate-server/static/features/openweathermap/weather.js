angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', '$filter', function($scope, $http, $interval, $filter) {

    var apiUrl = "/api/openweathermap";
    //var apiUrl = "/static/test/weather.json";
    
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
    $interval($scope.getWeatherData, 60000);

  }]);
