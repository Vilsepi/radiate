
angular.module('radiateApp')
  .controller('BusStopCtrl', ['$scope', '$http', '$interval', function($scope, $http, $interval) {

    var apiUrl = "/api/tkl_lissu?stops=3733,3523,3737";
    //var apiUrl = "/static/test/bus.json";

    var busLineBlacklist = ["38", "65"];

    $scope.getBusStopData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.busStopData = _.map(data["stops"], function(stop){
          stop.next_buses = _.filter(stop.next_buses, function(line){
            return !_.contains(busLineBlacklist, line.line);
          });
          return stop;
        });

      });
    };

    $scope.getBusStopData();
    $interval($scope.getBusStopData, 5000);

  }]);
