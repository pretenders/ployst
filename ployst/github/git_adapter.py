import git


class PythonGitAdapter(object):

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = git.Repo("{path}/.git".format(path=self.repo_path))
        self.remote = git.remote.Remote(self.repo, 'origin')

    def get_branches_and_heads(self):
        """
        Get branch names and latest commit found in the repo.

        :returns:
            A list of tuples containing branch name, head commit.
        """
        branches = []
        for remote_ref in self.remote.refs:
            if remote_ref.remote_head == "HEAD":
                continue
            branches.append((remote_ref.remote_head,
                            str(remote_ref.commit)))
        return branches

    def is_contained(self, commit, branch):
        """
        Is the commit given contained in the branch given.

        :returns:
            A boolean.
        """
        if not branch.startswith('origin'):
            branch = "origin/{}".format(branch)
        return commit in (c.hexsha for c in self.repo.iter_commits(branch))

    def fetch(self):
        """
        Fetch from the origin.
        """
        # TODO: This will need to be called.
        # TODO: We need to somehow use the ssh_key associated with the repo
        # when doing this.
        self.remote.fetch()
