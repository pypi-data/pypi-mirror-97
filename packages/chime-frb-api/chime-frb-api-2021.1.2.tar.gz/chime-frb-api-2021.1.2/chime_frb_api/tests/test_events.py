#!/usr/bin/env python

import pytest

from chime_frb_api.backends import frb_master

master = frb_master.FRBMaster(debug=True, base_url="http://localhost:8001")


def test_get_event_full_header():
    event = master.events.get_event(event_number=9386707, full_header=True)
    assert event["event_register"]["event_no"] == 9386707


def test_get_event():
    event = master.events.get_event(9386707)
    assert event["id"] == 9386707


def test_exception_measured_parameters():
    with pytest.raises(NameError):
        master.events.add_measured_parameters()


def test_name_error_meas_params():
    parameters = {
        "dm": 1.0,
        "dm_error": 1.0,
        "galactic_dm": {},
        "expected_spectrum": [],
        "beam_number": 1123,
        "bad_parameter": "asda",
    }
    with pytest.raises(NameError):
        master.events.add_measured_parameters(
            event_number="9386707", measured_parameters=parameters
        )


def test_type_error_meas_param():
    parameters = {
        "pipeline": {
            "name": "test",
            "status": "test",
            "log": "test",
            "version": "test",
        },
        "dm": 1.0,
        "dm_error": 1.0,
        "galactic_dm": {},
        "expected_spectrum": [],
        "beam_number": 1.0,
    }
    with pytest.raises(TypeError):
        master.events.add_measured_parameters(
            event_number="9386707", measured_parameters=parameters
        )


def test_bad_meas_param():
    parameters = {
        "pipeline": {
            "name": "test",
            "status": "test",
            "log": "test",
            "version": "test",
        },
        "dm": 1,
    }
    with pytest.raises(TypeError):
        master.events.add_measured_parameters(
            event_number="5000000", measured_parameters=parameters
        )
    parameters = {
        "pipeline": {
            "name": "test",
            "status": "test",
            "log": "test",
            "version": "test",
        },
        "galactic_dm": [],
    }
    with pytest.raises(TypeError):
        master.events.add_measured_parameters(
            event_number="5000000", measured_parameters=parameters
        )
    parameters = {
        "pipeline": {
            "name": "test",
            "status": "test",
            "log": "test",
            "version": "test",
        },
        "gain": 1,
    }
    with pytest.raises(TypeError):
        master.events.add_measured_parameters(
            event_number="5000000", measured_parameters=parameters
        )


def test_measured_parameters():
    parameters = {
        "pipeline": {
            "name": "test",
            "status": "test",
            "log": "test",
            "version": "test",
        },
        "dm": 1.0,
        "dm_error": 1.0,
        "nchain_end": 100,
        "nchain_start": 10,
        "nwalkers_end": 1000,
        "nwalkers_start": 100,
        "ra_list": [0.0, 12.4],
        "ra_list_error": [0.1, 0.1],
        "dec_list": [-1.2, 49.0],
        "dec_list_error": [0.1, 0.1],
        "x_list": [0.2, 0.3],
        "x_list_error": [0.01, 0.01],
        "y_list": [23.1, 45.3],
        "y_list_error": [0.01, 0.1],
        "max_log_prob": [0.6, 1.0],
        "galactic_dm": {},
        "expected_spectrum": [],
        "beam_number": 1123,
        "is_bandpass_calibrated": True,
        "fitburst_reference_frequency": 600.0,
        "fitburst_reference_frequency_scattering": 600.0,
        "ftest_statistic": 0.5,
        "sub_burst_dm": [1.0],
        "sub_burst_dm_error": [1.0],
        "sub_burst_snr": [10.0],
        "sub_burst_width": [1.0],
        "fixed": {"dm": True, "width": False},
    }
    status = master.events.add_measured_parameters(
        event_number=9386707, measured_parameters=parameters
    )
    assert status["replaced"] == 1


def test_no_event():
    event = master.events.get_event()
    assert event == "event_number is required."
