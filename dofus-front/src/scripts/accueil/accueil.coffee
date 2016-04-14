"use strict"


angular.module('app.accueil', ['misc.accueilTemplate', 'ngRoute', 'xin.backend'])
  .config ($routeProvider) ->
    $routeProvider
      .when '/accueil', {
        restrict: 'EA'
        templateUrl: 'scripts/accueil/accueil_template.html'
        controller: 'AccueilController'
      }


  .controller 'AccueilController', ($scope, Backend) ->
    $scope.base =
      vitalite: 0
      sagesse: 0
      force: 0
      intelligence: 0
      agilite: 0
      chance: 0
    $scope.parcho =
      vitalite: 0
      sagesse: 0
      force: 0
      intelligence: 0
      agilite: 0
      chance: 0
    $scope.objectif =
      vitalite: 0
      sagesse: 0
      force: 0
      intelligence: 0
      agilite: 0
      chance: 0

    $scope.compute = ->
      console.log("TODO")
