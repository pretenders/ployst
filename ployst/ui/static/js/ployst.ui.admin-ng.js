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
        .run([
            '$http', '$cookies',
            ng.run
        ])
        .config([
            '$routeProvider', '$locationProvider',
            ng.config.routing
        ])
        .factory('Project', [
            '$resource', ng.factories.Project
        ])
        .factory('Team', [
            '$resource', ng.factories.Team
        ])
        .service('User', [
            '$resource',
            ng.services.User
        ])
        .controller('profile', [
            '$scope', 'User',
            ng.controllers.profile
        ])
        .controller('teams', [
            '$http', '$scope', 'Project', 'Team', 'User',
            ng.controllers.teams
        ]);
})();

