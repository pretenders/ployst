(function () {
    var ng = ployst.ng;
    ng.modules = ng.modules || {};

    ng.modules.main = angular.module('ployst')
        .factory('Organisations', [
            '$resource', function($resource) {
                return $resource('/providers/github/user-orgs');
            }
        ])
        .factory('Repos', [
            '$resource', function($resource) {
                return $resource('/providers/github/user-repos');
            }
        ])
        .factory('GithubToken', [
            '$resource', function($resource) {
                return $resource('/core/accounts/token?identifier=github');
            }
        ])
        .controller('githubCtl', [
            '$scope', 'GithubToken', 'Organisations', 'Repos',
            function($scope, GithubToken, Organisations, Repos) {

                $scope.hasToken = false;

                var loadData = function() {
                    Organisations.query(function(orgs) {
                        $scope.organisations = orgs;
                    });
                    Repos.query(function(repos) {
                        $scope.myRepos = repos;
                    });
                };

                GithubToken.query(function(token) {
                    if(token.length > 0) {
                        $scope.hasToken = true;
                        loadData();
                    }
                });
            }
        ])
        .directive('githubConfig', function() {
            return {
                controller: 'githubCtl',
                restrict: 'E',
                templateUrl: STATIC_URL + 'templates/github/config.html'
            };
        })
        ;
})();
