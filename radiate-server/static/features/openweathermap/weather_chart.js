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

      // Recreate chart when data changes
      scope.$watchCollection('[data, renderer]', function(newVal, oldVal){
        if(!newVal[0]){
          return;
        }

        element[0].innerHTML ='';

        var timeFixture = new Rickshaw.Fixtures.Time.Local();
        var graph = new Rickshaw.Graph({
          element: element[0],
          width: attrs.width,
          height: attrs.height,
          series: [{data: scope.data, color: attrs.color}],
          renderer: scope.renderer
        });

        /*
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
        */

        var xAxis = new Rickshaw.Graph.Axis.Time({
          graph: graph,
          timeUnit: timeFixture.unit('hour')
        });
        xAxis.render();

        var yAxis = new Rickshaw.Graph.Axis.Y({
          graph: graph,
          tickFormat: Rickshaw.Fixtures.Number.formatKMBT
        });
        yAxis.render();

        graph.render();
      });
    }
  };
});
