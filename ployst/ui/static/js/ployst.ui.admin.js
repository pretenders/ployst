(function () {
    window.ployst = window.ployst || {};
    ployst.ng = ployst.ng || {};

    var ng = ployst.ng;

    ng.config = ng.config || {};

    ng.config.routing = function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/profile', {
                controller: 'profile',
                templateUrl: '/static/templates/profile.html',
            })
            //.when('/teams', {
                //controller: 'teams',
                //templateUrl: STATIC_URL + 'templates/teams.html.tmpl',
            //})
            .otherwise({
                redirectTo: '/profile'
            });
        $locationProvider.html5Mode(false);
    };

    ng.controllers = ng.controllers || {};

    ng.controllers.profile = function ($scope, User) {
        User.query('', function(user) {
            $scope.user = user;
        });
    };

    //ng.controllers.teams = function ($scope, $rootScope, $route) {
        //$scope.exists = false;
    //};

    //ng.directives = ng.directives || {};

    ng.factories = ng.factories || {};

    //ng.factories.Teams = function($resource) {
        //return $resource(
            //'/core/accounts/team/:id',
            //{},
            //{
                //query: {
                    //method: 'GET',
                    //params: {id: ''},
                    //isArray: true
                //}
            //});
    //};

    ng.factories.User = function($resource) {
        return $resource(
            '/core/accounts/me',
            {},
            {
                query: { method: 'GET' }
            });
    };
 
})();

