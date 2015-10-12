
angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', '$filter', function($scope, $http, $interval, $filter) {
    var apiUrl = "/api/openweathermap";

    $scope.getWeatherData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.weatherData = data;

        var timestamps = _.map(data.forecast.list, function (item) {
          return $filter('date')(item.dt*1000, 'HH');
        });
        var temperatures = _.map(data.forecast.list, function (item) {
          return item.main.temp;
        });

        new Chartist.Line('.ct-chart', {
          labels: timestamps,
          series: [temperatures]
        }, {
          fullWidth: true,
          chartPadding: {
            right: 20
          }
        });

      });
    };

    $scope.getWeatherData();
    $interval($scope.getWeatherData, 60000);

  }]);
