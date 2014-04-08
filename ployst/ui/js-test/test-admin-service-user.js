describe('test user service', function () {

    var service,
        scope,
        $httpBackend,
        mockUser = {username: 'my-name', email: 'me@ployst.com'};

    beforeEach(module('ployst'));

    beforeEach(inject(function(_$httpBackend_, $rootScope, User) {
        $httpBackend = _$httpBackend_;
        $httpBackend.expectGET('/core/accounts/me')
                    .respond(mockUser);
        service = User;
    }));

    it('should include user with username and email', function () {
        $httpBackend.flush();
        expect(service.user.username).toBe('my-name');
        expect(service.user.email).toBe('me@ployst.com');
    });

});
