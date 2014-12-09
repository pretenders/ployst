describe('test GithubController', function() {

    var ctrl,
        scope,
        tokens = [{
            'token': '1234',
            'identifier': 'github',
            'id': 1,
            'user': 2
        }],
        mockUser = {
            username: 'user-1',
            id: 1
        },
        mockOrganisations = [
            {
                'type': 'User',
                'name': 'Me',
                'login': 'me'
            },
            {
                'login': 'org'
            }
        ],
        mockRepos = [
            {
                'name': 'somecode',
                'description': 'Some code',
                tracked: false
            },
            {
                'name': 'else',
                'description': 'Some oher code',
                tracked: false
            }
        ],
        projectRepos = [];

    beforeEach(module('ployst'));

    beforeEach(
        inject(function(_$httpBackend_, $controller, $rootScope, User) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/core/accounts/me').respond(mockUser);
            $httpBackend.expectGET('/github/oauth-access-token').respond(tokens);
            $httpBackend.expectGET('/core/repos/repo?project=5').respond(projectRepos);
            $httpBackend.expectGET('/github/user-orgs').respond(mockOrganisations);
            $httpBackend.expectGET('/github/user-repos').respond(mockRepos);

            User.user = mockUser;

            scope = $rootScope.$new();
            scope.project = {id: 5};
            ctrl = $controller(
                'GithubController', {
                    $scope: scope
                }
            );
        })
    );

    beforeEach(function() {
        $httpBackend.flush();
    });

    it('scope contains orgs and repos', function() {
        var i;
        for(i=0; i<mockOrganisations.length; i++) {
            expect(scope.organisations[0]).toNgEqual(mockOrganisations[0]);
        }
        for(i=0; i<mockRepos.length; i++) {
            expect(scope.repos[i]).toNgEqual(mockRepos[i]);
        }
        expect(scope.selectedOrganisation).toBe(scope.organisations[0]);
        expect(scope.myGithubLogin).toBe('me');
    });

});
