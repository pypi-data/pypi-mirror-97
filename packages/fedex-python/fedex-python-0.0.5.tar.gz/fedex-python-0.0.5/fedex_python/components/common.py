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
import decimal
from typing import List, Optional, Union

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

class Contact(base.BaseComponent):
    """Fedex Contact."""
    #Doc: Client provided identifier corresponding to this contact information.
    contact_id:Optional[str]
    #Doc: Identifies the contact person's name.
    person_name:str
    #Doc: Identifies the contact person's title.
    title:Optional[str]
    #Doc: Identifies the company this contact is associated with.
    company_name:Optional[str]
    #Doc: Identifies the phone number associated with this contact.
    phone_number:str
    #Doc: Identifies the phone extension associated with this contact.
    phone_extension:Optional[str]
    #Doc: Identifies a toll free number, if any, associated with this contact.
    toll_free_phone_number:Optional[str]
    #Doc: Identifies the pager number associated with this contact.
    pager_number:Optional[str]
    #Doc: Identifies the fax number associated with this contact.
    fax_number:Optional[str]
    #Doc: Identifies the email address associated with this contact.
    eMail_address:str

class Address(base.BaseComponent):
    """Fedex Address."""

    #Doc: Combination of number, street name, etc. At least one line is required. Until 2 lines.
    street_lines:Union[Optional[str], Optional[List[str]]]
    #Doc: Name of city, town, etc.
    city:Optional[str]
    #Doc: Identifying abbreviation for US state, Canada province, etc.
    state_or_province_code:Optional[str]
    #Doc: Identification of a region (usually small) for mail/package delivery.
    postal_code:str
    #Doc: Relevant only to addresses in Puerto Rico.
    urbanization_code:Optional[str]
    #Doc: The two-letter code used to identify a country.
    country_code:str
    #Doc: The fully spelt out name of a country.
    country_name:Optional[str]
    #Doc: Indicates whether this address residential (as opposed to commercial).
    residential:Optional[str]
    #Doc: The geographic coordinates cooresponding to this address.
    geographic_coordinates:Optional[str]


class ContactAddress(base.BaseComponent):
    """Party data."""
    #Doc: Fedex account number.
    account_number:Optional[str]
    #Doc: Contact.
    contact:Optional[Contact]
    #Doc: Address.
    address:Optional[Address]

class Weight(base.BaseComponent):
    """Weight component."""

    #Doc: weight unit.
    units:enums.WeightUnits
    #Doc: Decimal Value.
    value:decimal.Decimal

class Dimensions(base.BaseComponent):
    """Dimenssions for a package."""

    #Doc: Package Length.
    length:int
    #Doc: Package height.
    height:int
    #Doc: Package width.
    width:int
    #Doc Linear unit.
    units:enums.LinearUnits

class Payor(base.BaseComponent):
    """Payor for ship."""
    #Doc: Data for responsible party.
    responsible_party:ContactAddress

class ShippingChargesPayment(base.BaseComponent):
    """Shipping charges payment."""
    #Doc:Who make the payment.
    payment_type:enums.PaymentTypeEnum
    #Doc: Payor data.
    payor:Payor

class CustomerReference(base.BaseComponent):
    """Customer references."""
    #Doc: Customer Reference Type.
    customer_reference_type:enums.CustomerReferenceType
    #Doc: Customer reference Value.
    value:str


class RequestedPackageLineItemBase(base.BaseComponent):
    """Items in the rate."""
    #Doc: Used only with INDIVIDUAL_PACKAGE, as a unique identifier of each requested package.
    sequence:Optional[int]
    #Doc: Weight item.
    weight:Weight
    #Doc: Dimension item.
    dimensions:Dimensions
    #Doc: Customer references.
    customer_references:Optional[CustomerReference]
    #Doc: Sequence bumber
    sequence_number:Optional[int]


class RequestedShipmentBase(base.BaseComponent):
    """Base of request for shipment."""

    #Doc:Identifies the date and time the package is tendered to FedEx.
    ship_timestamp:str
    #Doc: Identifies the method by which the package is to be tendered to FedEx
    dropoff_type:Optional[enums.DropoffTypeEnum]
    #Doc: Identifies the FedEx service to use in shipping the package
    packaging_type:Optional[enums.PackagingTypeEnum]
    #Doc: Identifies the FedEx service to use in shipping the package.
    service_type:Optional[enums.ShipServiceTypeEnum]
    #Doc: Descriptive data identifying the party responsible for shipping the package.
    shipper:ContactAddress
    #Doc: Descriptive data identifying the party receiving the package.
    recipient:ContactAddress
    #Doc: Identifies the total weight of the shipment being conveyed to FedEx. Only International.
    total_weight:Optional[Weight]
    #Doc: Total number of packages in the shipment.
    package_count:int = 1
    #Doc: Charges por shipping.
    shipping_charges_payment:ShippingChargesPayment
    #Doc: Ship Items.
    requested_package_line_items:List[RequestedPackageLineItemBase]
    #Doc: Preferred currency.
    preferred_currency:Optional[enums.CurrencyCodeEnum]

class TrackingId(base.BaseComponent):
    """Tracking id type."""
    #Doc: Describes the type of tracking ID.
    tracking_id_type:enums.TrackingIdTypeEnum
    #Doc: Describes in detail the type of airbill and shipment moving through the FedEx system.
    form_id:Optional[str]
    #Doc: For use with SmartPost tracking IDs only.
    usps_application_id:Optional[str]
    #Doc: Tracking number
    tracking_number:str


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------