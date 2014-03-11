(function () {
    window.ployst = window.ployst || {};
    ployst.ng = ployst.ng || {};

    var ng = ployst.ng;

    ng.config = ng.config || {};

    ng.config.routing = function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/profile', {
                controller: 'profile',
                templateUrl: STATIC_URL + 'templates/profile.html',
            })
            .when('/teams', {
                controller: 'teams',
                templateUrl: STATIC_URL + 'templates/teams.html',
            })
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

    ng.controllers.teams = function ($scope, Teams, Projects) {
        Teams.query('', function(teams) {
            $scope.teams = teams;
        });
        Projects.query('', function(projects) {
            $scope.projects = projects;
        });
    };

    //ng.directives = ng.directives || {};

    ng.factories = ng.factories || {};

    ng.factories.Projects = function($resource) {
        return $resource(
            '/core/accounts/project/:id',
            {},
            {
                query: {
                    method: 'GET',
                    params: {id: ''},
                    isArray: true
                }
            });
    };

    ng.factories.Teams = function($resource) {
        return $resource(
            '/core/accounts/team/:id',
            {},
            {
                query: {
                    method: 'GET',
                    params: {id: ''},
                    isArray: true
                }
            });
    };

    ng.factories.User = function($resource) {
        return $resource(
            '/core/accounts/me',
            {},
            {
                query: { method: 'GET' }
            });
    };
 
})();

