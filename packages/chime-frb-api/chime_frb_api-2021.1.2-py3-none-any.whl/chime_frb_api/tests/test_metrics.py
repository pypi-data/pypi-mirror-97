#!/usr/bin/env python

from datetime import datetime
from time import sleep

import pytest
import requests

from chime_frb_api.backends import frb_master

master = frb_master.FRBMaster(debug=True, base_url="http://localhost:8001")


def test_configure():
    response = master.metrics.configure(
        description="test", category="test", names=["test_a", "test_b"]
    )
    assert response == {
        "category_registered": True,
        "table_created": True,
        "indices_created": True,
    }


def test_bad_configure():
    with pytest.raises(AttributeError):
        master.metrics.configure(description="bad-test", names=["test_a", "test_b"])


def test_reconfigure():
    response = master.metrics.reconfigure(category="test", names=["test_c", "test_d"])
    assert response == {
        "deleted": 0,
        "errors": 0,
        "inserted": 0,
        "replaced": 1,
        "skipped": 0,
        "unchanged": 0,
    }


def test_bad_reconfigure():
    with pytest.raises(AttributeError):
        master.metrics.reconfigure(names=["test_a", "test_b"])


def test_overview():
    response = master.metrics.overview()
    assert "test_c" in response[0]["names"]
    assert "test_d" in response[0]["names"]


def test_add_new_metric():
    response = master.metrics.add(
        category="test", metrics={"test_a": 1, "test_b": 2}, patch=False
    )
    assert response == {
        "deleted": 0,
        "errors": 0,
        "inserted": 2,
        "replaced": 0,
        "skipped": 0,
        "unchanged": 0,
    }


def test_bad_add():
    with pytest.raises(AttributeError):
        master.metrics.add(metrics={"test_a": 1, "test_b": 2}, patch=False)


def test_patch_add():
    response = master.metrics.add(
        category="test", metrics={"test_a": 1, "test_b": 2}, patch=True
    )
    assert response == {
        "deleted": 0,
        "errors": 0,
        "inserted": 0,
        "replaced": 2,
        "skipped": 0,
        "unchanged": 0,
    }


def test_timestamp_add():
    response = master.metrics.add(
        category="test",
        metrics={"test_a": 5, "test_b": 5},
        timestamp=datetime.utcnow().isoformat(),
    )
    assert response == {
        "deleted": 0,
        "errors": 0,
        "inserted": 2,
        "replaced": 0,
        "skipped": 0,
        "unchanged": 0,
    }


def test_get_metrics():
    sleep(0.5)
    response = master.metrics.get_metrics(category="test", metric="test_a")
    assert len(response) == 2


def test_bad_get_metrics():
    with pytest.raises(AttributeError):
        master.metrics.get_metrics(metric="test_a")


def test_metric_search():
    # Sleep 1 second to allow the database to index
    sleep(1)
    response = master.metrics.search(
        category="test",
        metrics=["test_a", "test_b"],
        timestamps=["min", "max"],
        values=[2, 2],
    )
    assert response[0]["metric"] == "test_b"
    assert response[0]["value"] == 2


def test_bad_metric_search():
    with pytest.raises(AttributeError):
        master.metrics.search(metrics=["test_a", "test_b"])
    with pytest.raises(AttributeError):
        master.metrics.search(category="test")


def test_delete_category():
    response = requests.delete(url="http://localhost:8001/v1/metrics/destroy/test")
    assert response.status_code == 200
    assert response.json() == {
        "deleted": 1,
        "errors": 0,
        "inserted": 0,
        "replaced": 0,
        "skipped": 0,
        "unchanged": 0,
    }
