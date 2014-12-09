describe('directive: navbar', function() {
    var $compile,
        $httpBackend,
        $rootScope,
        mockUser = {
            username: 'me',
            id: 1
        };

    beforeEach(module('ployst'));
    beforeEach(module('/static/navbar/navbar.html'));
    beforeEach(module('/static/projects/projects.html'));

    beforeEach(inject(function(_$compile_, _$httpBackend_, _$rootScope_) {
        $httpBackend = _$httpBackend_;
        $compile = _$compile_;
        $rootScope = _$rootScope_;
        $httpBackend.whenGET('/core/accounts/me').respond(mockUser);
    }));

    describe('render navbar', function() {
        it('should include logout', function() {
            var element = angular.element('<navbar></navbar>');
            var scope = $rootScope.$new();

            element = $compile(element)(scope);
            $rootScope.$digest();

            scope = element.isolateScope();

            expect(element.html()).toContain('Logout');
        });
    });

});

