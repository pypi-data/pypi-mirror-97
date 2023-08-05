#!/usr/bin/env python

import json
import typing as t

from chime_frb_api.core import API

JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]


class Bucket(API):
    """
    CHIME/FRB Backend Bucket API

    Attributes
    ----------
    base_url : str
        Base URL at which the bucket is accessible.
    """

    def __init__(
        self,
        debug: bool = False,
        base_url: str = "http://frb-vsop.chime:4357/buckets",
        authentication: bool = False,
    ):
        API.__init__(
            self,
            debug=debug,
            default_base_urls=["http://frb-vsop.chime:4357/buckets"],
            base_url=base_url,
            authentication=authentication,
        )

    def create_bucket(self, bucket_name: str) -> JSON:
        """
        Create a bucket on the CHIME/FRB Backend

        Parameters
        ----------
        bucket_name : str
            Name of the bucket
        """
        payload = {"name": bucket_name}
        return self.post(url="", json=payload)

    def delete_bucket(self, bucket_name: str) -> JSON:
        """
        Delete a bucket on the CHIME/FRB Backend

        Parameters
        ----------
        bucket_name : str
            Name of the bucket
        """
        return self.delete(url=f"/{bucket_name}")

    def deposit(self, bucket_name: str, work: JSON, priority: str) -> JSON:
        """
        Deposit work into a bucket

        Parameters
        ----------
        bucket_name : str
            Name of the bucket

        work : JSON Encodeable
            List of json encodeable values, if the work

        priority : str
            Priority of the work. Choices are high, medium, low.

        Returns
        -------
            list
        """
        try:
            work = json.dumps(work)
        except Exception as err:
            raise (err)
        payload = {"work": [work], "priority": priority}
        return self.post(url=f"/work/{bucket_name}", json=payload)

    def withdraw(self, bucket_name: str, client: str, expiry: int) -> JSON:
        """
        Get work from a bucket

        Parameters
        ----------
        bucket_name : str
            Name of the bucket

        client : str
            Name of the client asking for work.

        expiry : int
            Duration in seconds after which the work is re-deposited.
            The client should finish the work and conclude it before expiry.
        """
        payload = {"client": client, "expiry": expiry}
        return json.loads(self.get(url=f"/work/{bucket_name}", json=payload))

    def conclude(
        self, bucket_name: str, work_name: str, redeposit: bool = False
    ) -> JSON:
        """
        Conclude work managed by a bucket

        Parameters
        ----------
        bucket_name : str
            Name of the bucket

        work_name
            Work processed

        priority : str
            Priority of the work. Choices are high, medium, low.

        client : str
            Name of the client that withdrew the work.
        """
        payload = {"work": work_name, "redeposit": redeposit}
        return self.post(url=f"/conclude-work/{bucket_name}", json=payload)

    def change_priority(self, bucket_name: str, work_name: str, priority: str) -> JSON:
        """
        Change the priority of work in a bucket

        Parameters
        ----------
        bucket : str
            Name of the bucket

        work_name
            Work processed

        redeposit: bool
            bool: whether to redeposit work in the bucket.
        """
        payload = {"work": work_name, "priority": priority}
        return self.post(url=f"/change-priority/{bucket_name}", json=payload)

    def get_status(self, bucket_name: str = None) -> JSON:
        """
        Get status of CHIME/FRB Bucket

        Parameters
        ----------
        bucket_name : str, optional
            Name of the bucket

        Returns
        -------
        json
        """
        if bucket_name is None:
            response = self.get("")
        else:
            response = self.get(url=f"/{bucket_name}")
        return response
