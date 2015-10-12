
angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
    var apiUrl = "/api/openweathermap";

    $scope.getWeatherData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.weatherData = data;
      });
    };

    $scope.getWeatherData();
    $interval($scope.getWeatherData, 60000);

  }]);
