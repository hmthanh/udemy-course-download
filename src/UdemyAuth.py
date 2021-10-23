import cloudscraper
from requests.exceptions import ConnectionError as conn_error

from Session import Session
from src.utils import search_regex, hidden_inputs

LOGIN_URL = "https://www.udemy.com/join/login-popup/?ref=&display_type=popup&loc"
LOGOUT_URL = "https://www.udemy.com/user/logout"


class UdemyAuth(object):
    def __init__(self, username="", password="", cache_session=False):
        self.username = username
        self.password = password
        self._cache = cache_session
        self._session = Session()
        self._cloudsc = cloudscraper.create_scraper()

    def _form_hidden_input(self, form_id):
        try:
            resp = self._cloudsc.get(LOGIN_URL)
            resp.raise_for_status()
            webpage = resp.text
        except conn_error as error:
            raise error
        else:
            login_form = hidden_inputs(
                search_regex(
                    r'(?is)<form[^>]+?id=(["\'])%s\1[^>]*>(?P<form>.+?)</form>'
                    % form_id,
                    webpage,
                    "%s form" % form_id,
                    group="form",
                ))
            login_form.update({
                "email": self.username,
                "password": self.password
            })
            return login_form

    def authenticate(self, access_token="", client_id=""):
        if not access_token and not client_id:
            data = self._form_hidden_input(form_id="login-form")
            self._cloudsc.headers.update({"Referer": LOGIN_URL})
            auth_response = self._cloudsc.post(LOGIN_URL,
                                               data=data,
                                               allow_redirects=False)
            auth_cookies = auth_response.cookies

            access_token = auth_cookies.get("access_token", "")
            client_id = auth_cookies.get("client_id", "")

        if access_token:
            # dump cookies to configs
            # if self._cache:
            #     _ = to_configs(
            #         username=self.username,
            #         password=self.password,
            #         cookies=f"access_token={access_token}",
            #     )
            self._session._set_auth_headers(access_token=access_token,
                                            client_id=client_id)
            self._session._session.cookies.update(
                {"access_token": access_token})
            return self._session, access_token
        else:
            self._session._set_auth_headers()
            return None, None
