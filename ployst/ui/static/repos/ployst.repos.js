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
    .service('RepoService', [
        'Repos',

        function(Repos) {
            this.getRepos = function(projectId) {
                return Repos.query({project: projectId});
            };
        }
    ]);
