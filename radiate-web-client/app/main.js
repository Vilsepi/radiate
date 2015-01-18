
angular.module('radiateApp')
  .controller('MainCtrl', ['$scope', function($scope) {

    $scope.panels = [
    {contentView: "features/demo/demo.html"},
    {contentView: "features/tkl_lissu_scraper/bus_next.html"}
    ];

  }]);
