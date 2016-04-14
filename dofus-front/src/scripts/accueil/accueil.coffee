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
    test = Backend("test").get(
      (response) -> console.log("success", response)
      (response) -> console.log("error", response)
    )
