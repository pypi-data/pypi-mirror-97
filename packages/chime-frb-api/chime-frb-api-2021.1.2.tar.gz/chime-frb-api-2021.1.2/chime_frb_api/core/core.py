#!/usr/bin/env python
"""Core API Class Object."""
import logging
import warnings
from getpass import getpass
from os import environ
from time import ctime, time
from typing import List

import jwt
import requests

from chime_frb_api.core.exceptions import ConfigurationError, TokenError

from .json_type import JSON

# Configure Logger
logging_format = "[%(asctime)s] %(levelname)s "
logging_format += "%(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO)
log = logging.getLogger()


class API:
    """Application Programming Interface Base Class."""

    def __init__(self, debug: bool = False, **kwargs):
        """
         CHIME/FRB Core API Initialization

        Parameters
        ----------
        **kwargs: dict

        base_url : str
            Base URL for CHIME/FRB Master
        access_token : str
            Access token for authentiation
        refresh_token : str
            Refresh token to authentiation
        username : str
            CHIME username
        password : str
            CHIME password

        Returns
        -------
        class-type

        Raises
        ------
        APIError
            CHIME/FRB API Error
        """
        # base_url is set automatically now
        self.base_urls = kwargs.get("default_base_urls", [])
        if not debug:
            # Construct list of possible base_urls
            if kwargs.get("base_url"):
                self.base_urls.append(kwargs.get("base_url"))
            self.base_url = self._select_base_url(self.base_urls)
        else:
            log.warning("Debug Mode: Ignoring default base URLS")
            self.base_url = kwargs.get("base_url", None)

        # Create a requests session
        self._session = requests.Session()
        # Enable / Disable authentication
        self.authentication = kwargs.get("authentication", True)
        # Collect authentiation parameters if they were initialized
        self.access_token = kwargs.get("access_token", None)
        self.refresh_token = kwargs.get("refresh_token", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        # State Variables
        self.authorized = False
        self.expire_time = 0
        # Get configuration parameters from env
        self._config_from_env()
        self._check_configuration()

    def _config_from_env(self, environment: dict = None) -> None:
        """
        Get configuration parameters from os environment
        """
        if not environment:
            environment = dict(environ)
        if not self.access_token:
            self.access_token = environ.get("FRB_MASTER_ACCESS_TOKEN", None)
        if not self.refresh_token:
            self.refresh_token = environ.get("FRB_MASTER_REFRESH_TOKEN", None)
        if not self.username:
            self.username = environ.get("FRB_MASTER_USERNAME", None)
        if not self.password:
            self.password = environ.get("FRB_MASTER_PASSWORD", None)

    def _select_base_url(self, base_urls: List[str]) -> str:
        """Find the optimal base_url for HTTP Requests Session."""
        for base_url in base_urls:
            try:
                response = requests.get(base_url + "/version", timeout=1)
                if response.status_code == 200:
                    log.info(f"Base URL: {base_url}")
                    version = response.json().get("version")
                    log.info(f"Version : {version}")
                    return base_url
            except Exception as error:  # pragma: no cover
                log.error(f"Unable to connect @ {base_url}")
                log.error(error)

    def _check_configuration(self):
        """
        Check minimum configuration parameters
        """
        if not self.base_url:
            raise ConfigurationError("base_url not configured")

    def _coalesse_parameters(
        self,
        access_token: str = None,
        refresh_token: str = None,
        username: str = None,
        password: str = None,
    ):
        """
        Coalesse passed and configured parameters
        """
        # Gather authentication parameters if none were provided
        if not access_token:
            access_token = self.access_token
        if not refresh_token:
            refresh_token = self.refresh_token
        if not username:
            username = self.username
        if not password:
            password = self.password
        return access_token, refresh_token, username, password

    def _get_user_details(self, username: str = None, password: str = None):
        """
        Get user details from terminal input
        """
        if not username:  # pragma: no cover
            username = input("Username: ")
            # Save username for future uses
            self.username = username
        if not password:  # pragma: no cover
            # Get the password if we don't have it
            password = getpass("Password: ")
        return username, password

    def _check_authorization(self):
        """
        Check CHIME/FRB API Authorization Status
        """
        if self.authorized:
            # If authorized, check if access_token is valid
            if self.expire_time < time():  # pragma: no cover
                log.info("Authorization Status: Expired")
                self.reauthorize()
            else:
                log.debug("Authorization Status: Active")
        else:
            # If not currently authorized, do it.
            log.info("Authorization Status: None")
            self.authorize()

    def _set_expire_time(self, access_token: str = None):
        """
        Decode the JWT and find when it will expire
        """
        try:
            self.expire_time = jwt.decode(self.access_token, verify=False).get("exp", 0)
            log.info("Authorization Expiry: {}".format(ctime(self.expire_time)))
        except Exception as e:  # pragma: no cover
            log.warning(e)

    def _deprecation(self, message):  # pragma: no cover
        warnings.warn(message, DeprecationWarning, stacklevel=2)
        log.warning(message)

    ###########################################################################
    def authorize(
        self,
        access_token: str = None,
        refresh_token: str = None,
        username: str = None,
        password: str = None,
    ) -> bool:
        """
        Authentication

        Parameters
        ----------
        access_token : str
            CHIME/FRB Master JWT Token
        refresh_token : str
            CHIME/FRB Refresh Token
        username : str
            CHIME/FRB Username
        password : str
            CHIME/FRB Password

        Returns
        -------
        result : bool
            Result of the authorization
        """
        access_token, refresh_token, username, password = self._coalesse_parameters(
            access_token, refresh_token, username, password
        )
        try:
            # We already have access_token, check if it is valid
            if access_token:
                log.info("Authorization Method: Tokens")
                self._session.headers.update(authorization=access_token)
                response = self._session.get(self.base_url + "/auth/verify")
                response.raise_for_status
                # If response is good, return True
                if response.json().get("valid", False):
                    log.info("Authorization Result: Passed")
                    # Deposit Tokens
                    self.access_token = access_token
                    self.refresh_token = refresh_token
                    self._set_expire_time()
                    self.authorized = True
                    return True
                # Check if we have refresh token
                elif refresh_token:
                    log.info("Authorization Token : Expired")
                    # If reauth was successful, return True
                    if self.reauthorize():  # pragma: no cover
                        self.authorized = True
                        return True
                else:  # pragma: no cover
                    log.warning("Token Authorization Failed")
                    # Remove bad
                    self._session.headers.pop("authorization", None)

            # If token authentiation was not successful try user/pass
            log.info("Authorization Method: Username/Password")
            username, password = self._get_user_details(
                username=username, password=password
            )
            payload: dict = {}
            payload.update(username=username, password=password)
            response = self._session.post(url=self.base_url + "/auth", json=payload)
            response.raise_for_status()
            log.info("Authorization Result: Passed")
            tokens = response.json()
            log.debug(tokens)
            self.username = username
            self.access_token = tokens.get("access_token", None)
            self.refresh_token = tokens.get("refresh_token", None)
            self._session.headers.update(authorization=self.access_token)
            self._set_expire_time()
            self.authorized = True
            return True
        except requests.exceptions.RequestException as e:
            log.error("Authorization Failed")
            self.expire_time = 0
            self.authorized = False
            self._session.headers.pop("authorization", None)
            log.error(e)
            raise e

    def reauthorize(self, access_token: str = None, refresh_token: str = None) -> bool:
        """
        Re-authentication

        Parameters
        ----------
        access_token : str
            CHIME/FRB Master JWT Token
        refresh_token : str
            CHIME/FRB Refresh Token
        username : str
            CHIME/FRB Username
        password : str
            CHIME/FRB Password

        Returns
        -------
        result : bool
            Result of the authorization
        """
        access_token, refresh_token, username, password = self._coalesse_parameters(
            access_token, refresh_token
        )
        try:
            if not (refresh_token or access_token):
                raise TokenError("missing either refresh_token or access_token")
            log.info("Reauthorize Method: Tokens")
            self._session.headers.update(authorization=access_token)
            payload = {}
            payload.update(refresh_token=refresh_token)
            response = self._session.post(self.base_url + "/auth/refresh", json=payload)
            response.raise_for_status()
            tokens = response.json()
            log.debug(tokens)
            self.access_token = tokens.get("access_token", None)
            self.refresh_token = refresh_token
            self._set_expire_time()
            self._session.headers.update(authorization=self.access_token)
            log.info("Reauthorize Result: Passed")
            return True
        except requests.exceptions.RequestException as e:
            log.error("Re-authorize Result: Failed")
            self.access_token = None
            self.refresh_token = None
            self.expire_time = 0
            self.authorized = False
            raise e

    ###########################################################################
    def post(self, url: str, **kwargs) -> JSON:
        """
        HTTP POST

        Parameters
        ----------
        url : str
            HTTP URL
        **kwargs : dict
            Keyworded arguments synonmous to requests.post

        Returns
        -------
        response : json
            JSON encoded server response

        Raises
        ------
        requests.exceptions.RequestException
        """
        try:
            if self.authentication:
                self._check_authorization()
            response = self._session.post(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def patch(self, url: str, **kwargs) -> JSON:
        """
        HTTP PATCH
        """
        try:
            if self.authentication:
                self._check_authorization()
            response = self._session.patch(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:  # pragma: no cover
            raise e

    def get(self, url: str, **kwargs) -> JSON:
        """
        HTTP GET
        """
        try:
            if self.authentication:
                self._check_authorization()
            response = self._session.get(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def delete(self, url: str, **kwargs) -> JSON:
        """
        HTTP DELETE
        """
        try:
            if self.authentication:  # pragma: no cover
                self._check_authorization()
            response = self._session.delete(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise e

    def put(self, url: str, **kwargs) -> JSON:
        """
        HTTP PUT
        """
        try:
            if self.authentication:
                self._check_authorization()
            response = self._session.put(self.base_url + url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e

    def stream(self, url: str, request_type: str, **kwargs):
        """
        HTTP Stream
        """
        try:  # pragma: no cover
            if self.authentication:
                self._check_authorization()
            if request_type == "POST":
                response = self._session.post(
                    self.base_url + url, stream=True, **kwargs
                )
            elif request_type == "GET":
                response = self._session.get(self.base_url + url, **kwargs)
            else:
                raise ConfigurationError("request_type ['POST' or 'GET'] is required.")
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:  # pragma: no cover
            raise e
