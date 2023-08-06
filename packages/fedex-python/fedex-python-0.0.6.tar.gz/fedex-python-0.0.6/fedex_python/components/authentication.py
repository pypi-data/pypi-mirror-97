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

class UserCredential(base.BaseComponent):
    """User Credential required in Web authentication."""

    #Doc: Fedex account key.
    key:str
    #Doc: Fedex account password.
    password:str

class WebAuthenticationDetail(base.BaseComponent):
    """Web authentication required by Fedex web services."""

    #Doc: credentials to register.
    user_credential:UserCredential

class Localization(base.BaseComponent, enums.LocalizationEnum):
    """Localitation data."""
    #Doc: Language Code.
    language_code:str
    #Doc: Locale Code.
    locale_code:Optional[str]

    @classmethod
    def get(cls, item) -> "Localization":
        """Get some localization available in FedEx.

        Args:
            item: An item specified in LocalizationEnum.
        Returns:
            An itself class.
        """
        if isinstance(item, tuple):
            return cls(language_code=item[0], locale_code=item[1])
        return cls(language_code=item)

class ClientDetail(base.BaseComponent):
    """Fedex client data requert by Fedex web services."""

    #Doc: Fedex account number.
    account_number:str
    #Doc: Fedex meter number.
    meter_number:str
    #Doc: Location.
    localization:Optional[Localization]

class TransactionDetail(base.BaseComponent):
    """Set the details for transaction."""

    #Doc: Transaction unique identifier.
    customer_transaction_id:str

class Version(base.BaseComponent):
    """Upload de wsdl to that version."""
    #Doc: Set the service id.
    service_id:enums.ServiceTypeEnum
    #Doc: Identifies the service business level.
    major:int
    #Doc: Identifies the service interface level.
    intermediate:int = 0
    #Doc: Identifies the service code level.
    Minor:int = 0

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------