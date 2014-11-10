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
            .when('/projects', {
                controller: 'projects',
                templateUrl: STATIC_URL + 'templates/projects.html',
                menu: 'projects'
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
        $compile, $location, $routeParams, $scope, Provider
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
                $scope.provider = $scope.providers[0];
                $location.path('/providers/' + $scope.provider.slug);
            }

            // insert directive for provider configuration
            var directive = $scope.provider.slug + '-config';
            directive = '<' + directive + '></' + directive + '>';
            var compiled = $compile(directive);
            var el = compiled($scope);
            angular.element('#provider-config').append(el);
        });
    };

    ng.controllers.projects = function ($http, $scope, Project, User) {
        $scope.newUser = {};
        $scope.user = User.user;
        // prior to project loading, to avoid UI flicker with "no projects"
        // message:
        $scope.project = 'unknown';

        Project.query(function(projects) {
            $scope.projects = projects;
            $scope.setDefaultProject();
        });

        $scope.isManager = function(project, user) {
            return (project.managers.indexOf(user.id) !== -1);
        };

        $scope.setDefaultProject = function() {
            // set first project as active
            if($scope.projects.length > 0) {
                $scope.project = $scope.projects[0];
            } else {
                $scope.project = null;
            }
        };

        $scope.selectProject = function(project) {
            $scope.project = project;
        };

        $scope.createProject = function(newProject) {
            var project = new Project({name: newProject.name});
            project.$save(function(project) {
                project = Project.get({id: project.id});
                // Add to UI
                $scope.projects.push(project);
                $scope.project = project;
                newProject.name = '';
            });
        };

        $scope.deleteProject = function(project) {
            Project.delete({id: project.id}, function() {
                // remove from UI once deleted in backend
                $scope.projects.splice($scope.projects.indexOf(project), 1);
                $scope.setDefaultProject();
            });
        };

        $scope.inviteUser = function(project, user) {
            // invite user to join project: if email is recognised, add to
            // project, else the user will be sent an invite to join ployst
            var url = '/core/accounts/project/' + project.guid + '/invite_user';

            $http.post(url, {email: user.email})
                .success(function(data, status, headers, config) {
                    // this callback will be called asynchronously
                    // when the response is available
                    project.users.push(data);
                    user.email = '';
                })
                .error(function(data, status, headers, config) {
                    alert(data.error);
                }
            );
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

    ng.directives.menuProjects = function () {
        return {
            restrict: 'E',
            templateUrl: STATIC_URL + 'templates/menuProjects.html'
        };
    };


    // factories ------------------------------------------------------------

    ng.factories = ng.factories || {};

    ng.factories.Project = function($resource) {
        return $resource('/core/accounts/project/:id');
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
