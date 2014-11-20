describe('test profile scope', function () {

    var ctrl, scope, mockUser;
    mockUser = {username: 'my-name', email: 'me@ployst.com'};

    beforeEach(module('ployst'));

    beforeEach(inject(function($rootScope, $route, User, $controller) {
        User.user = mockUser;
        // mock routing
        $route.current = {'$$route': {menu: 'profile'}};

        scope = $rootScope.$new();
        ctrl = $controller(
            'profile',
            {$scope: scope}
        );
    }));

    it('should include user with username and email', function () {
        expect(scope.user.username).toBe('my-name');
        expect(scope.user.email).toBe('me@ployst.com');
    });

});
