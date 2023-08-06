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
from . import base, common, enums

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class LabelSpecification(base.BaseComponent):
    """Details about the imagetype,printer format,and label stock for label."""

    #Doc: to receive the correct label image in the Ship Reply service
    label_format_type:enums.LabelFormatTypeEnum
    #Doc: Specify the image format used for a shipping document.
    image_type:Optional[enums.ImageTypeEnum]
    #Doc: Optional for each label request, however required to print the labels requested.
    label_stock_type:Optional[enums.LabelStockTypeEnum]
    #Doc:  Applicable only to documents produced on thermal printers with roll
    label_printing_orientation:Optional[enums.LabelPrintingOrientationEnum]
    #Doc: Specifies the order in which the labels will be returned.
    label_order:Optional[enums.LabelOrderEnum]

class RequestedShipment(common.RequestedShipmentBase):
    """Details for shipment request."""
    #Doc: Details about the image type, printer format, and label stock for label.
    label_specification:LabelSpecification
    #Doc type rate request.
    rate_request_types:enums.RateRequestTypeEnum
    #Doc: Tracking master
    master_tracking_id:Optional[common.TrackingId]

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------