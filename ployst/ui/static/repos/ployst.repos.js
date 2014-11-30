/**
 * Ployst project management page
 */
angular.module('ployst.repos', [
        'ngResource'
    ])
    .factory('Repos', [
        '$resource',

        function($resource) {
            return $resource('/core/repos/repo');
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
    .controller('BranchController', [
        '$scope', 'Branches',

        function($scope, Branches) {
            $scope.branches = [];

            Branches.query({'repo__project': $scope.project.id}, function(branches) {
                $scope.branches = branches;
            });
        }
    ])
    .directive('projectActivity', function() {
        return {
            controller: 'BranchController',
            restrict: 'E',
            templateUrl: STATIC_URL + 'repos/project-branches.html',
            scope: {
                project: '='
            }
        };
    });

