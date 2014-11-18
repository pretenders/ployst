/**
 * Ployst project management page
 */
angular.module('ployst.projects', [
        'ngResource',
    ])
    .factory('Project', [
        '$resource',

        function($resource) {
            return $resource('/core/accounts/project/:id');
        }
    ])
    .controller('projects', [
        '$http', '$scope', 'Project', 'User',

        function($http, $scope, Project, User) {
            $scope.newUser = {};
            $scope.user = User.user;
            // prior to project loading, to avoid UI flicker with "no projects"
            // message:
            $scope.project = 'unknown';

            Project.query(function(projects) {
                $scope.projects = projects;
                $scope.setDefaultProject();
            });

            $scope.setDefaultProject = function() {
                // set first project as active
                if ($scope.projects.length > 0) {
                    $scope.project = $scope.projects[0];
                } else {
                    $scope.project = null;
                }
            };

            $scope.selectProject = function(project) {
                $scope.project = project;
            };

            $scope.createProject = function(newProject) {
                var project = new Project({
                    name: newProject.name
                });
                project.$save(function(project) {
                    project = Project.get({
                        id: project.id
                    });
                    // Add to UI
                    $scope.projects.push(project);
                    $scope.project = project;
                    newProject.name = '';
                });
            };

            $scope.deleteProject = function(project) {
                Project.delete({
                    id: project.id
                }, function() {
                    // remove from UI once deleted in backend
                    $scope.projects.splice($scope.projects.indexOf(project), 1);
                    $scope.setDefaultProject();
                });
            };

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
        }

    ])
    .directive('menuProjects',

        function() {
            return {
                restrict: 'E',
                templateUrl: STATIC_URL + 'projects/menuProjects.html'
            };
        }
    )
    .directive('projectUsers',

        function() {
            return {
                restrict: 'E',
                templateUrl: STATIC_URL + 'projects/projectUsers.html'
            };
        }
    );
