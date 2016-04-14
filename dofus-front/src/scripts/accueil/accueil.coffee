"use strict"


angular.module('app.accueil', ['misc.accueilTemplate', 'ngRoute'])
  .config ($routeProvider) ->
    $routeProvider
      .when '/accueil', {
        restrict: 'EA'
        templateUrl: 'scripts/accueil/accueil_template.html'
        controller: 'AccueilController'
      }


  .controller 'AccueilController', ($scope) ->
