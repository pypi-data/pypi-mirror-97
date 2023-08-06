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

# Third party libs

# Project libs
from .. import base
from ..components import ship_components, common, enums
from ..components.enums import ServiceTypeEnum

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
__all__ = ['ShipService']
# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class ShipService(base.FocusService):
    """Service to ship."""
    #Doc: inheritence attr from BaseService.
    service_type:str = ServiceTypeEnum.SHIP
    #Doc: inheritence attr from BaseService.
    major:int = 25
    #Doc: inheritence attr from FocusService.
    service_name:str = 'ship'

    def process_shipment(self, data:ship_components.RequestedShipment, custom_id:str):
        """Shipment service.

        Args:
            data: Data to make request.
            custom_id: Custom id to FedEx.
        """
        return self.service('processShipment', data, custom_id)

    def delete_shipment(self, ship_timestamp:str, tracking_id:common.TrackingId,
                        deletion_control:enums.DeletionControlEnum, custom_id:str):
        """Delete a ship.

        Args:
            ship_timestamp: The ship_timestamp given in the ship.
            tracking_id: A Fedex Tracking Id element(Not only the number).
            deletion_control: The delete action that FedExc will do.
            custom_id: Custom id to FedEx.

        """
        return self.service('deleteShipment', {
            'ShipTimestamp': ship_timestamp,
            'TrackingId': tracking_id,
            'DeletionControl': deletion_control
        }, custom_id)

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------