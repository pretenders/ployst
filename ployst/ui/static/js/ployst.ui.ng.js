(function () {
    var ng = ployst.ng;
    ng.modules = ng.modules || {};

    /**
     * Ployst Angular module application {@link
     *     http://docs.angularjs.org/api/angular.module}
     * @example
     *     <div ng-app="ployst">
     *         <div ng-view></div>
     *     </div>
     */

    ng.modules.main = angular.module('ployst', [
            'ngRoute',
            'ngResource',
            'ngCookies'
        ])
        .config([
            '$routeProvider', '$locationProvider',
            ng.config.routing
        ])
        .factory('Projects', [
            '$resource', ng.factories.Projects
        ])
        .factory('Teams', [
            '$resource', ng.factories.Teams
        ])
        .factory('User', [
            '$resource',
            ng.factories.User
        ])
        .controller('profile', [
            '$scope', 'User',
            ng.controllers.profile
        ])
        .controller('teams', [
            '$scope', 'Teams', 'Projects',
            ng.controllers.teams
        ]);
})();

