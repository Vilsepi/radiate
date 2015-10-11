
angular.module('radiateApp')
  .controller('BusStopCtrl', ['$scope', '$http', '$interval', function($scope, $http, $interval) {
    var apiUrl = "/api/tkl_lissu?stops=3733,3523,3737";

    $scope.getBusStopData = function(){
      $http.get(apiUrl).success(function(data){
        $scope.busStopData = data["stops"];
      });
    };

    $scope.getBusStopData();
    $interval($scope.getBusStopData, 10000);

  }]);
