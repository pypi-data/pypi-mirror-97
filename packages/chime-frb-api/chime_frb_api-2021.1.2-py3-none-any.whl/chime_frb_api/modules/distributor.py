#!/usr/bin/env python

import json
import typing as t

from chime_frb_api.core import API

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]


class Distributor(API):
    """
    CHIME/FRB Backend Distributor API

    Attributes
    ----------
    base_url : str
        Base URL at which the distributor is accessible.
    """

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://frb-vsop.chime:8002",
        authentication: bool = False,
    ):
        API.__init__(
            self,
            debug=debug,
            default_base_urls=["http://frb-vsop.chime:8002"],
            base_url=base_url,
            authentication=authentication,
        )

    def create_distributor(self, distributor_name: str, cleanup: bool = False) -> JSON:
        """
        Create a distributor on the CHIME/FRB Backend

        Parameters
        ----------
        distributor_name : str
            Name of the distributor
        cleanup : boolean, optional
            Removes the work from status queue once it is successfully concluded.
            (Default is False)
        """
        payload = {"distributor": distributor_name, "cleanup": cleanup}
        return self.post(url="/distributor/", json=payload)

    def stop_distributor(self, distributor_name: str) -> JSON:
        """
        Stops the distributor from accumulating new work,
        whether it is scanning a directory or accpeting work at an endpoint,
        however it continues to distribute work

        Parameters
        ----------
        distributor_name : str
            Name of the distributor
        """
        return self.get(f"/distributor/stop/{distributor_name}")

    def delete_distributor(self, distributor_name: str) -> JSON:
        """
        Delete a distributor on the CHIME/FRB Backend

        Parameters
        ----------
        distributor_name : str
            Name of the distributor
        """
        return self.delete(url=f"/distributor/{distributor_name}")

    def create_directory_scanning_distributor(
        self,
        distributor_name: str,
        directory: str,
        interval: int = 1,
        retries: int = 120,
        cleanup: bool = False,
    ) -> JSON:
        payload = {
            "distributor": distributor_name,
            "directory": directory,
            "interval": interval,
            "retries": retries,
            "cleanup": cleanup,
        }
        """
        Create a Distributor to scan a directory.

        Parameters
        ----------
        distributor : str
            Name of the distributor

        directory : str
            Absolute path to the glob files on, e.g. /frb-archiver/2018/02/01/*.h5

        interval : int, optional
            Scanning interval of the folder in seconds (default is 1)

        retries : int, optional
            Number of retries before the distributor stops (default is 120)

        cleanup : boolean, optional
            Delete work if successfully completed (default is False)
        """
        return self.post(url="/distributor/directory-scanner", json=payload)

    def deposit_work(self, distributor_name: str, work: JSON) -> JSON:
        """
        Deposit work into a distributor

        Parameters
        ----------
        distributor : str
            Name of the distributor

        work : JSON Encodeable
            List of json encodeable values, if the work

        Returns
        -------
            list
        """
        try:
            json.loads(work)
        except TypeError:
            work = json.dumps(work)
        except Exception as err:
            raise (err)

        payload = {"work": [work]}
        return self.post(url=f"/distributor/work/{distributor_name}", json=payload)

    def get_work(self, distributor_name: str) -> JSON:
        """
        Get work from a distributor

        Parameters
        ----------
        distributor : str
            Name of the distributor
        """
        return self.get(url=f"/distributor/work/{distributor_name}")

    def conclude_work(
        self, distributor_name: str, work_name: str, work_status: bool
    ) -> JSON:
        """
        Conclude work managed by a distributor

        Parameters
        ----------
        distributor : str
            Name of the distributor

        work_name
            Work processed

        work_status: bool
            bool defining pass/fail status of work
        """
        payload = {"work": work_name, "status": work_status}
        return self.post(
            url=f"/distributor/conclude-work/{distributor_name}", json=payload
        )

    def get_status(self, distributor_name: str = None) -> JSON:
        """
        Get status of CHIME/FRB Distributor Backend

        Parameters
        ----------
        distributor_name : str, optional
            Name of the distributor

        Returns
        -------
        json
        """
        if distributor_name is None:
            response = self.get("/distributor/status")
        else:
            response = self.get(url=f"/distributor/status/{distributor_name}")
        return response
