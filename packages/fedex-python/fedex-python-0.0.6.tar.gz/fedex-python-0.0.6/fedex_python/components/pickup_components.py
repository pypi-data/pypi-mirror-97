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
from typing import Optional

# Third party libs

# Project libs
from . import base, enums,common

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class OriginDetail(base.BaseComponent):
    """Origin detail."""
    #Doc: Provides a location description where the courier/driver will pick up the package.
    package_location:Optional[enums.PackageLocationEnum]
    #Doc: Describes the package location building type for the pickup
    building_part:Optional[enums.BuildingPartCodeEnum]
    #Doc: Accompanies the BuildingPartCode to describe the package pickup location.
    building_part_description:Optional[str]
    #Doc: Identifies the date and time the package will be ready for pickup by FedEx.
    ready_timestamp:str
    #Doc: Identifies the latest time at which the driver can gain access to pick up the package(s).
    company_close_time:str
    #Doc: Contact and address for pickup.
    pickup_location:Optional[common.ContactAddress]

class ShipmentAttributes(base.BaseComponent):
    """Shipment attributes."""
    #Doc: Identifies the FedEx service to use in shipping the package.
    service_type:enums.ShipServiceTypeEnum
    #Doc: Identifies the FedEx service to use in shipping the package.
    packaging_type:enums.PackagingTypeEnum
    #Doc: Weight item.
    weight:Optional[common.Weight]
    #Doc: Dimension item.
    dimensions:Optional[common.Dimensions]


class Availability(base.BaseComponent):
    """To encapsulate data in availability request."""

    #Doc: Address for pickup.
    pickup_address:common.Address
    #Doc: Describes the relationship between the date on which a dispatch occurs
    pickup_request_type:enums.PickupRequestTypeEnum
    #Doc: Identifies the dispatch date (in the local time zone) for the pickup is being requested.
    dispatch_date:str
    #Doc: Identifies the number of business days to consider when checking availability.
    number_of_business_days:int
    #Doc: Identifies the date and time the package will be ready for pickup by FedEx.
    package_ready_time:str
    #Doc: Identifies the latest time at which the driver can gain access to pick up the package(s).
    customer_close_time:str
    #Doc:Identifies the FedEx carrier(s) for which availability is requested.
    carriers:enums.CarrierCodeTypeEnum
    #Doc: Includes descriptive information about the shipment.
    shipment_attributes:ShipmentAttributes

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------