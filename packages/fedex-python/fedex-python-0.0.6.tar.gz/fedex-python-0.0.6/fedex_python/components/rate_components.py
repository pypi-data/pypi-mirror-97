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
from typing import List, Optional

# Third party libs

# Project libs
from . import common, enums

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class RequestedPackageLineItem(common.RequestedPackageLineItemBase):
    """Add some components."""
    #Doc: Inheritance from parent.
    group_number:Optional[int] = 1
    #Doc: Inheritane from parent.
    group_package_count:Optional[int] = 1

class RequestedShipment(common.RequestedShipmentBase):
    """Override only to change the requested_package_line_items type."""
    #Doc:Identifies the date and time the package is tendered to FedEx.
    ship_timestamp:Optional[str]
    #Doc: Ship Items.
    requested_package_line_items:List[RequestedPackageLineItem]
    #Doc type rate request.
    rate_request_types:enums.RateRequestTypeEnum


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------