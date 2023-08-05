#!/usr/bin/env python

import logging
import typing as t

from chime_frb_api.core import API

log = logging.getLogger(__name__)
JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]


class Mimic:
    """
    CHIME/FRB Mimic API
    """

    def __init__(self, API: API):
        self.API = API

    def register_injection(self, **kwargs) -> JSON:
        """
        Register an injection

        Parameters
        ----------
            **kwargs : dict
            Refer to http://frb-vsop.chime:8001/swagger/#/Mimic%20API/Mimic%20API.test_mimic_injection

        Returns
        -------
            uuid : dict
                python dict of the uuids of the registered injection
        """
        return self.API.post(url="/v1/mimic/injection", json=kwargs)  # pragma: no cover

    def register_detection(self, **kwargs) -> JSON:
        """
        Register a detection

        Parameters
        ----------
            **kwargs : dic
            Refer to http://frb-vsop.chime:8001/swagger/#/Mimic%20API/Mimic%20API.test_mimic_injection

        Returns
        -------
        """
        return self.API.post(url="/v1/mimic/detection", json=kwargs)  # pragma: no cover

    def get_active_injections(self) -> JSON:
        """
        Get parameters for all currently active injections

        Parameters
        ----------
            None

        Returns
        -------
            active_injections: list
        """
        return self.API.get(url="/v1/mimic/active_injections")

    def get_simulated_event(self, uuid: str = None) -> JSON:
        """
        Get the injected and detected parameters for a specific UUID

        Parameters
        ----------
            uuid : str
                universally unique identifier for the specific simulated event

        Returns
        -------
            dict

        Raises
        ------
            AttributeError
        """
        if uuid:
            return self.API.get(url=f"/v1/mimic/{uuid}")
        else:
            raise AttributeError("uuid is required")

    def get_uuids(self) -> JSON:
        """
        Get UUIDs for all simulated events

        Parameters
        ----------
            None

        Returns
        -------
            dict
        """
        return self.API.get(url="/v1/mimic/uuids")
