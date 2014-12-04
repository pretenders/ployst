describe('test projects controller', function() {

    var ctrl,
        scope,
        mockUser = {
            username: 'user-1',
            id: 1
        },
        mockProject = {
            users: [mockUser],
            managers: [1],
            id: 1,
            name: 'project-one'
        },
        mockProjects = [mockProject],
        _Project;

    beforeEach(module('ployst'));

    beforeEach(inject(
        function(_$httpBackend_, $controller, $rootScope, User) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/core/accounts/me').respond(mockUser);
            $httpBackend.expectGET('/core/accounts/project').respond(mockProjects);
            User.user = mockUser;

            scope = $rootScope.$new();
            ctrl = $controller(
                'projects', {
                    $scope: scope
                }
            );
        }));

    beforeEach(function() {
        $httpBackend.flush();
    });

    it('scope contains projects, first project is preselected', function() {
        expect(scope.ps.projects[0].name).toBe('project-one');
        expect(scope.ps.project).toBe(scope.ps.projects[0]);
        expect(scope.ps.project.managers).toEqual([mockUser.id]);
    });

    it('can delete a project', function() {
        $httpBackend.expectDELETE('/core/accounts/project/1').respond();
        scope.ps.deleteProject(mockProject);
        $httpBackend.flush();
        expect(scope.ps.projects.length).toBe(0);
        expect(scope.ps.project).toBe(null);
    });

    it('can create a project, and it becomes the active project', function() {
        var mockProject2 = {
            users: [mockUser],
            id: 2,
            name: 'project-two'
        };
        $httpBackend.expectPOST('/core/accounts/project')
            .respond(mockProject2);
        $httpBackend.expectGET('/core/accounts/project/2')
            .respond(mockProject2);
        scope.ps.createProject({
            name: 'project-two'
        });
        $httpBackend.flush();
        expect(scope.ps.projects.length).toBe(2);
        expect(scope.ps.project.name).toEqual(mockProject2.name);
    });

});
