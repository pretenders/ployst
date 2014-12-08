/**
 * Ployst main angular module
 * @example
 *     <div ng-app="ployst">
 *     </div>
 */
var ployst = angular.module('ployst', [
        'ngResource',
        'ngCookies',
        'ngLodash',
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

            $urlRouterProvider.otherwise('/projects/');

            $stateProvider
                .state('profile', {
                    url: '/profile',
                    controller: 'profile',
                    templateUrl: Django.URL.STATIC + 'profile/profile.html',
                    menu: 'profile'
                })
                .state('projects', {
                    url: '/projects/:project',
                    controller: 'ProjectController',
                    templateUrl: Django.URL.STATIC + 'projects/projects.html',
                    menu: 'projects'
                });

            $locationProvider.html5Mode(false);
        }
    ])
    .run([
        '$http', '$cookies',

        function($http, $cookies) {
            $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
        }
    ])
    .directive('ngEnter', function () {
        return function (scope, element, attrs) {
            element.bind('keydown keypress', function (event) {
                if(event.which === 13) {
                    scope.$apply(function (){
                        scope.$eval(attrs.ngEnter);
                    });

                    event.preventDefault();
                }
            });
        };
    });
