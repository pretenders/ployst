/**
 * Ployst main angular module
 * @example
 *     <div ng-app="ployst">
 *     </div>
 */
var ployst = angular.module('ployst', [
        'ngRoute',
        'ngResource',
        'ngCookies',

        'ployst.django',
        'ployst.navbar',
        'ployst.profile',
        'ployst.projects',
        'ployst.providers',
        'ployst.repos',

        'ployst.github'
    ])
    .run([
        '$http', '$cookies',

        function($http, $cookies) {
            $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
        }
    ])
    .config([
        '$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
            $routeProvider
                .when('/profile', {
                    controller: 'profile',
                    templateUrl: STATIC_URL + 'profile/profile.html',
                    menu: 'profile'
                })
                .when('/projects', {
                    controller: 'projects',
                    templateUrl: STATIC_URL + 'projects/project.html',
                    menu: 'projects'
                })
                .otherwise({
                    redirectTo: '/profile'
                });
            $locationProvider.html5Mode(false);
        }
    ])
    .directive('mainMenu',

        function() {
            return {
                restrict: 'E',
                templateUrl: STATIC_URL + 'mainMenu.html',
                controller: 'profile',
                transclude: true,
                replace: true,
                scope: {
                    collapsed: '@menuCollapsed'
                }
            };
        }
    );
