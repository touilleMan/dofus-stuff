"use strict"


angular.module('app', [
    'misc.403Template'
    'misc.404Template'
    'misc.oupsTemplate'
    'ngRoute'
    'app.settings'
    'app.accueil'
])
  .config ($routeProvider) ->
    $routeProvider
      .when '/', { redirectTo: '/accueil' }
      .when '/403', { templateUrl: '403_template.html' }
      .when '/404', { templateUrl: '404_template.html' }
      .when '/oups', { templateUrl: 'oups_template.html' }
