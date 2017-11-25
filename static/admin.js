(function () {

  'use strict';

  angular.module('HackathonFFAdminApp', ['ngMaterial'])
  .config(function ($mdThemingProvider, $mdIconProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('deep-orange')
      .accentPalette('cyan');
    $mdIconProvider
      .defaultIconSet('img/icons/sets/social-icons.svg', 24);
  })
  .controller('AdminController', ['$scope', '$log', '$http', '$filter', '$location',
    function($scope, $log, $http, $filter, $location) {



      $log.log("Controller initialiation");
      $scope.content = [];

      $scope.newContent = {'scenes': [{}, {}, {}]};

      $scope.password = ''

      $scope.getContent = function() {
        $log.log("Fetching content");
        $http.get('/content', {}).
        success(function(results) {
          $log.log("Content fetched ");
          $log.log(results);
          $scope.content = results;
        }).
        error(function(error) {
          $log.log(error);
        });
      }

      $scope.getContent();

      $scope.postContent = function(content) {

        $http.post('/content', {'password': $scope.password, 'content': content}).
          success(function(results) {
            $scope.getContent();
            $scope.newContent = {'scenes': [{}, {}, {}]};
          }).
          error(function(error) {
            $log.log(error);
          });
        }


    }
  ]);

}());
