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
    .controller('GithubController', [
        '$scope', 'github.Token', 'github.Organisations',
        'github.OrgRepos', 'github.Repos', 'Repos',

        function($scope, GHToken, GHOrganisations, GHOrgRepos, GHRepos, Repos)
        {

            var repoCount = {},      // map owner to number of tracked repos
                trackedRepos = {};   // map "<owner>/<repo>" to bool for fast lookup

            $scope.hasToken = null;
            $scope.repos = null;
            $scope.organisations = null;
            $scope.selectedOrganisation = null;
            $scope.myGithubLogin = null;

            var loadData = function() {
                Repos.query({project: $scope.project.id}, function(projectRepos) {
                    GHOrganisations.query(function(orgs) {
                        $scope.organisations = orgs;
                        // we rely on the backend API giving us the user's
                        // personal account as the first organisation:
                        $scope.myGithubLogin = orgs[0].login;
                        collectStats(projectRepos);

                        $scope.selectOrganisation(orgs[0]);
                    });
                });
            };

            var k = function(owner, name) {
                return owner + '/' + name;
            };

            var collectStats = function(projectRepos) {
                repoCount = {};
                trackedRepos = {};
                angular.forEach(projectRepos, function(repo) {
                    repoCount[repo.owner] = (repoCount[repo.owner] || 0) + 1;
                    trackedRepos[k(repo.owner, repo.name)] = repo.id;
                });
                angular.forEach($scope.organisations, function(org) {
                    org.trackedRepos = repoCount[org.login];
                });
            };

            var processRepos = function(repos) {
                var owner = $scope.selectedOrganisation.login;
                $scope.repos = repos;
                angular.forEach(repos, function(repo) {
                    repo.tracked = trackedRepos[k(owner, repo.name)] || false;
                });

            };

            $scope.selectOrganisation = function(org) {
                $scope.selectedOrganisation = org;
                $scope.repos = null;

                if (org.type === 'User') {
                    GHRepos.query(function(repos) {
                        processRepos(repos);
                    });
                } else {
                    GHOrgRepos.query({id: org.login}, function (repos) {
                        processRepos(repos);
                    });
                }

            };

            $scope.trackRepo = function(repo) {
                var projectRepo = new Repos({
                    name: repo.name,
                    owner: $scope.selectedOrganisation.login,
                    project: $scope.project.id
                });
                projectRepo.$save(function(projectRepo) {
                    repo.tracked = projectRepo.id;
                    $scope.selectedOrganisation.trackedRepos =
                        ($scope.selectedOrganisation.trackedRepos || 0) + 1;
                });
            };

            $scope.untrackRepo = function(repo) {
                Repos.delete({id: repo.tracked}, function() {
                    repo.tracked = false;
                    $scope.selectedOrganisation.trackedRepos =
                        ($scope.selectedOrganisation.trackedRepos || 0) - 1;
                });
            };

            GHToken.query(function(token) {
                if (token.length > 0) {
                    loadData();
                    $scope.hasToken = true;
                } else {
                    $scope.hasToken = false;
                }
            });

            // ensure that when current project ID changes, we reload
            $scope.$watch(function() {
                return $scope.project.id;
            }, function () {
                loadData();
            });
        }
    ])
    .directive('githubConfig', function() {
        return {
            controller: 'GithubController',
            restrict: 'E',
            templateUrl: STATIC_URL + 'github/github-config.html',
            scope: {
                project: '='
            }
        };
    });
