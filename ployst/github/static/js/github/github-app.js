(function() {

    angular.module('ployst')
        .factory('github.Organisations', [
            '$resource',
            function($resource) {
                return $resource('/github/user-orgs');
            }
        ])
        .factory('github.Repos', [
            '$resource',
            function($resource) {
                return $resource('/github/user-repos');
            }
        ])
        .factory('github.OrgRepos', [
            '$resource',
            function($resource) {
                return $resource(
                    '/github/org-repos/:id', {
                        id: '@id'
                    }
                );
            }
        ])
        .factory('github.Token', [
            '$resource',
            function($resource) {
                return $resource('/core/accounts/token?identifier=github');
            }
        ])
        .controller('github', [
            '$scope', 'github.Token', 'github.Organisations',
            'github.OrgRepos', 'github.Repos',
            function($scope, GHToken, GHOrganisations, GHOrgRepos, GHRepos) {

                $scope.hasToken = null;
                $scope.repos = null;
                $scope.organisations = null;

                var loadData = function() {
                    GHOrganisations.query(function(orgs) {
                        $scope.organisations = orgs;
                        $scope.selectedOrganisation = orgs[0];
                    });
                    GHRepos.query(function(repos) {
                        $scope.repos = repos;
                    });
                };

                $scope.selectOrganisation = function(org) {
                    $scope.selectedOrganisation = org;
                    $scope.repos = null;

                    if (org.type === 'User') {
                        GHRepos.query(function(repos) {
                            $scope.repos = repos;
                        });
                    } else {
                        GHOrgRepos.query({
                            id: org.login
                        }, function(repos) {
                            $scope.repos = repos;
                        });
                    }
                };

                GHToken.query(function(token) {
                    if (token.length > 0) {
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
        });
})();
