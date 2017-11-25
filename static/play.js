(function () {

  'use strict';

  angular.module('HackathonFFPlayApp', ['ngMaterial'])
  .config(function ($mdThemingProvider, $mdIconProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('deep-orange')
      .accentPalette('cyan');
    $mdIconProvider
      .defaultIconSet('img/icons/sets/social-icons.svg', 24);
  })
  .controller('HackathonFFPlayController', ['$scope', '$log', '$http', '$mdToast', '$location', '$window',
    function($scope, $log, $http, $mdToast, $location, $window) {
      $log.log("Controller initialiation");
      $scope.status = 'menu'; // menu, question, answer
      $scope.answers = [];
      $scope.scene = {good: {}, bad: {}};

      $scope.log = function(username, password) {
        $http.post('/login', {username: username, password: password}).
        success(function(result) {
          $log.log("User logged: " + result);
          $scope.username = username;
          $scope.user_id = result.user_id;
          $scope.history = result.history;
        }).
        error(function(error) {
          $log.log(error);
          $scope.showErrorToast("Could not login, ensure user exists and password is correct");
        });
      };

      $scope.new = function(username, password) {
        $http.post('/user', {username: username, password: password}).
        success(function(result) {
          $log.log("User created: " + result);
          $scope.username = username;
          $scope.user_id = result.user_id;
        }).
        error(function(error) {
          $log.log(error);
          $scope.showErrorToast("Could not create user, username already used.");
        });
      };

      $scope.play = function() {
        $http.post('/game', {user_id: $scope.user_id}).
        success(function(result) {
          $log.log("Game created: ");
          $scope.game_id = result.game_id;
          $scope.title = result.title;
          $scope.battle_tag = result.battle_tag;
          $scope.getScene();
        }).
        error(function(error) {
          $log.log(error);
        });
      };

      $scope.join = function(tag) {
        $http.post('/game', {user_id: $scope.user_id, battle_tag: tag}).
        success(function(result) {
          $log.log("Game joined: ");
          $scope.game_id = result.game_id;
          $scope.title = result.title;
          $scope.battle_tag = tag;
          $scope.getScene();
        }).
        error(function(error) {
          $log.log(error);
        });
      };

      $scope.getScene = function(choice) {
        $http.get('/scene?user_id='+$scope.user_id+'&game_id='+$scope.game_id, {}).
        success(function(result) {
          $log.log("Scene fetched: " + result);
          $scope.status = 'question';
          $scope.scene = result;
          console.log($scope.status);
        }).
        error(function(error) {
          $log.log(error);
        });
      };


      $scope.userChoice = function(choice) {
        let result;
        if (choice == 'good'){
          $scope.showSuccessToast();
          result = 1;
        }
        else {
          $scope.showFailureToast();
          result = 0;
        }
        $scope.status = "answer";
        $scope.answers.push(choice);
        $http.post('/scene', {user_id: $scope.user_id, game_id: $scope.game_id, choice: result}).
        success(function(results) {
          $log.log("Choice submited");
        }).
        error(function(error) {
          $log.log(error);
        });
      };

      $scope.getVideo = function(scene) {
        return "static/videos/" + scene.content;
      };

      $scope.getGoodVideo = function(scene) {
        return "static/videos/" + scene.good.content;
      };

      $scope.getBadVideo = function(scene) {
        return "static/videos/" + scene.bad.content;
      };

      $scope.next = function() {
        $scope.getScene()
      };

      $scope.exit = function() {
        $scope.status = 'menu';
        $scope.game_id = undefined;
        $scope.scene = {};
        $scope.answers = [];
      };

      $scope.showSuccessToast = function() {
        $mdToast.show(
          $mdToast.simple()
            .textContent('Congratulations! Here are some funny situations you probably have missed')
            .position('bottom center')
            .hideDelay(3000)
            .theme("success-toast")
        );
      };

      $scope.showFailureToast = function() {
        $mdToast.show(
          $mdToast.simple()
            .textContent('You got it wrong, check why !')
            .position('bottom center')
            .hideDelay(5000)
            .theme("failure-toast")
        );
      };

      $scope.showErrorToast = function(error) {
        $mdToast.show(
          $mdToast.simple()
            .textContent(error)
            .position('bottom center')
            .hideDelay(8000)
            .theme("failure-toast")
        );
      };
      }
  ]);

}());
