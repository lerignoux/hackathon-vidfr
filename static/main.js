(function () {

  'use strict';

  angular.module('HackathonFFApp', ['ngMaterial'])
  .config(function ($mdThemingProvider, $mdIconProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('deep-orange')
      .accentPalette('cyan');
    $mdIconProvider
      .defaultIconSet('img/icons/sets/social-icons.svg', 24);
  })
  .controller('HackathonFFController', ['$scope', '$log', '$http', '$mdToast', '$location', '$window',
    function($scope, $log, $http, $mdToast, $location, $window) {
      $log.log("Controller initialiation");
      $scope.video = null;
      $scope.videoFilename = null;

      var params = $location.search();
      $log.log(params.name);

      if (params.name !== undefined) {
        $scope.file_query = btoa(params.name);
      }

      if (params.user == "admin") {
        $scope.certified = true;
      }

      if (params.refresh == "1") {
        $scope.autorefresh = true;
      }

      $http.get('/video', {params: {"ip": "unknown", "filequery": $scope.file_query}}).
        success(function(result) {
          $log.log("Video fetched: " + result.filename);
          $scope.video = result.filename;
          $scope.version = result.version
          $scope.videoFilename = encodeURI("static/videos/" + result.filename);
        }).
        error(function(error) {
          $log.log(error);
        });

        $scope.videoFeedback = function(feedback) {
          $http.post('/video/rate', {name: $scope.video, version: $scope.version, feedback: $scope.feedback, rating:feedback, certified:$scope.certified}).
            success(function(results) {
              $log.log("feedback Submited: "+ feedback);
              $scope.showSuccessToast()
              if ($scope.autorefresh == true) {
                $window.location.reload();
              }
            }).
            error(function(error) {
              $log.log(error);
            });
        };

        $scope.showSuccessToast = function() {
          $mdToast.show(
            $mdToast.simple()
              .textContent('Thank you for your feedback, you can refresh the page if you want to go on!')
              .position('bottom center')
              .hideDelay(10000)
              .theme("success-toast")
          );
        };

      }
  ]);

}());
