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
from enum import Enum

# Third party libs

# Project libs

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class ServiceTypeEnum(str, Enum):
    """Fedex service types."""

    #Doc: Service to validate or complete recipient addresses.
    ADDRESS_VALIDATION = 'aval'
    #Doc: To store in the asynchronous service for later retrieval).
    ASYNC = 'async'
    #Doc: Service to reconcile shipping information for yourGround or FedEx SmartPost® shipments.
    CLOSE = 'close'
    #Doc: Enables customers to validate postal codes and service commitments
    COUNTRY = 'country'
    #Doc: optional program that gives dangerous goods (DG) and hazardous materials.
    DGDS = 'dgds'
    #Doc: International shipping to submit your trade documentation electronically.
    ETD = 'cdus'
    #Doc: International delivery of shipments weighing more than 150 lbs.
    IN_FLIGHT_SHIPMENT ='ifss'
    #Doc: Search the addresses of the nearest FedEx packagedrop-off locations.
    LOCATIONS = 'locs'
    #Doc: Service to create information for a shipment as it is received throughout the day.
    OPEN_SHIP = 'ship'
    #Doc: Service to schedule a courier a shipment, cancel request, or check for availability.
    PICKUP = 'disp'
    #Doc: Service to determine estimated or courtesy billing quotes.
    RATE = 'crs'
    #Doc: Service to process and submit various shipping requests.
    SHIP = 'ship'
    #Doc: Service to obtain real-time tracking information.
    TRACK ='trck'
    #Doc: Service to check service availability, route and postal codes.
    VALIDATION_AVAILABILITY_AND_COMMITMENT = 'vacs'

class DropoffTypeEnum(str, Enum):
    """Fedex dropp off type."""

    #Doc: Drop off the package at an authorized FedEx business service center.
    BUSINESS_SERVICE_CENTER = 'BUSINESS_SERVICE_CENTER'
    #Doc: Drop the package in a FedEx drop box.
    DROP_BOX = 'DROP_BOX'
    #Doc:Every-day pickup scheduled with a courier.
    REGULAR_PICKUP ='REGULAR_PICKUP'
    #Doc: call FedEx to ask for a courier.
    REQUEST_COURIER = 'REQUEST_COURIER'
    #Doc:Drop off the package at a FedEx Station.
    STATION = 'STATION'

