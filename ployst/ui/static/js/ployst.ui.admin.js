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

    ng.run = function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    };

    // controllers ----------------------------------------------------------

    ng.controllers = ng.controllers || {};

    ng.controllers.profile = function ($scope, User) {
        $scope.user = User.user;
    };

    ng.controllers.teams = function ($scope, Team, Project, User) {

        $scope.name = '';
        $scope.user = User.user;
        $scope.teams = Team.query();

        $scope.isManager = function(team, user) {
            return (team.managers.indexOf(user.id) !== -1);
        };

        $scope.deleteTeam = function(team) {
            Team.delete({guid: team.guid}, function() {
                // remove from UI once deleted in backend
                $scope.teams.splice($scope.teams.indexOf(team), 1);
            });
        };

        $scope.createProject = function(team, name, url) {
            var newProject = new Project({
                name: name,
                url: url,
                team: team.guid
                // managers: [$scope.user.id]
            });
            newProject.$save(function(project) {
                // remove from UI once deleted in backend
                team.projects.push(project);
            });
        };

        $scope.deleteProject = function(project) {
            Project.delete({id: project.id}, function() {
                // remove from UI once deleted in backend
                $.map($scope.teams, function(team) {
                    if(team.guid === project.team) {
                        team.projects.splice(
                            team.projects.indexOf(project), 1
                        );
                    }
                });
            });
        };
    };

    // directives -----------------------------------------------------------

    ng.directives = ng.directives || {};

    // factories ------------------------------------------------------------

    ng.factories = ng.factories || {};

    ng.factories.Project = function($resource) {
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

    ng.factories.Team = function($resource) {
        return $resource(
            '/core/accounts/team/:guid',
            {},
            {
                query: {
                    method: 'GET',
                    params: {guid: ''},
                    isArray: true
                }
            });
    };

    // services -------------------------------------------------------------

    ng.services = ng.services || {};

    ng.services.User = function($resource) {
        var userResource = $resource(
            '/core/accounts/me', {}, {query: {method: 'GET'}}
        );
        this.user = userResource.get();
    };
 
})();

