/**
 * Ployst data providers management
 *
 * Enable and disable providers in ployst, and manage provider-specific
 * settings.
 */
angular.module('ployst.providers', [
        'ngResource',
        'ngRoute'
    ])
    .service('Provider', [
        '$resource',

        function($resource) {
            var providerResource = $resource('/core/providers');
            this.providers = providerResource.query();
        }
    ])
    .controller('providers', [
        '$compile', '$location', '$routeParams', '$scope', 'Provider',

        function($compile, $location, $routeParams, $scope, Provider) {

            // Select active provider once they have loaded
            Provider.providers.$promise.then(function(result) {
                $scope.providers = result;
                var found = false;

                if ($routeParams.provider) {
                    found = $.grep($scope.providers, function(item, i) {
                        return ($routeParams.provider === item.slug);
                    });
                    $scope.provider = found[0];
                } else {
                    $scope.provider = $scope.providers[0];
                    $location.path('/providers/' + $scope.provider.slug);
                }

                // insert directive for provider configuration
                var directive = $scope.provider.slug + '-config';
                directive = '<' + directive + '></' + directive + '>';
                var compiled = $compile(directive);
                var el = compiled($scope);
                angular.element('#provider-config').append(el);
            });
        }
    ]);
