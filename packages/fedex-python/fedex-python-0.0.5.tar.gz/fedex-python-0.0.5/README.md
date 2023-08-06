# Fedex Python

NOT official FedEx python library to use its web services.
This library use [zeep library](https://github.com/mvantellingen/python-zeep) for do WSDL requests.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install fedex-python.

```bash
pip install fedex-python
```

## Usage

```python
import fedex-python as fedex

client = fedex.Client(
    key, password, account_number, meter_number,
    localization=(
        fedex.components.auth.Localization.get(
            fedex.components.auth.Localization.SPANISH_LATINOAMERICAN
        )
    ),
    test_mode=True
)

```

### Make a Rate

```python
from fedex_python.components import enums, common, rate_components

response = client.rate.get_rates(
    rate_components.RequestedShipment(
        dropoff_type=enums.DropoffTypeEnum.REGULAR_PICKUP,
        rate_request_types=enums.RateRequestTypeEnum.PREFERRED,
        preferred_currency=enums.CurrencyCodeEnum.US_DOLLAR,
        shipping_charges_payment=common.ShippingChargesPayment(
            payment_type=enums.PaymentTypeEnum.SENDER,
            payor=common.Payor(
                responsible_party=common.ContactAddress(
                    account_number=client.account_number
                )
            )
        ),
        requested_package_line_items=rate_components.RequestedPackageLineItem(
            weight=common.Weight(units=enums.WeightUnits.KG,value=20),
            dimensions=common.Dimensions(
                length=22, height=22,width=22, units=enums.LinearUnits.CM
            )
        ),
        shipper=common.ContactAddress(
            contact=None,
            address=common.Address(
                postal_code='06040',
                country_code='MX',
            )
        )
        recipient=common.ContactAddress(
            contact=None,
            address=common.Address(
                postal_code='15530',
                country_code='MX',
            )
        )
    ), 'Custom id to send FedEx service')
```

### Make a ship
```python
from fedex_python.components import enums, common, ship_components

response = self.client.ship.process_shipment(
    ship_components.RequestedShipment(
    ship_timestamp='2020-02-15T12:00:00',
    dropoff_type=enums.DropoffTypeEnum.REGULAR_PICKUP,
    service_type=enums.ShipServiceTypeEnum.STANDARD_OVERNIGHT,
    packaging_type=enums.PackagingTypeEnum.YOUR_PACKAGING,
    rate_request_types=enums.RateRequestTypeEnum.PREFERRED,
    shipping_charges_payment=common.ShippingChargesPayment(
        payment_type=enums.PaymentTypeEnum.SENDER,
        payor=common.Payor(
            responsible_party=common.ContactAddress(
                account_number=client.account_number
            )
        )
    ),
    requested_package_line_items=common.RequestedPackageLineItemBase(
        weight=common.Weight(units=enums.WeightUnits.KG,value=20),
        dimensions=common.Dimensions(
            length=22, height=22,width=22, units=enums.LinearUnits.CM
        )
    ),
    shipper=common.ContactAddress(
        contact=common.Contact(
            contact_id='Custom id',
            person_name='Sergio Alvarado',
            company_name='Costomit',
            phone_number='55523423324',
            eMail_address='sergioal18v@gmail.com'
        ),
        address=common.Address(
            postal_code='06040',
            country_code='MX',
            street_lines='complete street 209',
            city='Mexico',
        )
    )
    recipient=common.ContactAddress(
        contact=common.Contact(
            contact_id='Custom id',
            person_name='Sergio Alvarado 2',
            company_name='Costomit client',
            phone_number='55523423324',
            eMail_address='sergioal18v2@gmail.com'
        ),
        address=common.Address(
            postal_code='15530',
            country_code='MX',
            street_lines='another street 209',
            city='Mexico',
        )
    )
    label_specification=ship_components.LabelSpecification(
        label_format_type=enums.LabelFormatTypeEnum.COMMON2D,
        label_stock_type=enums.LabelStockTypeEnum.PAPER_LETTER,
        label_printing_orientation=
            enums.LabelPrintingOrientationEnum.BOTTOM_EDGE_OF_TEXT_FIRST,
        image_type=enums.ImageTypeEnum.PDF
    ),
    package_count=1,
    total_weight=common.Weight(
        units=enums.WeightUnits.KG, value=20)
    )
)
    , 'Custom id to send FedEx service')
```

### Cancel a ship
```python
from fedex_python.components import common, enums

response = client.ship.delete_shipment(
    ship_timestamp='2020-02-15T12:00:00',
    tracking_id=common.TrackingId(
        tracking_id_type=enums.TrackingIdTypeEnum.FEDEX,
        tracking_number='the track id number'
    ),
    deletion_control=enums.DeletionControlEnum.DELETE_ALL_PACKAGES,
    custom_id='Custom id to send FedEx service'
)
```

### Create a pickup

```python
from fedex_python.components import common, enums, pickup_components

response = client.pickup.create_pickup(
    origin_detail=pickup_components.OriginDetail(
        buildin_part_description='reference building,
        package_location=enums.PackageLocationEnum.FRONT,
        building_part_code=enums.BuildingPartCodeEnum.BUILDING,
        ready_timestamp='2020-02-15T12:00:00',
        company_close_time='19:00:00',
        pickup_location=common.ContactAddress(
            contact=common.Contact(
                contact_id='Custom id',
                person_name='Sergio Alvarado',
                company_name='Costomit',
                phone_number='55523423324',
                eMail_address='sergioal18v@gmail.com'
            ),
            address=common.Address(
                postal_code='06040',
                country_code='MX',
                street_lines='complete street 209',
                city='Mexico',
            )
        )
    ),
    total_weight=common.Weight(units=enums.WeightUnits.KG, value=22),
    carrier_code=enums.CarrierCodeTypeEnum.FEDEX_EXPRESS,
    package_count=1,
    country_relationship=enums.CountryRelationshipEnum.DOMESTIC,
    custom_id='Custom id to send FedEx service'
)
```

### Cancel a pickup
```python
from fedex_python.components import enums

response = client.pickup.cancel_pickup(
    scheduled_date='2020-02-15T12:00:00',
    pickup_confirmation_number='1',
    location='branch office code given in pickup,
    carrier_code=enums.CarrierCodeTypeEnum.FEDEX_EXPRESS,
    custom_id='Custom id to send FedEx service'
)
```

### Pickup availables
```python
from fedex_python.components import enums, pickup_components

response = self.client.pickup.availability(
    pickup_components.Availability(
        pickup_address=address=common.Address(
            postal_code='06040',
            country_code='MX',
            street_lines='complete street 209',
            city='Mexico',
        ),
        pickup_request_type=enums.PickupRequestTypeEnum.FUTURE_DAY,
        dispatch_date='2020-02-15',
        package_ready_time='12:00:00',
        customer_close_time='19:00:00',
        carriers=enums.CarrierCodeTypeEnum.FEDEX_EXPRESS,
        number_of_business_days=3,
        shipment_attributes=pickup_components.ShipmentAttributes(
            service_type=enums.ShipServiceTypeEnum.STANDARD_OVERNIGHT,
            packaging_type=enums.PackagingTypeEnum.YOUR_PACKAGING
        )
    ), 'Custom id to send FedEx service'
)
```

### Do a Tracking

```python
from fedex_python.components import track_components, enums
response = client.track.track(
    selection_details=track_components.SelectionDetails(
        carrier_code=enums.CarrierCodeTypeEnum.FEDEX_EXPRESS,
        package_identifier=track_components.PackageIdentifier(
            type=enums.PackageIdentifierType.TRACKING_NUMBER_OR_DOORTAG,
            value='yor track',
            account_number=clinet.account_number
        )
    ),
    processing_options=enums.ProcessingOptionsEnum.INCLUDE_DETAILED_SCANS,
    custom_id='Custom id to send FedEx service')
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)