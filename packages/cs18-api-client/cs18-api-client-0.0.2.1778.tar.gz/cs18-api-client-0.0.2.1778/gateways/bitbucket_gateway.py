from __future__ import unicode_literals
from urllib.parse import urlparse, parse_qs

from requests import Session
from requests.auth import HTTPBasicAuth


class BitbucketGateway:

    def __init__(self, username, password, client_email, client_id, redirect_url: str):
        self.username = username
        self.password = password
        self.client_email = client_email
        self.client_id = client_id
        self.redirect_url = redirect_url
        self.session = Session()

    def __enter__(self):
        self.session = self.start_http_session(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @staticmethod
    def headers(email):
        headers = {
            'Accept': 'application/json',
            'From': email
        }
        return headers

    def start_http_session(self, session):
        session.headers.update(self.headers(email=self.client_email))
        session.auth = HTTPBasicAuth(self.username, self.password)
        return session

    def get_consumer_app_temporary_code(self):
        server_consumer_auth_base_url = 'https://bitbucket.org/site/oauth2/authorize'
        consumer_temp_code_url = \
            '{server_base_uri}?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}' \
                .format(server_base_uri=server_consumer_auth_base_url,
                        client_id=self.client_id,
                        scope='repository',
                        redirect_uri=self.redirect_url)

        response = self.session.get(consumer_temp_code_url, allow_redirects=False)
        code_array = parse_qs(urlparse(response.next.url).query).get('code')
        return code_array[0]
