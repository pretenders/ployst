/**
 * Ployst user profile page and current user services
 */
angular.module('ployst.profile', [
        'ngResource',
        'ui.router'
    ])
    .service('User', [
        '$resource',

        function($resource) {
            var userResource = $resource('/core/accounts/me');
            this.user = userResource.get();
        }
    ])
    .controller('profile', [
        '$state', '$scope', 'User',

        function($state, $scope, User) {
            $scope.user = User.user;
            $scope.menu = $state.current.menu;
        }
    ]);