class ShipServiceTypeEnum(str, Enum):
    """Fexed ship service types."""

    #Doc: For intra-Europe shipment only.
    EUROPE_FIRST_INTERNATIONAL_PRIORITY = 'EUROPE_FIRST_INTERNATIONAL_PRIORITY'
    #Doc: 1 business days within the U.S. for packages over 150 pounds each.
    FEDEX_1_DAY_FREIGHT = 'FEDEX_1_DAY_FREIGHT'
    #Doc: 2 business days.
    FEDEX_2_DAY = 'FEDEX_2_DAY'
    #Doc: Second-business day by 10:30 a.m. to most business areas; for certain
    FEDEX_2_DAY_AM = 'FEDEX_2_DAY_AM'
    #Doc: 2 business days within the U.S. for packages over 150 pounds each.
    FEDEX_2_DAY_FREIGHT = 'FEDEX_2_DAY_FREIGHT'
    #Doc: 1 business days within the U.S. for packages over 150 pounds each.
    FEDEX_3_DAY_FREIGHT = 'FEDEX_3_DAY_FREIGHT'
    #Doc: Not doc.
    FEDEX_DISTANCE_DEFERRED = 'FEDEX_DISTANCE_DEFERRED'
    #Doc: Delivery to companies at 4:30 p.m. and 7 p.m. to residencies in 3 business days.
    FEDEX_EXPRESS_SAVER = 'FEDEX_EXPRESS_SAVER'
    #Doc First business days within the U.S. for packages over 150 pounds each.
    FEDEX_FIRST_FREIGHT = 'FEDEX_FIRST_FREIGHT'
    #Doc: Economical delivery within the U.S., for packages over 150 pounds each.
    FEDEX_FREIGHT_ECONOMY = 'FEDEX_FREIGHT_ECONOMY'
    #Doc: Deliver shipments quickly and reliably within the U.S., for packages over 150 pounds each.
    FEDEX_FREIGHT_PRIORITY = 'FEDEX_FREIGHT_PRIORITY'
    #Doc: Economical ground delivery to businesses.
    FEDEX_GROUND = 'FEDEX_GROUND'
    #Doc: Not doc.
    FEDEX_NEXT_DAY_AFTERNOON = 'FEDEX_NEXT_DAY_AFTERNOON'
    #Doc: Not doc.
    FEDEX_NEXT_DAY_EARLY_MORNING = 'FEDEX_NEXT_DAY_EARLY_MORNING'
    #Doc: Not doc.
    FEDEX_NEXT_DAY_END_OF_DAY = 'FEDEX_NEXT_DAY_END_OF_DAY'
    #Doc: Not doc.
    FEDEX_NEXT_DAY_FREIGHT = 'FEDEX_NEXT_DAY_FREIGHT'
    #Doc: Not doc.
    FEDEX_NEXT_DAY_MID_MORNING = 'FEDEX_NEXT_DAY_MID_MORNING'
    #Doc: First thing the next-business-day morning.
    FIRST_OVERNIGHT = 'FIRST_OVERNIGHT'
    #Doc: Economical ground delivery to residences.
    GROUND_HOME_DELIVERY = 'GROUND_HOME_DELIVERY'
    #Doc: Not doc.
    INTERNATIONAL_ECONOMY = 'INTERNATIONAL_ECONOMY'
    #Doc: Not doc.
    INTERNATIONAL_ECONOMY_FREIGHT = 'INTERNATIONAL_ECONOMY_FREIGHT'
    #Doc: Not doc.
    INTERNATIONAL_FIRST = 'INTERNATIONAL_FIRST'
    #Doc: Not doc.
    INTERNATIONAL_PRIORITY = 'INTERNATIONAL_PRIORITY'
    #Doc: Not doc.
    INTERNATIONAL_PRIORITY_EXPRESS = 'INTERNATIONAL_PRIORITY_EXPRESS'
    #Doc: Not doc.
    INTERNATIONAL_PRIORITY_FREIGHT = 'INTERNATIONAL_PRIORITY_FREIGHT'
    #Doc: Next-business-day morning.
    PRIORITY_OVERNIGHT = 'PRIORITY_OVERNIGHT'
    #Cross-country door-to-door delivery within hours, within the U.S.
    SAME_DAY = 'SAME_DAY'
    #Doc:Direct delivery with no additional service-related stops, within the U.S.
    SAME_DAY_CITY = 'SAME_DAY_CITY'
    #Doc: Provide line haul and deliver your packages to a USPS facility for final delivery.
    SMART_POST = 'SMART_POST'
    #Doc: Next-business-day afternoon.
    STANDARD_OVERNIGHT = 'STANDARD_OVERNIGHT'

class PackagingTypeEnum(str, Enum):
    """Fedex packaging types."""

    FEDEX_10KG_BOX = 'FEDEX_10KG_BOX'
    FEDEX_25KG_BOX = 'FEDEX_25KG_BOX'
    FEDEX_BOX = 'FEDEX_BOX'
    FEDEX_ENVELOPE = 'FEDEX_ENVELOPE'
    FEDEX_EXTRA_LARGE_BOX = 'FEDEX_EXTRA_LARGE_BOX'
    FEDEX_LARGE_BOX = 'FEDEX_LARGE_BOX'
    FEDEX_MEDIUM_BOX = 'FEDEX_MEDIUM_BOX'
    FEDEX_PAK = 'FEDEX_PAK'
    FEDEX_SMALL_BOX = 'FEDEX_SMALL_BOX'
    FEDEX_TUBE = 'FEDEX_TUBE'
    YOUR_PACKAGING = 'YOUR_PACKAGING'

class LabelFormatTypeEnum(str, Enum):
    """Label types."""
    #Doc: Label format type to receive a label.
    COMMON2D = 'COMMON2D'
    #Doc: this value is used to receive the barcode data if you create a custom label.
    LABEL_DATA_ONLY = 'LABEL_DATA_ONLY'

