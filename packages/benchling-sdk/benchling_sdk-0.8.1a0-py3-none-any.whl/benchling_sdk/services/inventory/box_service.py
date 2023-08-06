from typing import Any, Dict, Iterable, List, Optional

from benchling_api_client.api.boxes import (
    archive_boxes,
    bulk_get_boxes,
    create_box,
    get_box,
    list_boxes,
    unarchive_boxes,
    update_box,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import optional_array_query_param, schema_fields_query_param
from benchling_sdk.models import (
    Box,
    BoxCreate,
    BoxesArchivalChange,
    BoxesArchive,
    BoxesArchiveReason,
    BoxesPaginatedList,
    BoxesUnarchive,
    BoxUpdate,
    ListBoxesSort,
)
from benchling_sdk.services.base_service import BaseService


class BoxService(BaseService):
    @api_method
    def get_by_id(self, box_id: str) -> Box:
        response = get_box.sync_detailed(client=self.client, box_id=box_id)
        return model_from_detailed(response)

    @api_method
    def boxes_page(
        self,
        *,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListBoxesSort] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        storage_contents_id: Optional[str] = None,
        storage_contents_ids: Optional[str] = None,
        empty_positions: Optional[int] = None,
        empty_positions_gte: Optional[int] = None,
        empty_positions_gt: Optional[int] = None,
        empty_positions_lte: Optional[int] = None,
        empty_positions_lt: Optional[int] = None,
        empty_containers: Optional[int] = None,
        empty_containers_gte: Optional[int] = None,
        empty_containers_gt: Optional[int] = None,
        empty_containers_lte: Optional[int] = None,
        empty_containers_lt: Optional[int] = None,
        ids: Optional[str] = None,
        barcodes: Optional[str] = None,
        archive_reason: Optional[str] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
    ) -> Response[BoxesPaginatedList]:
        return list_boxes.sync_detailed(  # type: ignore
            client=self.client,
            sort=sort,
            schema_id=schema_id,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            ancestor_storage_id=ancestor_storage_id,
            storage_contents_id=storage_contents_id,
            storage_contents_ids=storage_contents_ids,
            empty_positions=empty_positions,
            empty_positionsgte=empty_positions_gte,
            empty_positionsgt=empty_positions_gt,
            empty_positionslte=empty_positions_lte,
            empty_positionslt=empty_positions_lt,
            empty_containers=empty_containers,
            empty_containersgte=empty_containers_gte,
            empty_containersgt=empty_containers_gt,
            empty_containerslte=empty_containers_lte,
            empty_containerslt=empty_containers_lt,
            ids=ids,
            barcodes=barcodes,
            archive_reason=archive_reason,
            schema_fields=schema_fields_query_param(schema_fields),
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        *,
        sort: Optional[ListBoxesSort] = None,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ancestor_storage_id: Optional[str] = None,
        storage_contents_id: Optional[str] = None,
        storage_contents_ids: Optional[List[str]] = None,
        empty_positions: Optional[int] = None,
        empty_positions_gte: Optional[int] = None,
        empty_positions_gt: Optional[int] = None,
        empty_positions_lte: Optional[int] = None,
        empty_positions_lt: Optional[int] = None,
        empty_containers: Optional[int] = None,
        empty_containers_gte: Optional[int] = None,
        empty_containers_gt: Optional[int] = None,
        empty_containers_lte: Optional[int] = None,
        empty_containers_lt: Optional[int] = None,
        ids: Optional[str] = None,
        barcodes: Optional[str] = None,
        archive_reason: Optional[str] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[Box]:
        storage_contents_ids_list = optional_array_query_param(storage_contents_ids)

        def api_call(next_token: NextToken) -> Response[BoxesPaginatedList]:
            return self.boxes_page(
                sort=sort,
                schema_id=schema_id,
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                ancestor_storage_id=ancestor_storage_id,
                storage_contents_id=storage_contents_id,
                storage_contents_ids=storage_contents_ids_list,
                empty_positions=empty_positions,
                empty_positions_gte=empty_positions_gte,
                empty_positions_gt=empty_positions_gt,
                empty_positions_lte=empty_positions_lte,
                empty_positions_lt=empty_positions_lt,
                empty_containers=empty_containers,
                empty_containers_gte=empty_containers_gte,
                empty_containers_gt=empty_containers_gt,
                empty_containers_lte=empty_containers_lte,
                empty_containers_lt=empty_containers_lt,
                ids=ids,
                barcodes=barcodes,
                archive_reason=archive_reason,
                schema_fields=schema_fields,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: BoxesPaginatedList) -> Optional[List[Box]]:
            return body.boxes

        return PageIterator(api_call, results_extractor)

    @api_method
    def bulk_get(
        self, *, box_ids: Optional[Iterable[str]] = None, barcodes: Optional[Iterable[str]] = None
    ) -> Optional[List[Box]]:
        box_id_string = optional_array_query_param(box_ids)
        barcode_string = optional_array_query_param(barcodes)
        response = bulk_get_boxes.sync_detailed(
            client=self.client, box_ids=box_id_string, barcodes=barcode_string
        )
        boxes_list = model_from_detailed(response)
        return boxes_list.boxes

    @api_method
    def create(self, box: BoxCreate) -> Box:
        response = create_box.sync_detailed(client=self.client, json_body=box)
        return model_from_detailed(response)

    @api_method
    def update(self, box_id: str, box: BoxUpdate) -> Box:
        response = update_box.sync_detailed(client=self.client, box_id=box_id, json_body=box)
        return model_from_detailed(response)

    @api_method
    def archive(
        self, box_ids: Iterable[str], reason: BoxesArchiveReason, should_remove_barcodes: bool
    ) -> BoxesArchivalChange:
        archive_request = BoxesArchive(
            box_ids=list(box_ids), reason=reason, should_remove_barcodes=should_remove_barcodes
        )
        response = archive_boxes.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, box_ids: Iterable[str]) -> BoxesArchivalChange:
        unarchive_request = BoxesUnarchive(box_ids=list(box_ids))
        response = unarchive_boxes.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)
