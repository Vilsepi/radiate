
angular.module('radiateApp')
  .controller('DemoCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.title = "Demo panel";
    $scope.date = new Date();

  }]);