class ImageTypeEnum(str, Enum):
    """Image types."""

    DOC = 'DOC'
    EPL2 = 'EPL2'
    PDF = 'PDF'
    PNG = 'PNG'
    RTF = 'RTF'
    TEXT = 'TEXT'
    ZPLII = 'ZPLII'

class LabelStockTypeEnum(str, Enum):
    """Label stock types."""

    #Doc: These values display a thermal format label.
    PAPER_4X6 = 'PAPER_4X6'
    PAPER_4X8 = 'PAPER_4X8'
    PAPER_4X9 = 'PAPER_4X9'
    #Doc: These values display a plain paper format shipping label.
    PAPER_7X4_75 = 'PAPER_7X4.75'
    PAPER_8_5X11_BOTTOM_HALF_LABEL = 'PAPER_8.5X11_BOTTOM_HALF_LABEL'
    PAPER_8_5X11_TOP_HALF_LABEL = 'PAPER_8.5X11_TOP_HALF_LABEL'
    PAPER_LETTER = "PAPER_LETTER"
    STOCK_4X6 = "STOCK_4X6"
    STOCK_4X675 = "STOCK_4X6.75"
    STOCK_4X675_LEADING_DOC_TAB = "STOCK_4X6.75_LEADING_DOC_TAB"
    STOCK_4X675_TRAILING_DOC_TAB = "STOCK_4X6.75_TRAILING_DOC_TAB"
    STOCK_4X8 = "STOCK_4X8"
    STOCK_4X9 = "STOCK_4X9"
    STOCK_4X9_LEADING_DOC_TAB = "STOCK_4X9_LEADING_DOC_TAB"
    STOCK_4X9_TRAILING_DOC_TAB = "STOCK_4X9_TRAILING_DOC_TAB"

class LabelPrintingOrientationEnum(str, Enum):
    """Label printing orientation enum."""
    BOTTOM_EDGE_OF_TEXT_FIRST = 'BOTTOM_EDGE_OF_TEXT_FIRST'
    TOP_EDGE_OF_TEXT_FIRST = 'TOP_EDGE_OF_TEXT_FIRST'

class LabelOrderEnum(str, Enum):
    """Label order."""
    SHIPPING_LABEL_FIRST = 'SHIPPING_LABEL_FIRST'
    SHIPPING_LABEL_LAST = 'SHIPPING_LABEL_FIRST'

class WeightUnits(str, Enum):
    """Weights allowed in weigths."""
    LB = 'LB'
    KG = 'KG'

class LinearUnits(str, Enum):
    """ Linear units."""
    CM = 'CM'
    IN = 'IN'

class PaymentTypeEnum(str, Enum):
    """Payment types."""

    ACCOUNT='ACCOUNT'
    COLLECT='COLLECT'
    RECIPIENT='RECIPIENT'
    SENDER='SENDER'
    THIRD_PARTY='THIRD_PARTY'

class CarrierCodeTypeEnum(str, Enum):
    """dentification of a FedEx operating company (transportation)."""

    FEDEX_CARGO = 'FDXC'
    FEDEX_EXPRESS = 'FDXE'
    FEDEX_GROUND = 'FDXG'
    FEDEX_CUSTOM_CRITICAL = 'FXCC'
    FEDEX_FREIGHT = 'FXFR'
    FEDEX_SMARTPOST = 'FXSP'

