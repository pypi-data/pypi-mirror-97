import attr
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, MissingSchema

from config import http, logger
from config.exceptions import RequestFailedException, RequestTokenException


@attr.s(slots=True)
class OAuth2:
    access_token_uri = attr.ib(type=str, validator=attr.validators.instance_of(str))
    client_id = attr.ib(type=str, validator=attr.validators.instance_of(str))
    client_secret = attr.ib(type=str, validator=attr.validators.instance_of(str))
    grant_type = attr.ib(
        type=str,
        default="client_credentials",
        validator=attr.validators.instance_of(str),
    )
    _token = attr.ib(type=str, default="", validator=attr.validators.instance_of(str))

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value) -> None:
        self._token = value
        logger.debug(f"access_token set: {self._token}")

    @property
    def authorization_header(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    def request_token(self, client_auth: HTTPBasicAuth, data: dict) -> None:
        try:
            response = http.post(self.access_token_uri, auth=client_auth, data=data)
            # response.raise_for_status()
        except MissingSchema:
            raise RequestFailedException("Access token URI it's empty")
        except HTTPError:
            raise RequestTokenException("Failed to retrieve oauth2 access_token.")
        self.token = response.json().get("access_token")
        logger.info("Access token successfully obtained.")

    def configure(self) -> None:
        client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {"grant_type": f"{self.grant_type}"}
        self.request_token(client_auth, data)
