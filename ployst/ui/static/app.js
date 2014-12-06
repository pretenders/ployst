/**
 * Ployst main angular module
 * @example
 *     <div ng-app="ployst">
 *     </div>
 */
var ployst = angular.module('ployst', [
        'ngResource',
        'ngCookies',
        'ui.router',

        'ployst.navbar',
        'ployst.profile',
        'ployst.projects',
        'ployst.repos',

        'ployst.github'
    ])
    .constant('Django', {
        URL: URLS
    })
    .config([
        '$locationProvider', '$stateProvider', '$urlRouterProvider', 'Django',

        function($locationProvider, $stateProvider, $urlRouterProvider, Django) {

            $urlRouterProvider.otherwise('/projects');

            $stateProvider
                .state('profile', {
                    url: '/profile',
                    controller: 'profile',
                    templateUrl: Django.URL.STATIC + 'profile/profile.html',
                    menu: 'profile'
                })
                .state('projects', {
                    url: '/projects',
                    controller: 'ProjectController',
                    templateUrl: Django.URL.STATIC + 'projects/projects.html',
                    menu: 'projects'
                });

            $locationProvider.html5Mode(false);
        }
    ])
    .run([
        '$http', '$cookies', '$state',

        function($http, $cookies, $state) {
            $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
            //$state.transitionTo('projects');
        }
    ]);
