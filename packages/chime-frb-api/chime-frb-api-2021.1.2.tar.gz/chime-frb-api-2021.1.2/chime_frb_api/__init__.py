#!/usr/bin/env python
from pkg_resources import get_distribution as _get_distribution

import chime_frb_api.core
from chime_frb_api.backends import bucket, distributor, frb_master

__version__ = _get_distribution("chime_frb_api").version
