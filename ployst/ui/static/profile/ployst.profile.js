/**
 * Ployst user profile page and current user services
 */
angular.module('ployst.profile', [
        'ngResource',
        'ui.router',
        'ployst.base'
    ])
    .config([
        '$stateProvider', 'Django',

        function($stateProvider, Django) {
            $stateProvider
                .state('profile', {
                    url: '/profile',
                    controller: 'profile',
                    templateUrl: Django.URL.STATIC + 'profile/profile.html',
                    menu: 'profile'
                });
        }
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
