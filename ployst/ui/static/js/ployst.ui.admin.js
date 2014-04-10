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
                menu: 'profile'
            })
            .when('/teams', {
                controller: 'teams',
                templateUrl: STATIC_URL + 'templates/teams.html',
                menu: 'teams'
            })
            .when('/providers/:provider?', {
                controller: 'providers',
                templateUrl: STATIC_URL + 'templates/providers.html',
                menu: 'providers'
            })
            .otherwise({
                redirectTo: '/profile'
            });
        $locationProvider.html5Mode(false);
    };

    ng.run = function ($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    };

    // controllers ----------------------------------------------------------

    ng.controllers = ng.controllers || {};

    ng.controllers.profile = function ($route, $scope, User) {
        $scope.user = User.user;
        $scope.menu = $route.current.$$route.menu;
    };

    ng.controllers.providers = function (
        $location, $routeParams, $scope, Provider
    ) {

        // Select active provider once they have loaded
        Provider.providers.$promise.then(function(result) {
            $scope.providers = result;
            var found = false;

            if ($routeParams.provider) {
                found = $.grep($scope.providers, function(item, i) {
                    return ($routeParams.provider === item.slug);
                });
                $scope.provider = found[0];
            } else {
                provider = $scope.providers[0];
                $location.path('/providers/' + provider.slug);
            }
        });
    };

    ng.controllers.teams = function ($http, $scope, Project, Team, User) {
        $scope.newProject = {};
        $scope.newUser = {};
        $scope.user = User.user;
        // prior to team loading, to avoid UI flicker with "no teams" message:
        $scope.team = 'unknown';

        Team.query(function(teams) {
            $scope.teams = teams;
            $scope.setDefaultTeam();
        });

        $scope.isManager = function(team, user) {
            return (team.managers.indexOf(user.id) !== -1);
        };

        $scope.setDefaultTeam = function() {
            // set first team as active
            if($scope.teams.length > 0) {
                $scope.team = $scope.teams[0];
            } else {
                $scope.team = null;
            }
        };

        $scope.selectTeam = function(team) {
            $scope.team = team;
        };

        $scope.createTeam = function(newTeam) {
            var team = new Team({name: newTeam.name});
            team.$save(function(team) {
                // Add to UI
                $scope.teams.push(team);
                $scope.team = team;
                newTeam.name = '';
            });
        };

        $scope.deleteTeam = function(team) {
            Team.delete({guid: team.guid}, function() {
                // remove from UI once deleted in backend
                $scope.teams.splice($scope.teams.indexOf(team), 1);
                $scope.setDefaultTeam();
            });
        };

        $scope.inviteUser = function(team, user) {
            // invite user to join team: if email is recognised, add to team,
            // else the user will be sent an invite to join ployst
            var url = '/core/accounts/team/' + team.guid + '/invite_user';

            $http.post(url, {email: user.email})
                .success(function(data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    team.users.push(data);
                    user.email = '';
                })
                .error(function(data, status, headers, config) {
                    alert(data.error);
                }
            );
        };

        $scope.createProject = function(team, newProject) {
            var project = new Project({
                name: newProject.name,
                url: newProject.url,
                team: team.guid
                // managers: [$scope.user.id]
            });
            project.$save(function(project) {
                // remove from UI once deleted in backend
                team.projects.push(project);
                newProject.name = '';
                newProject.url = '';
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

    ng.directives.mainMenu = function () {
        return {
            restrict: 'E',
            templateUrl: STATIC_URL + 'templates/mainMenu.html',
            controller: 'profile',
            transclude: true,
            replace: true,
            scope: {
                collapsed: '@menuCollapsed'
            }
        };
    };

    ng.directives.menuTeams = function () {
        return {
            restrict: 'E',
            templateUrl: STATIC_URL + 'templates/menuTeams.html'
        };
    };

    ng.directives.menuProviders = function () {
        return {
            restrict: 'E',
            templateUrl: STATIC_URL + 'templates/menuProviders.html'
        };
    };


    // factories ------------------------------------------------------------

    ng.factories = ng.factories || {};

    ng.factories.Project = function($resource) {
        return $resource('/core/accounts/project/:id');
    };

    ng.factories.Team = function($resource) {
        return $resource('/core/accounts/team/:guid');
    };

    // services -------------------------------------------------------------

    ng.services = ng.services || {};

    ng.services.User = function($resource) {
        var userResource = $resource('/core/accounts/me');
        this.user = userResource.get();
    };

    ng.services.Provider = function($resource) {
        var providerResource = $resource('/core/providers');
        this.providers = providerResource.query();
    };

})();
