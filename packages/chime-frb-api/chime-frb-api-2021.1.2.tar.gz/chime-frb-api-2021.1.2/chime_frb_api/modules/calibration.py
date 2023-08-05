#!/usr/bin/env python

import typing as t

from chime_frb_api.core import API

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]


class Calibration:
    """
    CHIME/FRB Calibration API
    """

    def __init__(self, API: API):
        self.API = API

    def get_calibration(self, utc_date: str = None, source_name: str = None) -> JSON:
        """
        Fetches all CHIME/FRB calibration data products for a specific utc_date,
        source_name or a combination of both filters. Atleast one is required.

        Parameters
        ----------
        utc_date : str
            UTC date in the format YYYYMMDD, e.g. 20190101
        source_name : str
            Name of the calibration source, e.g. CAS_A

        Returns
        -------
        calibration_data_product : JSON

        Raises
        ------
        AttributeError
        """
        if isinstance(utc_date, type(None)) and isinstance(source_name, type(None)):
            raise AttributeError("either utc_date or source_name is required")
        url = "/v1/calibration"
        # Build the url in the format BASE/SOURCE/DATE
        if isinstance(source_name, str):
            url += f"/{source_name}"
        if isinstance(utc_date, str):
            url += f"/{utc_date}"
        return self.API.get(url)

    def get_calibration_in_timerange(
        self,
        start_utc_date: str = None,
        stop_utc_date: str = None,
        source_name: str = None,
    ) -> JSON:
        """
        Fetches all CHIME/FRB calibration data products for a specific time
        range within start_utc_date and stop_utc_date. You can further, filter
        the results based on source_name.

        Parameters
        ----------
        start_utc_date, stop_utc_date : str
            UTC date in the format YYYYMMDD, e.g. 20190101

        source_name : str
            Name of the calibration source, e.g. CAS_A

        Returns
        -------
        calibration_data_product : JSON

        Raises
        ------
        AttributeError
        """
        if isinstance(start_utc_date, type(None)) or isinstance(
            stop_utc_date, type(None)
        ):
            raise AttributeError("both start_utc_date and stop_utc_date are required")
        url = "/v1/calibration"
        if isinstance(source_name, str):
            url += f"/{source_name}"
        url += f"/{start_utc_date}-{stop_utc_date}"
        return self.API.get(url)

    def get_nearest_calibration(
        self, utc_date: str = None, ra: float = None, dec: float = None
    ) -> JSON:
        """
        Fetches all CHIME/FRB calibration data products for a given
        right ascension, declication and utc_date combination.

        Parameters
        ----------
        ra : float
            Right Ascension
        dec : float
            Declication
        utc_date: str
            UTC date in the format YYYYMMDD, e.g. 20190101

        Returns
        -------
        calibration_data_product : JSON

        Raises
        ------
        AttributeError
        """
        if (
            isinstance(ra, type(None))
            or isinstance(dec, type(None))
            or isinstance(utc_date, type(None))
        ):
            raise AttributeError("ra, dec and utc_date are all required")
        url = f"/v1/calibration/nearest/{utc_date}/{ra}/{dec}"
        return self.API.get(url)

    def get_calibration_product(self, calprod_filepath: str = None) -> JSON:
        """
        Fetches the CHIME/FRB calibration spectrum.

        Parameters
        ----------
        calprod_filepath: str
            The path of the .npz file containing the 16K BF/Jy calibration
            spectrum and calibration diagnostic information on the
            CHIME/FRB Archiver.

        Returns
        -------
        calibration_product : JSON
            {"calibration_spectrum": [],
             "effective_bandwidth": 0,
              "beam_num": 0,
              "fwhm": 0,
              "fwhm_err": 0,
              "fwhm_fit_rsquared": 0}

        Raises
        ------
        AttributeError
        """

        if isinstance(calprod_filepath, type(None)):
            raise AttributeError("calprod_filepath is required")
        payload = {"calprod_filepath": calprod_filepath}
        url = "/v1/calibration/get-calibration"
        return self.API.post(url=url, json=payload)
