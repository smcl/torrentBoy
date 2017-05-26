'use strict';   // See note about 'use strict'; below


var torrentBoy = angular.module('torrentBoy', [
 //'ngRoute',
]).controller('torrentBoyController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {

    $scope.search = function() {
        $log.log("test");

        // get the URL from the input
        var userInput = $scope.searchTerm;

        // fire the API request
        $http.post('/search', {"search_term": userInput}).
            success(function(data) {
                $log.log(data.results);
                $scope.results = data.results;
            }).
            error(function(error) {
                $log.log(error);
              });
    };

    $scope.queue_download = function(urn, url) {
        $log.log("requesting magnet " + urn);
        $http.post('/download', {"urn": urn, "url": url}).
            success(function(data) {
                $log.log("requested successfully");
            });
    };
  }
]).config(function ( $compileProvider) {
      $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|magnet):/);
  });

