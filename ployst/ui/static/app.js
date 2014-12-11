/**
 * Ployst angular app
 */
angular.module('ployst', [
        'ngResource',
        'ngCookies',
        'ngLodash',
        'ui.router',

        'ployst.base',
        'ployst.navbar',
        'ployst.profile',
        'ployst.projects',
        'ployst.repos',

        'ployst.github'
    ])
    .config([
        '$locationProvider', '$urlRouterProvider', 'Django',

        function($locationProvider, $urlRouterProvider, Django) {
            $urlRouterProvider.otherwise('/projects/');
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


/**
 * Ployst base set of low-level services to be used in multiple modules
 */
angular.module('ployst.base', [])
    .constant('Django', {
        URL: URLS
    });
