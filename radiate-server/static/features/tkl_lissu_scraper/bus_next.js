
angular.module('radiateApp')
  .controller('BusNextCtrl', ['$scope', '$http', function($scope, $http) {

    var apiUrl = "/api/tkl_lissu?stops=3733,3523,3737";
    var busData = [];

    // TODO: This should be done on the backend, i.e. provide list of next buses for given stops
    $http.get(apiUrl).success(function(data){
      data["stops"].forEach(function(stop) {
        stop["next_buses"].forEach(function(bus_line) {
          bus_line["eta"].forEach(function(bus) {
            bus["bus_stop_name"] = stop["bus_stop_name"]
            bus["updated_at"] = stop["updated_at"]
            bus["line"] = bus_line["line"]
            bus["destination"] = bus_line["destination"]
            busData.push(bus);
          });
        });
      });
      $scope.buses = busData;
    });

  }]);
