describe('test ProjectController', function() {

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
        mockProject2 = {
            users: [mockUser],
            managers: [1],
            id: 2,
            name: 'project-two'
        },
        mockProjects = [mockProject, mockProject2],
        _Project;

    beforeEach(module('ployst'));
    beforeEach(module('templates'));

    beforeEach(
        inject(function(_$httpBackend_, $controller, $rootScope, User) {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/core/accounts/me').respond(mockUser);
            $httpBackend.expectGET('/core/accounts/project').respond(mockProjects);

            User.user = mockUser;

            scope = $rootScope.$new();
            ctrl = $controller(
                'ProjectController', {
                    $scope: scope
                }
            );
        })
    );

    beforeEach(function() {
        $httpBackend.flush();
    });

    it('scope contains projects, first project is preselected', function() {
        expect(scope.ps.projects[0].name).toBe('project-one');
        expect(scope.ps.project).toBe(scope.ps.projects[0]);
        expect(scope.ps.project.managers).toEqual([mockUser.id]);
    });

    it('can create a project, and it becomes the active project', function() {
        var mockProject3 = {
            users: [mockUser],
            id: 3,
            name: 'project-three'
        };
        $httpBackend.expectPOST('/core/accounts/project')
            .respond(mockProject3);
        $httpBackend.expectGET('/core/accounts/project/3')
            .respond(mockProject3);
        scope.createProject({
            name: 'project-three'
        });
        $httpBackend.flush();
        expect(scope.ps.projects.length).toBe(3);
        expect(scope.ps.project.name).toEqual(mockProject3.name);
    });

    it('can delete a project', function() {
        $httpBackend.expectDELETE('/core/accounts/project/1').respond();
        scope.deleteProject(mockProject);
        $httpBackend.flush();
        expect(scope.ps.projects.length).toBe(1);
    });

    it('route contains project, that project is preselected',
        inject(function($controller) {
            ctrl = $controller('ProjectController', {
                $scope: scope,
                $stateParams: {project: 'project-two'}
            });
            expect(scope.ps.project.name).toBe('project-two');
        })
    );

});
