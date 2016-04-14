"use strict"


angular.module('app.settings', [])
  .constant 'SETTINGS', {
    DEFAULT_COUNTRY: 'FRA'
    API_DOMAIN: 'http://localhost:5000'
    FRONT_DOMAIN: 'http://localhost:9000'
    BASE_TITLE: 'Dofus'
  }
