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
from . import base
from . import enums

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class PackageIdentifier(base.BaseComponent):
    """Package identifier that is to be used to retrieve the tracking information for a package."""

    #Doc: The type of the Value to be used to retrieve tracking informationfor a package.
    type:enums.PackageIdentifierType
    #Doc: he value to be used to retrieve tracking informationfor a package
    value:str

class SelectionDetails(base.BaseComponent):
    """Specify the details needed to select the shipment being requested to be tracked."""

    #Doc: The FedEx operating company (transportation) used for this package's delivery.
    carrier_code:enums.CarrierCodeTypeEnum
    package_identifier:PackageIdentifier
    shipment_account_number:Optional[str]

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------