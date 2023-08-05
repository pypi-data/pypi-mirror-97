#!/usr/bin/env python

import logging

from chime_frb_api.core import API
from chime_frb_api.modules import (
    calibration,
    candidates,
    catalog,
    events,
    metrics,
    mimic,
    parameters,
    sources,
    swarm,
    tns,
    voe,
    voe_subscribers,
)

log = logging.getLogger(__name__)


class FRBMaster:
    """
    CHIME/FRB Master Backend
    """

    def __init__(self, debug: bool = False, **kwargs):
        # Instantiate FRB/Master Core API
        kwargs.setdefault(
            "default_base_urls",
            ["http://frb-vsop.chime:8001", "https://frb.chimenet.ca/frb-master"],
        )
        self.API = API(debug=debug, **kwargs)
        # Instantiate FRB Master Components
        self.swarm = swarm.Swarm(self.API)
        self.events = events.Events(self.API)
        self.parameters = parameters.Parameters(self.API)
        self.calibration = calibration.Calibration(self.API)
        self.metrics = metrics.Metrics(self.API)
        self.mimic = mimic.Mimic(self.API)
        self.sources = sources.Sources(self.API)
        self.voe = voe.Voe(self.API)
        self.voe_subscribers = voe_subscribers.VoeSubscribers(self.API)
        self.tns = tns.TNSAgent(self.API)
        self.candidates = candidates.Candidates(self.API)
        self.catalog = catalog.Catalog(self.API)

    def version(self) -> str:
        # Version of the frb-master API client is connected to
        try:
            return self.API.get("/version").get("version", "unknown")
        except Exception as e:  # pragma: no cover
            log.warning(e)
            return "unknown"
