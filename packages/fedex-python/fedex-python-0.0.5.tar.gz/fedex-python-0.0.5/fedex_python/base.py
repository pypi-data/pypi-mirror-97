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
import enum
from typing import Any, Dict, Optional
import pathlib

# Third party libs
import zeep

# Project libs
from .components import authentication

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class BaseService:
    """Base fedex Service."""

    #Doc: Service Type, only available types are allowed.
    service_type:str = None
    #Doc: version of service.
    major:int = None
    #Doc: function to set the custom id.

    """Base service to make request."""
    def __init__(self, wsdl:str, key:str, password:str,
                 account_number:str, meter_number:str,
                 localization:Optional[authentication.Localization] = None) -> None:
        """Init the object.

        Args:
            wsdl: wsdl file path.
            key: Fedex account key.
            password: Fedex account password.
            account_number: Fedex account number.
            meter_number: Fedex meter number.
            localization: FedEx localzation available in authorization
        """
        self.client = zeep.Client(wsdl)
        self.key = key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number
        self.localization = localization
        self.set_custom_id = (lambda service, value: f'{service.__class__.__name__}_{value}')

        #Doc: Elements to add the request.
        self._elements= {}

    def service(self, service_name:str, data:Any, custom_id:str) -> Dict[str, Any]:
        """Make the service to fedex.

        Args:
            service_name: Service name in wsdl file.
            data: Data to pass to that service.
            custom_id: Custom_id in transaction.
        Returns:
            Fedex response into a dict.
        """
        self._set_default_authorization(custom_id)
        if isinstance(data, dict):
            for key, value in data.items():
                self.add(value, key)
        else:
            self.add(data)
        response = getattr(self.client.service, service_name)(**self._elements)
        self._elements = {}
        return response

    def _set_default_authorization(self, custom_id):
        """Set default authorization required in all Fedex web services.

        Args:
            custom_id: Custom_id in transaction.
        """
        self.add(authentication.WebAuthenticationDetail(
            user_credential=authentication.UserCredential(key=self.key, password=self.password)
        ))
        self.add(authentication.ClientDetail(
            account_number=self.account_number, meter_number=self.meter_number,
            localization=self.localization
        ))
        custom_id = self.set_custom_id(self, custom_id)
        self.add(authentication.TransactionDetail(customer_transaction_id=custom_id))

        self.add(authentication.Version(
            service_id=self.service_type, major=self.major
        ))


    def add(self, element:Any, key:str = None) -> None:
        """Add new element to _elements var.

        Args:
            element: The element to add, It has to be an instance object of Base component, enum
                or any type.
            key: The key element used to append the object, if its null it will take the class
                name.
        """
        if not key:
            key = element.__class__.__name__
        if hasattr(element, 'dict'):
            self._elements[key] = element.dict()
        elif isinstance(element, enum.Enum):
            self._elements[key] = element.value
        else:
            self._elements[key] = element

class FocusService(BaseService):
    """Class to implement the services into One client"""

    #Doc: service name in Fedex web service.
    service_name:str = None

    def __init__(self, *args, test_mode:bool = True, **kwargs):
        """Init the object with specified wsdl file.

        Args:
            test_mode: If there was point to test mode.
        """
        wsdl = f"{pathlib.Path(__file__).parent.absolute()}/wsdl/{'test/' if test_mode else ''}" + \
               f"{self.service_name}_{self.major}.wsdl"
        super().__init__(wsdl, *args, **kwargs)

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------