class PackageIdentifierType(str, Enum):
    """The type of track to be performed."""
    BILL_OF_LADING = 'BILL_OF_LADING'
    COD_RETURN_TRACKING_NUMBER = 'COD_RETURN_TRACKING_NUMBER'
    CUSTOMER_AUTHORIZATION_NUMBER = 'CUSTOMER_AUTHORIZATION_NUMBER'
    CUSTOMER_REFERENCE = 'CUSTOMER_REFERENCE'
    DEPARTMENT = 'DEPARTMENT'
    DOCUMENT_AIRWAY_BILL = 'DOCUMENT_AIRWAY_BILL'
    FREE_FORM_REFERENCE = 'FREE_FORM_REFERENCE'
    GROUND_INTERNATIONAL = 'GROUND_INTERNATIONAL'
    GROUND_SHIPMENT_ID = 'GROUND_SHIPMENT_ID'
    GROUP_MPS = 'GROUP_MPS'
    INVOICE = 'INVOICE'
    JOB_GLOBAL_TRACKING_NUMBER = 'JOB_GLOBAL_TRACKING_NUMBER'
    ORDER_GLOBAL_TRACKING_NUMBER = 'ORDER_GLOBAL_TRACKING_NUMBER'
    ORDER_TO_PAY_NUMBER = 'ORDER_TO_PAY_NUMBER'
    OUTBOUND_LINK_TO_RETURN = 'OUTBOUND_LINK_TO_RETURN'
    PARTNER_CARRIER_NUMBER = 'PARTNER_CARRIER_NUMBER'
    PART_NUMBER = 'PART_NUMBER'
    PURCHASE_ORDER = 'PURCHASE_ORDER'
    RETURN_MATERIALS_AUTHORIZATION = 'RETURN_MATERIALS_AUTHORIZATION'
    RETURNED_TO_SHIPPER_TRACKING_NUMBER = 'RETURNED_TO_SHIPPER_TRACKING_NUMBER'
    TRACKING_CONTROL_NUMBER = 'TRACKING_CONTROL_NUMBER'
    TRACKING_NUMBER_OR_DOORTAG = 'TRACKING_NUMBER_OR_DOORTAG'
    TRANSPORTATION_CONTROL_NUMBER = 'TRANSPORTATION_CONTROL_NUMBER'
    SHIPPER_REFERENCE = 'SHIPPER_REFERENCE'
    STANDARD_MPS = 'STANDARD_MPS'

class RateRequestTypeEnum(str, Enum):
    """"hat kind of rates the customer wishes to have quoted on this shipment."""

    LIST = 'LIST'
    NONE = 'NONE'
    PREFERRED = 'PREFERRED'

class CurrencyCodeEnum(str, Enum):
    ANTILLES_GUILDER = 'ANG'
    ARGENTINIAN_PESO = 'ARN'
    AUSTRALIAN_DOLLAR = 'AUD'
    ARUBAN_FLORIJN = 'AWG'
    BARBADOS_DOLLAR = 'BBD'
    BAHRAINI_DINAR = 'BHD'
    BERMUDA_DOLLAR = 'BMD'
    BRUNEI_DOLLAR = 'BND'
    BRAZILIAN_REAL = 'BRL'
    BAHAMIAN_DOLLARS = 'BSD'
    BULGARIAN_LEV = 'BGN'
    CANADIAN_DOLLAR = 'CAD'
    CAYMAN_DOLLARS = 'CID'
    CHILEAN_PESO = 'CHP'
    CHINESE_RENMINBI = 'CNY'
    COLOMBIAN_PESO = 'COP'
    COSTA_RICAN_COLON = 'CRC'
    CROATIAN_KUNA = 'HRK'
    CZECH_REPUBLIC_KORUNY = 'CZK'
    DANISH_KRONE = 'DKK'
    DOMINICAN_PESO = 'RDD'
    CARIBBEAN_DOLLAR = 'ECD'
    EGYPTIAN_POUND = 'EGP'
    EURO = 'EUR'
    GUATEMALAN_QUETZAL = 'GTQ'
    BRITISH_POUND_STERLING = 'GBP'
    HONG_KONG_DOLLAR = 'HKD'
    HUNGARIAN_FORINT = 'HUF'
    ISRAELI_SHEKEL = 'ILS'
    INDIAN_RUPEE = 'INR'
    INDONESIAN_RUPIAH = 'IDR'
    JAMAICAN_DOLLAR = 'JAD'
    JAPANESE_YEN = 'JYE'
    KENYAN_SCHILLING = 'KES'
    KAZACHSTAN_T_ENGE = 'KZT'
    KUWAITI_DINAR = 'KUD'
    LATVIAN_LATS = 'EURO'
    LIBYAN_DINAR = 'LYD'
    LITHUANIAN_LITAS = 'EURO'
    MACAU_PATACAS = 'MOP'
    MALAYSIAN_RINGGITS = 'MIR'
    MAURITIAN_RUPEE = 'MUR'
    MOZAMBICAN_METICAL = 'MZN'
    NEW_MEXICAN_PESO = 'NMP'
    NEW_TAIWAN_DOLLAR = 'NTP'
    NEW_TURKISH_LIRA = 'TRY'
    NEW_ZEALAND_DOLLAR = 'NZD'
    NORWEGIAN_KRONE = 'NOK'
    PAKISTAN_RUPEE = 'PKR'
    PANAMA_BALBOA = 'PAB'
    PHILIPPINE_PESO = 'PHP'
    ROMANIAN_LEU = 'RON'
    POLISH_ZLOTY = 'PLN'
    RUSSIAN_ROUBLE = 'RUR'
    SAUDI_ARABIAN_RIYAL = 'SAR'
    SINGAPORE_DOLLAR = 'SID'
    SOLOMON_ISLAND_DOLLAR = 'SBD'
    SOUTH_AFRICAN_RAND = 'ZAR'
    SOUTH_KOREAN_WON = 'WON'
    SWEDISH_KRONA = 'SEK'
    SWISS_FRANCS = 'SFR'
    EURO_THAILAND_BAHT = 'THB'
    TONGA_PAANGA= 'TOP'
    TRINIDAD_AND_TOBAGO_DOLLAR = 'TTD'
    UGANDA_SCHILLING = 'UGX'
    UK_POUNDS_STERLING = 'UKL'
    UNITED_ARAB_EMIRATES_DIRHAM = 'DHS'
    URUGUAY_NEW_PESO= 'UYP'
    US_DOLLAR= 'USD'
    VENEZUELA_BOLIVAR_FUERTE= 'VEF'
    VIETNAMESE_DONG = 'VND'
    WESTERN_SAMOA_TALA = 'WST'


