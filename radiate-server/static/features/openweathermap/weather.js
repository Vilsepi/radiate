
angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', '$filter', function($scope, $http, $interval, $filter) {

    var apiUrl = "/api/openweathermap";
    
    $scope.getWeatherData = function(){
      $http.get(apiUrl).then(
        function successCallback(response) {

          $scope.weatherData = response.data;
          $scope.weatherSeries = _.map(response.data.forecast.list.slice(0,8), function (item) {
            return {'x': item.dt, 'y': item.main.temp};
          });

          // seriesTemperatureCurrent = [{'x': response.data.current.dt, 'y': response.data.current.main.temp}];
        },
        function errorCallback(response) {
          console.log("Failed to get data from backend");
        });

    };

    $scope.getWeatherData();
    $interval($scope.getWeatherData, 5000);

  }]);
