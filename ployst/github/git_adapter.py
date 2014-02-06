import git


class GitAdapter(object):

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.initialise()

    def initialise(self):
        pass

    def is_contained(self, commit, branch):
        """
        Is the commit given contained in the branch given.

        :returns:
            A boolean.
        """
        raise NotImplementedError(
            '"is_contained" should be implemented by subclasses of GitAdapter')

    def get_branches_and_heads(self):
        """
        Get branch names and latest commit found in the repo.

        :returns:
            A list of tuples containing branch name, head commit.
        """
        raise NotImplementedError(
            '"get_branches_and_heads" should be implemented by a subclass')

    def fetch(self):
        """
        Fetch from the origin.
        """
        raise NotImplementedError(
            '"fetch" must be implemented by subclasses of GitAdapter')


class PythonGitAdapter(GitAdapter):

    def initialise(self):
        self.repo = git.Repo("{path}/.git".format(path=self.repo_path))
        self.remote = git.remote.Remote(self.repo, 'origin')

    def get_branches_and_heads(self):
        branches = []
        for remote_ref in self.remote.refs:
            if remote_ref.remote_head == "HEAD":
                continue
            branches.append((remote_ref.remote_head,
                            str(remote_ref.commit)))
        return branches

    def is_contained(self, commit, branch):
        return commit in [c.hexsha for c in self.repo.iter_commits(branch)]

    def fetch(self):
        self.remote.fetch()
