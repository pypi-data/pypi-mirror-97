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
from typing import Any, Dict

# Third party libs
import pydantic

# Project libs

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

__all__ = ['BaseComponent']

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class BaseComponent(getattr(pydantic, 'BaseModel')):
    """Components in wsdl tansform to python classes."""

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        """Transfrom snake_case_name, to CamelCaseName that are required in Fedex web services.

        By convention, python variables should be in snake_case `variable_name`, but fedex web
        services required in CamelCase `VariableName` in all services. This transfrom the variable
        name to that.

        Also, make a deep iterate to convert to dict all subcomponents of each component.
        """
        data = super().dict(*args, **kwargs)
        dict_mapped = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, enum.Enum):
                    value = value.value
                key = ''.join("%s%s" % (word[0].upper(), word[1:]) for word in key.split('_'))
                if hasattr(value, 'dict'):
                    value = value.dict()
                dict_mapped[key] = value
        return dict_mapped

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------