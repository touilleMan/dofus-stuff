"use strict"

angular.module('xin.backend', ['ngResource'])
  .factory 'Backend', ($resource, SETTINGS) ->
    (url, paramDefaults = null, actions = null) ->
      url = "#{SETTINGS.API_DOMAIN}/#{url}"
      $resource(url, paramDefaults, actions)
