"use strict"


angular.module('app.settings', [])
  .constant 'SETTINGS', {
    DEFAULT_COUNTRY: 'FRA'
    API_DOMAIN_LOCALHOST: 'http://localhost:5000'
    API_DOMAIN_LOCALNETWORK: 'http://centakina:5000'
    API_DOMAIN_INTERNET: 'http://centakina.no-ip.biz:5000'
    FRONT_DOMAIN: 'http://localhost:9000'
    BASE_TITLE: 'Dofus'
  }
