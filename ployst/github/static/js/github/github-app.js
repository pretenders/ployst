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
        .controller('githubCtl', [
            '$scope', 'GithubToken', 'Organisations', 'OrgRepos', 'Repos',
            function($scope, GithubToken, Organisations, OrgRepos, Repos) {

                $scope.hasToken = false;

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
                    $scope.repos = [];
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
