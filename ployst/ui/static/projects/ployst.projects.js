/**
 * Ployst project management page
 */
angular.module('ployst.projects', [
        'ngResource'
    ])
    .factory('Project', [
        '$resource',

        function($resource) {
            return $resource('/core/accounts/project/:id');
        }
    ])
    .service('ProjectService', [
        '$filter',
        'lodash',
        'Project',

        function($filter, _, Project) {
            var $this = this;
            this.project = 'unknown';
            this.projects = [];
            this.startProject = null;

            this.setStartProject = function(projectName) {
                $this.startProject = projectName;
                if($this.projects.length > 0) {
                    this.selectProjectByName(projectName);
                }
            };

            this.setDefaultProject = function() {
                // set first project as active
                if ($this.projects.length > 0) {
                    $this.project = $this.projects[0];
                } else {
                    $this.project = null;
                }
            };

            this.selectProject = function(project) {
                $this.project = project;
            };

            this.selectProjectByName = function(name) {
                var found = _.find($this.projects, function(p) {
                    return name && p.name == name;
                });
                if(found) {
                    $this.project = found;
                } else {
                    $this.setDefaultProject();
                }
            };

            this.createProject = function(newProject) {
                var project = new Project({
                    name: newProject.name
                });
                project.$save(function(project) {
                    project = Project.get({
                        id: project.id
                    });
                    // Add to UI
                    $this.projects.push(project);
                    $this.project = project;
                    newProject.name = '';
                });
            };

            this.deleteProject = function(project) {
                Project.delete({
                    id: project.id
                }, function() {
                    // remove from list once deleted in backend
                    $this.projects.splice($this.projects.indexOf(project), 1);
                    $this.setDefaultProject();
                });
            };

            Project.query(function(projects) {
                $this.projects = projects;
                $this.selectProjectByName($this.startProject);
            });
        }
    ])
    .controller('ProjectController', [
        '$http', '$scope', '$stateParams', 'ProjectService', 'User',

        function($http, $scope, $stateParams, ProjectService, User) {
            $scope.newUser = {};
            $scope.user = User.user;
            $scope.ps = ProjectService;
            $scope.tab = 'activity';

            $scope.inviteUser = function(project, user) {
                // invite user to join project: if email is recognised, add to
                // project, else the user will be sent an invite to join ployst
                var url = '/core/accounts/project/' + project.id + '/invite_user';

                $http.post(url, {
                        email: user.email
                    })
                    .success(function(data, status, headers, config) {
                        // this callback will be called asynchronously
                        // when the response is available
                        project.users.push({
                            'user': data
                        });
                        user.email = '';
                    })
                    .error(function(data, status, headers, config) {
                        alert(data.error);
                    });
            };

            if($stateParams.project) {
                $scope.ps.setStartProject($stateParams.project);
            }
        }

    ])
    .directive('menuProjects', [
        'Django',

        function(Django) {
            return {
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'projects/menuProjects.html'
            };
        }
    ])
    .directive('project', [
        'Django',

        function(Django) {
            return {
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'projects/project.html'
            };
        }
    ])
    .directive('projectUsers', [
        'Django',

        function(Django) {
            return {
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'projects/projectUsers.html'
            };
        }
    ]);
