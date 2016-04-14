"use strict"

angular.module('xin.backend', ['ngResource'])
  .factory 'Backend', ($resource, $location, SETTINGS) ->
    (url, paramDefaults = null, actions = null) ->
      if not url?
        url = ""
      if $location.$$host == "localhost"
        url = "#{SETTINGS.API_DOMAIN_LOCALHOST}/#{url}"
      else if $location.$$host == "centakina"
        url = "#{SETTINGS.API_DOMAIN_LOCALNETWORK}/#{url}"
      else
        url = "#{SETTINGS.API_DOMAIN_INTERNET}/#{url}"
      $resource(url, paramDefaults, actions)
