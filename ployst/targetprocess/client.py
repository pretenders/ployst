import apitopy


class TargetProcess(object):

    def __init__(self, domain, user, password, verbose=False):
        self.api = apitopy.Api(
            'https://{}/api/v1/'.format(domain),
            (user, password),
            verbose=verbose
        )

    def select_projects(self, *project_ids):
        context = self.api.Context(ids=",".join(map(str, project_ids)))
        self.acid = context.Acid
        return self.acid

    def get_entities(self, entity_type='Userstories'):
        """
        Assumes a project context has been selected
        """
        entities = getattr(self.api, entity_type)
        return entities(acid=self.acid, include='[Name,Owner]').Items

    @property
    def auth_token(self):
        "If we want to eventually authenticate via token"
        return self.api.Authentication().Token

    @property
    def projects(self):
        return self.api.Projects().Items

    @property
    def user_stories(self):
        return self.get_entities('Userstories')

    @property
    def features(self):
        return self.get_entities('Features')

    @property
    def bugs(self):
        return self.get_entities('Bugs')

    @property
    def teams(self):
        return self.api.Teams().Items
        # api.Teammembers()

    @property
    def users(self):
        return self.api.Users(where="IsActive eq 'true'").Items

    @property
    def project_members(self):
        return self.api.Projectmembers(acid=self.acid)
