
angular.module('radiateApp')
  .controller('OpenWeatherCtrl', ['$scope', '$http', '$interval', '$filter', function($scope, $http, $interval, $filter) {

    var apiUrl = "/api/openweathermap";
    
    var timeFixture = new Rickshaw.Fixtures.Time.Local();
    var seriesTemperatureForecast = [];
    var seriesTemperatureCurrent = [];
    var graph = null;

    $scope.getWeatherData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.weatherData = data;

        seriesTemperatureForecast = _.map(data.forecast.list, function (item) {
          return {'x': item.dt, 'y': item.main.temp};
        });

        // Only view one day TODO API should provide this
        seriesTemperatureForecast = seriesTemperatureForecast.slice(0,8);

        seriesTemperatureCurrent = [{'x': data.current.dt, 'y': data.current.main.temp}];
        
        // TODO Move graph stuff out of http success and call graph update instead
        graph = new Rickshaw.Graph( {
          element: document.getElementById("chart"),
          width: 900,
          height: 500,
          renderer: 'multi',
          dotSize: 8,
          stroke: true,
          preserve: true,
          series: [
            {
              data: seriesTemperatureForecast,
              color: '#ccc',
              renderer: 'line'
            },
            {
              data: seriesTemperatureCurrent,
              color: '#f00',
              renderer: 'scatterplot'
            },
          ]
        });
        //graph.render();

        var xAxis = new Rickshaw.Graph.Axis.Time({
            graph: graph,
            timeUnit: timeFixture.unit('3hour')
        });
        xAxis.render();

        var yAxis = new Rickshaw.Graph.Axis.Y( {
          graph: graph,
          tickFormat: Rickshaw.Fixtures.Number.formatKMBT
        } );
        yAxis.render();

        graph.update();

      });
    };

    $scope.getWeatherData();
    $interval($scope.getWeatherData, 5000);

  }]);
