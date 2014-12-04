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

        'ployst.navbar',
        'ployst.profile',
        'ployst.projects',
        'ployst.providers',
        'ployst.repos',

        'ployst.github'
    ])
    .constant('Django', {
        URL: URLS
    })
    .run([
        '$http', '$cookies',

        function($http, $cookies) {
            $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
        }
    ])
    .config([
        '$routeProvider', '$locationProvider', 'Django',

        function($routeProvider, $locationProvider, Django) {
            $routeProvider
                .when('/profile', {
                    controller: 'profile',
                    templateUrl: Django.URL.STATIC + 'profile/profile.html',
                    menu: 'profile'
                })
                .when('/projects', {
                    controller: 'projects',
                    templateUrl: Django.URL.STATIC + 'projects/project.html',
                    menu: 'projects'
                })
                .otherwise({
                    redirectTo: '/projects'
                });
            $locationProvider.html5Mode(false);
        }
    ])
    .directive('mainMenu',

        function() {
            return {
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'mainMenu.html',
                controller: 'profile',
                transclude: true,
                replace: true,
                scope: {
                    collapsed: '@menuCollapsed'
                }
            };
        }
    );
