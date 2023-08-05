#!/usr/bin/env python

import logging
import typing as t

from chime_frb_api.core import API

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]
log = logging.getLogger(__name__)


class Sources:
    """
    CHIME/FRB Sources API

    Parameters
    ----------
    API : chime_frb_api.core.API class-type

    Returns
    -------
    object-type
    """

    def __init__(self, API: API):
        self.API = API

    def get_source(self, source_name: str) -> JSON:
        """
        Astrophysical Source from CHIME/FRB Master

        Parameters
        ----------
        source_name : str
            Source name, e.g. CAS_A

        Returns
        -------
        source : dict
        """
        assert source_name, AttributeError("source_name is required")
        return self.API.get(f"/v1/sources/{source_name}")

    def get_source_type(self, source_type: str = None) -> JSON:
        """
        Get CHIME/FRB sources based on type.

        Parameters
        ----------
        source_type : str
            One of ["FRB", "FRB_REPEATER", "PULSAR", "STEADY", "RRAT"]

        Returns
        -------
        sources : dict
            Returns a dict of all valid sources
        """
        valid = ["FRB", "FRB_REPEATER", "PULSAR", "STEADY", "RRAT"]
        assert source_type in valid, "source_type has to be a subset of {}".format(
            valid
        )
        return self.API.get(f"/v1/sources/search/type/{source_type}")

    def get_expected_spectrum(self, source_name: str) -> JSON:
        """
        Expected spectra for a CHIME/FRB Source

        Parameters
        ----------
        source_name : str
            Source name, e.g. CAS_A

        Returns
        -------
        spectrum : dict
            Returns dict with the following format
            {"freqs": [], "expected_spectrum": []}
        """
        assert source_name, AttributeError("source_name is required")
        return self.API.get(f"/v1/sources/spectrum/{source_name}")
