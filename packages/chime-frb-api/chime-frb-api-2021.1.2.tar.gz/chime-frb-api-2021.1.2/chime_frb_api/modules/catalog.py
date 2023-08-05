#!/usr/bin/env python

import logging
import typing as t

from chime_frb_api.core import API

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]
log = logging.getLogger(__name__)


class Catalog:
    """
    CHIME/FRB Catalog API

    Parameters
    ----------
    API : chime_frb_api.core.API class-type

    Returns
    -------
    object-type
    """

    def __init__(self, API: API):
        self.API = API

    def get_catalog(self, version: int) -> JSON:
        """
        Fetches the CHIME/FRB Catalog.

        Parameters
        ----------
        version : int
            catalog version number, e.g. 1

        Returns
        -------
        catalog : dict
        """
        assert version, AttributeError(
            "catalog verison number is required. Try version=1 in the kwargs"
        )
        return self.API.get(f"/catalog/{version}")
