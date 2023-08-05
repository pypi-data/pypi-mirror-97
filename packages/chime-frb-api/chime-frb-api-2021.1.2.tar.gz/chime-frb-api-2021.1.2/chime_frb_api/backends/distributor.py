#!/usr/bin/env python

import logging

from chime_frb_api.modules import distributor

log = logging.getLogger(__name__)


class Distributor(distributor.Distributor):
    """
    CHIME/FRB Distributor Backend
    """

    def __init__(self, debug: bool = False, **kwargs):
        # Instantiate Distributor Components
        super().__init__(debug=debug, **kwargs)
