/**
 * Ployst user profile page and current user services
 */
angular.module('ployst.profile', [
        'ngResource',
        'ngRoute'
    ])
    .service('User', [
        '$resource',

        function($resource) {
            var userResource = $resource('/core/accounts/me');
            this.user = userResource.get();
        }
    ])
    .controller('profile', [
        '$route', '$scope', 'User',

        function($route, $scope, User) {
            $scope.user = User.user;
            $scope.menu = $route.current.$$route.menu;
        }
    ]);
