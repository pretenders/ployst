describe('test teams controller', function () {

    var ctrl,
        scope,
        mockUser = {username: 'user-1', id: 1},
        mockTeam = {
            users: [mockUser],
            managers: [1],
            projects: [],
            guid: 'guid-one',
            name: 'team-one'
        },
        mockTeams = [mockTeam],
        _Team;

    beforeEach(module('ployst'));

    beforeEach(inject(
        function(_$httpBackend_, $controller, $rootScope, $route, Project,
                 Team, User)
        {
            $httpBackend = _$httpBackend_;
            $httpBackend.expectGET('/core/accounts/me')
                        .respond(mockUser);
            $httpBackend.expectGET('/core/accounts/team')
                        .respond(mockTeams);
            $httpBackend.expectGET('/static/templates/profile.html')
                        .respond();
            User.user = mockUser;
            _Team = Team;

            scope = $rootScope.$new();
            ctrl = $controller(
                ployst.ng.controllers.teams,
                {
                    $scope: scope
                }
            );
        })
    );

    beforeEach(function() {
        $httpBackend.flush();
    });

    it('scope contains teams, first team is preselected', function () {
        expect(scope.teams[0].name).toBe('team-one');
        expect(scope.team).toBe(scope.teams[0]);
        expect(scope.team.managers).toEqual([mockUser.id]);
    });

    it('can determine manager', function () {
        var mockUnrelatedUser = {username: 'user-2', id: 2};

        expect(scope.isManager(scope.team, mockUser)).toBe(true);
        expect(scope.isManager(scope.team, mockUnrelatedUser)).toBe(false);
    });

    it('can delete a team', function () {
        $httpBackend.expectDELETE('/core/accounts/team/guid-one')
                    .respond();
        scope.deleteTeam(mockTeam);
        $httpBackend.flush();
        expect(scope.teams.length).toBe(0);
        expect(scope.team).toBe(null);
    });

    it('can create a team, and it becomes the active team', function () {
        var mockTeam2 = {
            users: [mockUser],
            managers: [1],
            projects: [],
            guid: 'guid-two',
            name: 'team-two'
        };
        $httpBackend.expectPOST('/core/accounts/team')
                    .respond(mockTeam2);
        scope.createTeam({name: 'team-two'});
        $httpBackend.flush();
        expect(scope.teams.length).toBe(2);
        expect(scope.team.name).toEqual(mockTeam2.name);
    });

});