class PackageLocationEnum(str, Enum):
    "Provides a location description where the courier/driver will pick up the package."
    FRONT = 'FRONT'
    NONE = 'NONE'
    SIDE = 'SIDE'
    REAR = 'REAR'

class BuildingPartCodeEnum(str, Enum):
    "Describes the package location building type for the pickup."
    PARTMENT = 'APARTMENT'
    BUILDING = 'BUILDING'
    DEPARTMENT = 'DEPARTMENT'
    FLOOR = 'FLOOR'
    ROOM = 'ROOM'
    SUITE = 'SUITE'

class PickupServiceCategoryEnum(str, Enum):
    """Specify the service category for the pickup being scheduled."""
    SAME_DAY = 'SAME_DAY'
    SAME_DAY_CITY = 'SAME_DAY_CITY'
    FEDEX_DISTANCE_DEFERRED = 'FEDEX_DISTANCE_DEFERRED'
    FEDEX_NEXT_DAY_EARLY_MORNING = 'FEDEX_NEXT_DAY_EARLY_MORNING'
    FEDEX_NEXT_DAY_MID_MORNING = 'FEDEX_NEXT_DAY_MID_MORNING'
    FEDEX_NEXT_DAY_AFTERNOON = 'FEDEX_NEXT_DAY_AFTERNOON'
    FEDEX_NEXT_DAY_END_OF_DAY = 'FEDEX_NEXT_DAY_END_OF_DAY'
    FEDEX_NEXT_DAY_FREIGHT = 'FEDEX_NEXT_DAY_FREIGHT'

class LocalizationEnum:
    "Languages allowed in FedEx."

    ARABIC = 'AR'
    CZECH = 'CS'
    DANISH = 'DA'
    GERMAN = 'DE'
    ENGLISH= 'EN'
    SPANISH_LATINOAMERICAN = ('ES', 'ES')
    SPANISH_NORTEAMERICAN = ('ES', 'US')
    FINNISH = 'FI'
    FRENCH_CANADA = ('FR', 'CA')
    FRENCH_EUROPE = 'FR'
    HUNGARIAN = 'HU'
    ITALIAN = 'IT'
    KANJI_JAPAN = 'JA'
    KOREAN = 'KO'
    NORWEGIAN = 'NO'
    DUTCH = 'NL'
    POLISH = 'PL'
    PORTUGUESE_LATINAMERICAN = 'PT'
    RUSSIAN = 'RU'
    SWEDISH = 'SV'
    TURKISH = 'TR'
    CHINESE_SIMPLIFIED = ('CN','ZH')
    CHINESE_TAIWAN = ('ZH', 'TW')
    CHINESE_HONG_KONG = ('ZH','HK')


