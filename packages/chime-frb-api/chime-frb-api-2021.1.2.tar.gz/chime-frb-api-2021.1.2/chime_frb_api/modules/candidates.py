#!/usr/bin/env python

import logging

from chime_frb_api.core import API

log = logging.getLogger(__name__)


class Candidates:
    """
    CHIME/FRB Candidates API
    """

    def __init__(self, API: API):
        self.API = API

    def get_all_candidates(self) -> list:
        """
        Get all CHIME/FRB Candidates from Candidates Database
        Parameters
        ----------
            None
        Returns
        -------
            list
        """
        return self.API.get("/v1/candidates")
