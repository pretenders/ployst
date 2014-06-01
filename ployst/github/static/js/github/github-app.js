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
        .factory('OrgRepos', [
            '$resource', function($resource) {
                return $resource(
                    '/providers/github/org-repos/:id',
                    {id: '@id'}
                );
            }
        ])
        .factory('GithubToken', [
            '$resource', function($resource) {
                return $resource('/core/accounts/token?identifier=github');
            }
        ])
        .controller('github', [
            '$scope', 'GithubToken', 'Organisations', 'OrgRepos', 'Repos',
            function($scope, GithubToken, Organisations, OrgRepos, Repos) {

                $scope.hasToken = null;
                $scope.repos = null;

                var loadData = function() {
                    Organisations.query(function(orgs) {
                        $scope.organisations = orgs;
                        $scope.selectedOrganisation = orgs[0];
                    });
                    Repos.query(function(repos) {
                        $scope.repos = repos;
                    });
                };

                $scope.selectOrganisation = function(org) {
                    $scope.selectedOrganisation = org;
                    $scope.repos = null;

                    if(org.type === 'User') {
                        Repos.query(function(repos) {
                            $scope.repos = repos;
                        });
                    } else {
                        OrgRepos.query({id: org.login}, function(repos) {
                            $scope.repos = repos;
                        });
                    }
                };

                GithubToken.query(function(token) {
                    if(token.length > 0) {
                        loadData();
                        $scope.hasToken = true;
                    } else {
                        $scope.hasToken = false;
                    }
                });
            }
        ])
        .directive('githubConfig', function() {
            return {
                controller: 'github',
                restrict: 'E',
                templateUrl: STATIC_URL + 'templates/github/config.html'
            };
        })
        ;
})();