class PackageStatus(str, Enum):
    """Availables Codes and descriptions."""
    AF = 'AF'
    AR = 'AR'
    FD = 'FD'
    OF = 'OF'
    HL = 'HL'
    AS = 'AS'
    CA = 'CA'
    CC = 'CC'
    CD = 'CD'
    CP = 'CP'
    DE = 'DE'
    DL = 'DL'
    DP = 'DP'
    IT = 'IT'
    DS = 'DS'
    OC = 'OC'
    OD = 'OD'
    PU = 'PU'
    IP = 'IP'
    SE = 'SE'
    RR = 'RR'
    TR = 'TR'
    class Descriptions:
        """Descriptions from status code."""
        AF = 'At FedEx destination facility'
        AR = 'Arrived at FedEx location'
        FD = AF
        OF = 'At FedEx origin facility'
        HL = AF
        AS = 'Address Corrected'
        CA = 'Shipment Cancelled by sender'
        CC = 'International shipment release'
        CD = 'Clearance delay'
        CP = 'Clearance in progress'
        DE = 'Delivery Exception'
        DL = 'Delivered'
        DP = 'Departed FedEx location'
        IT = 'In transit'
        DS = 'US export approved'
        OC = 'Shipment information sent to FedEx'
        OD = 'On FedEx vehicle for delivery'
        PU = 'Picked Up'
        IP = 'In FedEx possession'
        SE = 'Shipment Exception'
        RR = 'Hold at Location request received'
        TR = 'Transfer'
    class CarrierStatus:
        """ The status that can has each carrier."""
        FDXE = ['AF', 'AR', 'FD', 'OF', 'HL', 'AS', 'CA', 'CC', 'CD', 'CP', 'DE', 'DL',
                'DP', 'IT', 'DS', 'OC', 'OD', 'PU', 'IP', 'SE', 'RR', 'TR']

class CustomerReferenceType(str, Enum):
    """Customer reference types."""
    CUSTOMER_REFERENCE = 'CUSTOMER_REFERENCE'
    DEPARTMENT_NUMBER = 'DEPARTMENT_NUMBER'
    INTRACOUNTRY_REGULATORY_REFERENCE = 'INTRACOUNTRY_REGULATORY_REFERENCE'
    INVOICE_NUMBER = 'INVOICE_NUMBER'
    P_O_NUMBER = 'P_O_NUMBER'
    RMA_ASSOCIATION = 'RMA_ASSOCIATION'
    SHIPMENT_INTEGRITY = 'SHIPMENT_INTEGRITY'

class ProcessingOptionsEnum(str, Enum):
    """Track processing options."""
    INCLUDE_DETAILED_SCANS = 'INCLUDE_DETAILED_SCANS'

class PickupRequestTypeEnum(str, Enum):
    """Pickuo request type."""
    SAME_DAY = 'SAME_DAY'
    FUTURE_DAY = 'FUTURE_DAY'

class CountryRelationshipEnum(str, Enum):
    """Contry Relationship."""
    DOMESTIC = 'DOMESTIC'
    INTERNATIONAL = 'INTERNATIONAL'

class TrackingIdTypeEnum(str, Enum):
    """Tracking types."""
    EXPRESS = "EXPRESS"
    FEDEX="FEDEX"
    FREIGHT="FREIGHT"
    GROUND="GROUND"
    USPS="USPS"

class DeletionControlEnum(str, Enum):
    """Deletion ship type."""
    DELETE_ALL_PACKAGES = "DELETE_ALL_PACKAGES"
    DELETE_ENTIRE_CONSOLIDATION = "DELETE_ENTIRE_CONSOLIDATION"
    DELETE_ONE_PACKAGE = "DELETE_ONE_PACKAGE"
    LEGACY = "LEGACY"

class CommodityPurposeTypeEnum(str, Enum):
    """Used for calculation of duties and taxes."""
    BUSINESS = 'BUSINESS'
    CONSUMER = 'CONSUMER'

class MeasureEnum(str, Enum):
    """Measure type."""
    QUANTITY = 'QUANTITY'
    UNITS = 'UNITS'

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------