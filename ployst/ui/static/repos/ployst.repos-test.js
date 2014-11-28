describe('test repos', function() {

    var ctrl,
        scope,
        mockUser = {
            username: 'me',
            id: 1
        },
        mockRepo = {
            'id': 1,
            'name': 'ployst',
            'owner': 'pretenders',
            'branches': [],
            'project': 1
        },
        mockRepos = [mockRepo],
        _Repo;

    beforeEach(module('ployst.repos'));

    beforeEach(inject(function(_$httpBackend_, RepoService) {
        $httpBackend = _$httpBackend_;
        _RepoService = RepoService;
    }));

    it('getRepos gives a list of repos for a project', function() {
        $httpBackend.expectGET('/core/repos/repo?project=1')
            .respond(mockRepos);
        repos = _RepoService.getRepos(1);
        $httpBackend.flush();
        expect(repos.length).toBe(1);
        expect(repos[0].name).toBe('ployst');
    });

});
