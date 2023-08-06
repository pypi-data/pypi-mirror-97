#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright 2020 fedex-python
# Author: Sergio Alvarado (sergioal18v@gmail.com)
# =============================================================================

# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
# Core libs
from typing import Any, Callable

# Third party libs

# Project libs
from . import services
from . components.authentication import Localization
from . base import BaseService

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
__all__ = ['Client']

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class Client:
    """Client that manage all Fedex services."""

    def __init__(self, key:str, password:str, account_number:str,
                 meter_number:str, localization:Localization,
                 test_mode:bool = True) -> None:
        """Init the object.

        Args:
            key: Fedex account key.
            password: Fedex account password.
            account_number: Fedex account number.
            meter_number: Fedex meter number.
            localization: The localization object to the query base.
            test_mode: If it point to test server.
        """
        self.key = key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number
        self.localization = localization
        self.test_mode = test_mode
        self.ship = self.init_service(services.ShipService)
        self.rate = self.init_service(services.RateService)
        self.track = self.init_service(services.TrackService)
        self.pickup = self.init_service(services.PickupService)

    def init_service(self, service:BaseService) -> Any:
        """Init the service specified.

        Args:
            service: Service to init.
        Returns:
            An instance of that service.
        """
        return service(self.key, self.password, self.account_number, self.meter_number,
                       localization=self.localization, test_mode=self.test_mode)

    def override_custom_id(self, function:Callable[[BaseService, str], str]) -> None:
        """Override the `set_custom_id` in service specified."""
        self.ship.set_custom_id = function
        self.rate.set_custom_id = function
        self.track.set_custom_id = function



# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------