"""
Container for object classes used in cs18-api-client
"""
import abc

import dateutil.parser


class AccessLink:
    def __init__(self, protocol: str, link: str):
        self.link = link
        self.protocol = protocol


class Commit:
    def __init__(self, data: dict):
        self.sha = data["sha"]
        self.author = data["commit"]["author"]["name"]
        self.date = dateutil.parser.parse(data["commit"]["author"]["date"])
        self.comment = data["commit"]["message"]

    def __str__(self):
        return "{0}: [{1}] {2}".format(self.date, self.sha[:7], self.comment)


class ColonyAccount:
    def __init__(
            self, account: str, email: str, password: str, first_name: str, last_name: str
    ):
        self.account = account
        self.default_space = "Trial"
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class BlueprintRepositoryDetails:
    def __init__(self, repository_url: str, access_token: str, repository_type: str, branch: str = None):
        self.repository_url = repository_url
        self.repository_type = repository_type
        self.access_token = access_token
        self.branch = branch


class BitbucketBlueprintRepositoryDetails(BlueprintRepositoryDetails):
    def __init__(self, username: str, password: str, client_email: str, client_id: str, redirect_url: str,
                 repository_url: str, repository_type: str, branch: str = None):
        self.username = username
        self.password = password
        self.client_email = client_email
        self.client_id = client_id
        self.redirect_url = redirect_url
        access_token = ''
        super(BitbucketBlueprintRepositoryDetails, self).__init__(repository_url, access_token, repository_type, branch)


class AddAccountBlueprintRepositoryRequest(abc.ABC):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool):
        self.name = name
        self.repository_url = repository_url
        self.open_access = open_access
        self.allow_sharing = allow_sharing


class AddBlueprintUsingTokenRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, access_token: str, repository_type: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.repository_type = repository_type
        self.access_token = access_token


class AddBlueprintGithubRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, state: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.state = state


class AddBlueprintBitbucketRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, redirection_url: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.redirection_url = redirection_url
