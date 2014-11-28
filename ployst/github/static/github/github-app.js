(function() {

    angular.module('ployst.github', [
            'ployst.repos'
        ])
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
                return $resource('/github/oauth-access-token');
            }
        ])
        .controller('github', [
            '$scope', 'github.Token', 'github.Organisations',
            'github.OrgRepos', 'github.Repos', 'Repos',

            function($scope, GHToken, GHOrganisations, GHOrgRepos, GHRepos, Repos)
            {

                var repoCount = {},
                    trackedRepos = {};

                $scope.hasToken = null;
                $scope.repos = null;
                $scope.organisations = null;
                $scope.selectedOrganisation = null;
                $scope.myGithubLogin = null;

                var loadData = function() {
                    Repos.query({project: $scope.projectId}, function(repos) {
                        angular.forEach(repos, function(repo) {
                            repoCount[repo.owner] = (repoCount[repo.owner] || 0) + 1;
                            trackedRepos[repo.owner + '/' + repo.name] = true;
                        });

                        GHOrganisations.query(function(orgs) {
                            $scope.organisations = orgs;
                            // we rely on the backend API giving us the user's
                            // personal account as the first organisation:
                            $scope.myGithubLogin = orgs[0].login;
                            angular.forEach(orgs, function(org) {
                                org.trackedRepos = repoCount[org.login];
                            });

                            $scope.selectOrganisation(orgs[0]);
                        });
                    });
                };


                var incorporateRepos = function(repos) {
                    var owner = $scope.selectedOrganisation.login;
                    $scope.repos = repos;
                    angular.forEach(repos, function(repo) {
                        repo.tracked = trackedRepos[owner + '/' + repo.name] || false;
                    });

                };

                $scope.selectOrganisation = function(org) {
                    $scope.selectedOrganisation = org;
                    $scope.repos = null;

                    if (org.type === 'User') {
                        GHRepos.query(function(repos) {
                            incorporateRepos(repos);
                        });
                    } else {
                        GHOrgRepos.query({id: org.login}, function (repos) {
                            incorporateRepos(repos);
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
                templateUrl: STATIC_URL + 'github/github-config.html',
                scope: {
                    projectId: '='
                }
            };
        });
})();
