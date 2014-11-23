
angular.module('radiateApp')
  .controller('BusNextCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.apiUrl = "http://localhost:5000/api/tkl_lissu?stops=3733,3523,3737";
    $scope.busData = new Array();

    $http.get($scope.apiUrl).success(function(data){
      console.log(data)

      data["stops"].forEach(function(stop) {
        stop["next_buses"].forEach(function(bus) {
          bus["bus_stop_name"] = stop["bus_stop_name"]
          bus["updated_at"] = stop["updated_at"]
          $scope.busData.push(bus);
        });
      });
      console.log($scope.busData);
    });

  }]);
