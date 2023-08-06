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
from .. import base
from ..components import track_components, enums
from ..components.enums import ServiceTypeEnum

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
__all__ = ['TrackService']

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class TrackService(base.FocusService):
    """Track service."""
    #Doc: inheritence attr from BaseService.
    service_type:str = ServiceTypeEnum.TRACK
    #Doc: inheritence attr from BaseService.
    major:int = 16
    #Doc: inheritence attr from FocusService.
    service_name:str = 'track'

    def track(self, selection_details:track_components.SelectionDetails,
                    processing_options:Optional[enums.ProcessingOptionsEnum], custom_id:str):
        """Track service.

        Args:
            data: Data to make request.
            processing_options: Optional; To show all events.
            custom_id: Custom id to Fedex.
        """
        return self.service('track', {'SelectionDetails':selection_details,
                                      'ProcessingOptions': processing_options}, custom_id)



# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------