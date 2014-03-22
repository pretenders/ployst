(function () {
    window.ployst = window.ployst || {};
    ployst.ng = ployst.ng || {};

    var ng = ployst.ng;

    ng.config = ng.config || {};

    ng.config.routing = function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/profile', {
                controller: 'profile',
                templateUrl: STATIC_URL + 'templates/profile.html'
            })
            .when('/teams', {
                controller: 'teams',
                templateUrl: STATIC_URL + 'templates/teams.html'
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

    ng.controllers.teams = function ($http, $scope, Project, Team, User) {
        $scope.newProject = {};
        $scope.newUser = {};
        $scope.user = User.user;
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

