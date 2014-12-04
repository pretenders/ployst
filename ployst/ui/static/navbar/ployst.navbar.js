/**
 * Ployst user profile page and current user services
 */
angular.module('ployst.navbar', [
        'ployst.projects',
        'ployst.profile'
    ])
    .controller('NavbarController', [
        '$scope', 'Django', 'ProjectService', 'User',

        function($scope, Django, ProjectService, User) {
            $scope.user = User.user;
            $scope.URL = Django.URL;
        }
    ])
    .directive('navbar', [
        'Django',

        function(Django) {
            return {
                controller: 'NavbarController',
                restrict: 'E',
                templateUrl: Django.URL.STATIC + 'navbar/navbar.html'
            };
        }
    ]);
