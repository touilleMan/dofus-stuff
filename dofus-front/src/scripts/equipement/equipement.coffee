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


  .controller 'ListEquipementsController', ($scope, Backend) ->
    $scope.equipements = []

    Backend("equipements").get(
      (response) ->
        $scope.equipements = response.items
      (response) -> console.log("error", response)
    )
