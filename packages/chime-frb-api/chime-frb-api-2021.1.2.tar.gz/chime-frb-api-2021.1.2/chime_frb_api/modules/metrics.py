#!/usr/bin/env python

import logging
import typing as t

from chime_frb_api.core import API

log = logging.getLogger(__name__)
JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]


class Metrics:
    """
    CHIME/FRB Events API
    """

    def __init__(self, API: API):
        self.API = API

    def overview(self) -> JSON:
        """
        GET Metrics Configuration

        Parameters
        ----------
            None

        Returns
        -------
            JSON
        """
        return self.API.get(url="/v1/metrics/overview")

    def configure(
        self, description: str = "", category: str = None, names: [str] = None
    ):
        """
        Configure a new category of metrics

        Parameters
        ----------
        description : str
            Small description of the metrics being tracked
            e.g. L1 beams not sending packets
        category : str
            Unique category to track the metrics under
            e.g. deadbeams
        names : list
            List of strings, mapping to metric names to be tracked
            e.g. ["0","1000", "2000", "3000"]

        Returns
        -------
        status : dict
            Returns the status of the configuration, nominal response should be
        """
        if not category:
            raise AttributeError("category is required")

        for name in names:
            assert type(name) == str, "names can only be strings"

        payload = {"description": description, "category": category, "names": names}
        return self.API.post(url="/v1/metrics/configure", json=payload)

    def reconfigure(self, category: str = None, names: [str] = None):
        """
        Reconfigure/Update an existing metrics category

        Parameters
        ----------
        category : str
            Name of the metric category
        names : list
            A list of names (str) to be added

        Returns
        -------
            dict
        """
        if not category:
            raise AttributeError("category is required")
        for name in names:
            assert type(name) == str, "names can only be strings"
        payload = {"category": category, "names": names}
        return self.API.patch(url="/v1/metrics/configure", json=payload)

    def add(
        self,
        timestamp: str = None,
        category: str = None,
        metrics: dict = {},
        patch: bool = False,
    ):
        """
        Add Metrics

        Parameters
        ----------
        timestamp: str
            Timestamp in UTC, expected to be parsed by dateutil.parser.parse
        category : str
            category the metrics belong to, e.g. deadbeams
        metrics : dict
            Metrics to posted, {metric_name: metric_value} format
        patch : bool
            When True, there will be an attempt patch the timestamp of the
            most recently posted metric, rather than adding new entry
            NOTE: When posting for the first time to a newly configured metric,
            if patch cannot be set to True

        Returns
        -------
            dict
        """
        if not category:
            raise AttributeError("category is required")
        assert type(metrics) == dict, "metrics needs to be dictionary"
        # Construct the payload
        payload = {}
        if timestamp:
            payload["timestamp"] = timestamp
        payload["category"] = category
        payload["metrics"] = metrics
        # Patch or Post the metricss
        if patch:
            return self.API.patch(url="/v1/metrics", json=payload)
        else:
            return self.API.post(url="/v1/metrics", json=payload)

    def get_metrics(self, category: str = None, metric: str = None) -> JSON:
        """
        Get Metrics

        Parameters
        ----------
        category : str
            category the metrics belong to, e.g. deadbeams
        metric : str
            Name of the metric to get, e.g. "1000"

        Returns
        -------
        metrics: list
            metrics are a list of dicts with the following key & values
        """
        if not category:
            raise AttributeError("category is required")
        url = f"/v1/metrics/{category}"
        if metric:
            url = f"{url}/{metric}"
        return self.API.get(url=url)

    def search(
        self,
        category: str = None,
        metrics: [str] = None,
        timestamps: [t.Any, t.Any] = ["min", "max"],
        values: [t.Any, t.Any] = ["min", "max"],
    ) -> JSON:
        """
        Search Metrics

        Parameters
        ----------
        category : str
            category the metrics belong to, e.g. deadbeams
        metric : list
            List of metrics (str) to get, e.g. "1000"
        timestamps : list
            Bounds of time range to search. Valid values are
            "min", "max", dateutil.parser parseable str
            e.g. ["min", "2019-01-3"], ["2019-01-3", "max"]
        values: list
            Bounds of values to search in a lexicographical order
            Valid values are dependent on the metrics being searched
            e.g. [0, 1], ["30.0", "30.123"]

        Returns
        -------
        metrics : list
            List of python dicts conforming to a metric type
        """
        if not category:
            raise AttributeError("category is required")
        if not metrics:
            raise AttributeError("atleast 1 metric name is required")
        payload = {}
        payload["category"] = category
        payload["metrics"] = metrics
        payload["values"] = values
        payload["timestamps"] = timestamps
        return self.API.post(url="/v1/metrics/search", json=payload)
