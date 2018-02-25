
angular.module('radiateApp')
  .controller('BusStopCtrl', ['$scope', '$http', '$interval', function($scope, $http, $interval) {

    var apiUrl = "/api/tkl_lissu?stops=3733,3523,3737";
    //var apiUrl = "/static/test/bus.json";

    // List of bus lines to filter out for each bus stop
    var busLineBlacklist = {
      '3733': ['38', '65'], // Poliisikoulu
      '3523': ['5'], // Hervantakeskus pohjoiseen
      '3737': ['13', '38'] // Tuulanhovi
    };

    $scope.getBusStopData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.busStopData = _.map(data["stops"], function(stop){
          stop.next_buses = _.filter(stop.next_buses, function(line){
            return !_.contains(busLineBlacklist[stop.bus_stop_id], line.line);
          });
          return stop;
        });

      });
    };

    $scope.getBusStopData();
    $interval($scope.getBusStopData, 5000);

  }]);
