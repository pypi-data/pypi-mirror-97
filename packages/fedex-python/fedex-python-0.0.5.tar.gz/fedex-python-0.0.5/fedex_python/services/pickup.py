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
from ..components import common, pickup_components, enums
from ..components.enums import ServiceTypeEnum

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
__all__ = ['PickupService']
# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class PickupService(base.FocusService):
    """Service to ship."""
    #Doc: inheritence attr from BaseService.
    service_type:str = ServiceTypeEnum.PICKUP
    #Doc: inheritence attr from BaseService.
    major:int = 17
    #Doc: inheritence attr from FocusService.
    service_name:str = 'pickup'

    def create_pickup(self, origin_detail:pickup_components.OriginDetail,
                      total_weight:common.Weight, carrier_code:enums.CarrierCodeTypeEnum,
                      package_count:int, country_relationship:enums.CountryRelationshipEnum,
                      custom_id:str):
        """Pickup service.

        Args:
            origin_detail:detal component,
            custom_id: Custom id to Fedex.
            total_weight: Total Weight.
            carrier_code: Code type.
        """
        return self.service('createPickup', {
            'OriginDetail': origin_detail,
            'TotalWeight': total_weight,
            'CarrierCode': carrier_code,
            'CountryRelationship': country_relationship,
            'PackageCount': package_count
        }, custom_id)

    def cancel_pickup(self, scheduled_date:str, pickup_confirmation_number:str,
                      location:str, carrier_code:str, custom_id:str):
        """Cancel pickup service.

        Args:
            scheduled_Date: str date (Y-m-d) that was programming the pickup.
            pickup_confirmation_number: The number given in create pickup.
            location: Fedex Location.
            carrier_code: FedEx carrier.
            custom_id: Custom id to Fedex.
        """
        return self.service('cancelPickup', {
            'ScheduledDate': scheduled_date,
            'PickupConfirmationNumber': pickup_confirmation_number,
            'CarrierCode': carrier_code,
            'Location': location,
        }, custom_id)

    def availability(self, availability_data:pickup_components.Availability, custom_id:str):
        """Cancel pickup service.

        Args:
            availability_data: Data to request.
            custom_id: Custom id to Fedex.
        """
        return self.service('getPickupAvailability', availability_data.dict(), custom_id)

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------