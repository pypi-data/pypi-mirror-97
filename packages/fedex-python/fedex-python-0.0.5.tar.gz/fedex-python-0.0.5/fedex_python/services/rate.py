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
from ..components import ship_components
from ..components.enums import ServiceTypeEnum

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
__all__ = ['RateService']
# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class RateService(base.FocusService):
    #Doc: inheritence attr from BaseService.
    service_type:str = ServiceTypeEnum.RATE
    #Doc: inheritence attr from BaseService.
    major:int = 28
    #Doc: inheritence attr from FocusService.
    service_name:str = 'rate'

    def get_rates(self, data:ship_components.RequestedShipment, custom_id:str):
        """Rate service.

        Args:
            data: Data to make request.
            custom_id: Custom id to Fedex.
        """
        return self.service('getRates', data, custom_id)



# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------