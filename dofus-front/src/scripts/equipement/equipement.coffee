"use strict"


angular.module('app.equipement', ['misc.list_equipementsTemplate',
                                  'ngRoute', 'xin.backend'])
  .config ($routeProvider) ->
    $routeProvider
      .when '/equipements', {
        restrict: 'EA'
        templateUrl: 'scripts/equipement/list_equipements_template.html'
        controller: 'ListEquipementsController'
      }
      .when '/equipements/:equipementId', {
        restrict: 'EA'
        templateUrl: 'scripts/equipement/show_equipement_template.html'
        controller: 'ShowEquipementController'
      }



  .controller 'ListEquipementsController', ($scope, Backend) ->
    $scope.equipements = []

    Backend("equipements").get(
      (response) ->
        $scope.equipements = response.items
      (response) -> console.log("error", response)
    )

    $scope.onClick = () ->
      console.log(this.equipement._id)
      # $window.location = "#/equipements/#{this.equipement._id}"



  .controller 'ShowEquipementController', ($scope, $routeParams, Backend) ->
    $scope.equipement = {}

    Backend("equipements", $routeParams.equipementId).get(
      (response) ->
        console.log(response)
        # $scope.equipement = response.items
      (response) -> console.log("error", response)
    )
