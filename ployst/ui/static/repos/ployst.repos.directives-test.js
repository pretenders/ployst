describe('directive: project-activity', function() {
    var $compile,
        $rootScope,
        project = {
            name: 'Ployst',
            id: 1
        },
        mockRepo = {
            'id': 1,
            'name': 'ployst',
            'owner': 'pretenders',
            'branches': [{name: 'branch-one'}],
            'project': 1
        },
        mockRepos = [mockRepo];

    beforeEach(module('ployst'));
    beforeEach(module('templates'));

    beforeEach(inject(function(_$compile_, _$rootScope_) {
        $compile = _$compile_;
        $rootScope = _$rootScope_;
    }));

    beforeEach(inject(function(_$httpBackend_) {
        $httpBackend = _$httpBackend_;
        $httpBackend.expectGET('/core/repos/repo?project=1').respond(mockRepos);
    }));

    describe('with the initial value', function() {
        it('should include a list of repos', function() {
            var element = '<project-activity project="project"></project-activity>';
            var scope = $rootScope.$new();
            scope.project = project;
            element = $compile(element)(scope);
            scope = element.isolateScope();

            $rootScope.$digest();

            expect(element.controller).not.toBeNull();
            expect(element.html()).toContain('<th>Branch Name');
            //expect(element.html()).toContain('branch-one');
        });

    });

});
