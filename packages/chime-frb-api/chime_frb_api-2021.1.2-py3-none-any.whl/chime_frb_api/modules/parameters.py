#!/usr/bin/env python
import datetime
import logging

from chime_frb_api.core import API

log = logging.getLogger(__name__)


class Parameters:
    """
    CHIME/FRB Parameters API
    """

    def __init__(self, API: API):
        self.API = API

    def get_node_info(self, node_name: str = None):
        """
        Get CHIME/FRB Compute Node Information

        Parameters
        ----------
        node_name : str
            CHIME/FRB Compute Node Name, e.g. cf1n1

        Returns
        -------
        dict
        """
        try:
            assert isinstance(node_name, str), "node_name is required, e.g. cf1n1"
            return self.API.get(f"/v1/parameters/get-node-info/{node_name}")
        except AssertionError as e:
            raise NameError(e)

    def get_beam_info(self, beam_number: int = None):
        """
        Get CHIME/FRB Beam Information

        Parameters
        ----------
        beam_number : int
            CHIME/FRB Beam Number, e.g. 2238

        Returns
        -------
        dict
        """
        try:
            assert isinstance(beam_number, int), "int required"
            assert 0 < beam_number % 1000 < 256, "antenna id range [0,255]"
            assert 0 < beam_number / 1000 < 4, "cylinder id range [0,3]"
            return self.API.get(f"/v1/parameters/get-beam-info/{beam_number}")
        except AssertionError as e:
            raise TypeError(f"invalid beam_number {e}")

    def get_frame0_nano(self, event_date: datetime = None):
        """
        Get the frame0_nano for any given UTC Timestamp

        Parameters
        ----------
            event_date : datetime object
            Datetime object containing the time of the event

        Returns
        -------
            frame0_nano : float
            frame0_nano time for the event datetime

        Raises
        ------
            RuntimeError
        """
        raise NotImplementedError("Currently not implemented")  # pragma: no cover

    def get_datapaths(self, event_number: int = None) -> list:
        """
        Returns top-level folders for each CHIME/FRB event number

        Parameters
        ----------
        event_number : int
            CHIME/FRB Event Number

        Returns
        -------
        list
            List of data paths
        """
        if event_number:  # pragma: no cover
            return self.API.get(url=f"/v1/events/datapaths/{event_number}")
        else:
            raise AttributeError("event_number is required")

    def get_datapath_size(self, datapath: str = None) -> int:
        """
        Returns the size (in bytes) of a folder and its sub-directories

        Parameters
        ----------
        datapath : str
            Absolute path to directory

        Returns
        -------
        integer
            Size of the directory in bytes
        """
        if datapath:  # pragma: no cover
            return self.API.post(
                url="/v1/events/datapath/size", json={"datapath": datapath}
            )
        else:
            raise AttributeError("datapath is required")

    def get_max_size(
        self, datapath: str = None, fileformat: str = None
    ) -> int:  # pragma: no cover
        """
        Returns the maximum size of a file under a datapath

        Parameters
        ----------
        datapath : str
            Absolute path to directory
        fileformat : str
            Format of the file to search

        Returns
        -------
        max_file_size : int
            maximum file size in bytes
        """
        assert datapath and fileformat, "datapath and fileformat required"
        payload = {"datapath": datapath, "fileformat": fileformat}
        return self.API.post(url="/v1/events/datapath/max-size", json=payload)

    def get_filenames(self, event_number: int = None) -> list:  # pragma: no cover
        """
        Get analysed data product filenames for an event

        Parameters
        ----------
        event_number : int
            CHIME/FRB Event Number

        Returns
        -------
        filenames : list
            Returns a list of filenames attached to an event
        """
        return self.API.get(f"/v1/events/filenames/{event_number}")
