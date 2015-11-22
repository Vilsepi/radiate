// Based on http://tagtree.tv/d3-with-rickshaw-and-angular
// TODO Does this constantly create a new Graph?
// Is this better? https://github.com/flo-c/Blog/blob/master/angularrickshaw/src/angularrickshaw/angularrickshaw.js

angular.module('radiateApp')
.directive('rickshawChart', function () {
  return {
    scope: {
      data: '=',
      renderer: '='
    },
    template: '<div></div>',
    restrict: 'E',
    link: function postLink(scope, element, attrs) {

      // Helper to nicely fit the data series into the drawn range
      function calculateRange(upperOrLower, series) {
        if (upperOrLower === 'upper') {
          highestPoint = _.max(_.pluck(series, 'y'))
          return Math.ceil(highestPoint/5)*5;
        }
        else if (upperOrLower === 'lower') {
          lowestPoint = _.min(_.pluck(series, 'y'))
          return Math.floor(lowestPoint/5)*5;
        }
        else {
          return 0;
        }
      }

      // Recreate chart when data changes
      scope.$watchCollection('[data, renderer]', function(newVal, oldVal){
        if(!newVal[0]){
          return;
        }

        var weatherSeries = _.map(scope.data.forecast.list, function (item) {
          return {'x': item.dt, 'y': item.main.temp};
        });

        var currentSeries = [{'x': scope.data.current.dt, 'y': scope.data.current.main.temp}];

        element[0].innerHTML ='';

        var timeFixture = new Rickshaw.Fixtures.Time.Local();
        var graph = new Rickshaw.Graph({
          element: element[0],
          width: attrs.width,
          height: attrs.height,
          dotSize: 8,
          strokeWidth: 4,
          stroke: true,
          preserve: true,
          renderer: 'multi',
          max: calculateRange('upper', weatherSeries),
          min: calculateRange('lower', weatherSeries),
          series: [
            {
              data: weatherSeries,
              color: '#ccb',
              renderer: 'line'
            }
          ]
        });

        var customTimeFormatter = {
          seconds: 3600 * 6,
          formatter: function(d) {
            return d.toString().match(/(\d+):\d+:/)[1];
          }
        }

        var xAxis = new Rickshaw.Graph.Axis.Time({
          graph: graph,
          timeUnit: customTimeFormatter,
          timeFixture: timeFixture
        });
        xAxis.render();

        var yAxis = new Rickshaw.Graph.Axis.Y({
          graph: graph,
          tickFormat: function (d) { return d; }
        });
        yAxis.render();

        graph.render();
      });
    }
  };
});
