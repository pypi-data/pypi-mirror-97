from typing import Iterable, List

from benchling_api_client.api.inventory import validate_barcodes
from benchling_api_client.client import Client

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.models import Barcodes, BarcodeValidationResult
from benchling_sdk.services.base_service import BaseService
from benchling_sdk.services.inventory.box_service import BoxService
from benchling_sdk.services.inventory.container_service import ContainerService
from benchling_sdk.services.inventory.label_service import LabelService
from benchling_sdk.services.inventory.location_service import LocationService
from benchling_sdk.services.inventory.plate_service import PlateService


class InventoryService(BaseService):
    _box_service: BoxService
    _container_service: ContainerService
    _label_service: LabelService
    _location_service: LocationService
    _plate_service: PlateService

    def __init__(
        self, client: Client, retry_strategy: RetryStrategy,
    ):
        super().__init__(client, retry_strategy)
        self._box_service = BoxService(client, retry_strategy)
        self._container_service = ContainerService(client, retry_strategy)
        self._label_service = LabelService(client, retry_strategy)
        self._location_service = LocationService(client, retry_strategy)
        self._plate_service = PlateService(client, retry_strategy)

    @property
    def boxes(self) -> BoxService:
        return self._box_service

    @property
    def containers(self) -> ContainerService:
        return self._container_service

    @property
    def labels(self) -> LabelService:
        return self._label_service

    @property
    def locations(self) -> LocationService:
        return self._location_service

    @property
    def plates(self) -> PlateService:
        return self._plate_service

    @api_method
    def validate_barcodes(self, registry_id: str, barcodes: Iterable[str]) -> List[BarcodeValidationResult]:
        barcodes_list = Barcodes(barcodes=list(barcodes))
        response = validate_barcodes.sync_detailed(
            client=self.client, registry_id=registry_id, json_body=barcodes_list
        )
        results = model_from_detailed(response)
        return results.validation_results
