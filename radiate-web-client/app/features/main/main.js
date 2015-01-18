
angular.module('radiateApp')
  .controller('MainCtrl', ['$scope', function($scope) {

  	$scope.panels = [
  	{contentView: "features/tkl_lissu_scraper/bus_next.html"},
  	{contentView: "features/tkl_lissu_scraper/bus_stop.html"}];

  }]);
