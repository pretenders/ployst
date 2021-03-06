/**
 * Ployst project management page
 */
angular.module('ployst.repos', [
        'ngResource'
    ])
    .factory('Repos', [
        '$resource',

        function($resource) {
            return $resource('/core/repos/repo/:id');
        }
    ])
    .factory('Branches', [
        '$resource',

        function($resource) {
            return $resource('/core/repos/branch');
        }
    ])
    .service('RepoService', [
        'Repos',

        function(Repos) {
            this.getRepos = function(projectId) {
                return Repos.query({project: projectId});
            };
        }
    ])
    .controller('ActivityController', [
        '$scope', 'Repos',

        function($scope, Repos) {
            $scope.repos = [];
            $scope.branches = null;

            var loadData = function() {
                Repos.query({'project': $scope.project.id}, function (repos) {
                    $scope.repos = repos;
                    $scope.branches = [];
                    angular.forEach(repos, function (repo) {
                        angular.forEach(repo.branches, function (branch) {
                            branch.repo = repo.owner + '/' + repo.name;
                            $scope.branches.push(branch);
                        });
                    });
                });
            };

            // ensure that when current project ID changes, we reload
            $scope.$watch(function() {
                return $scope.project.id;
            }, function () {
                loadData();
            });
        }
    ])
    .directive('projectActivity', [
        'Django',

        function(Django) {
            return {
                controller: 'ActivityController',
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'repos/project-branches.html',
                scope: {
                    project: '='
                }
            };
        }
    ]);

