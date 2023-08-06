from typing import List, Optional

from benchling_api_client.api.dropdowns import (
    create_dropdown,
    get_dropdown,
    list_dropdowns,
    list_dropdowns_by_registry,
    update_dropdown,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import (
    Dropdown,
    DropdownCreate,
    DropdownSummariesPaginatedList,
    DropdownSummary,
    DropdownUpdate,
)
from benchling_sdk.services.base_service import BaseService


class DropdownService(BaseService):
    @api_method
    def get_by_id(self, dropdown_id: str) -> Dropdown:
        response = get_dropdown.sync_detailed(client=self.client, dropdown_id=dropdown_id)
        return model_from_detailed(response)

    @api_method
    def dropdowns_page(
        self, *, next_token: Optional[str] = None, page_size: Optional[int] = 50,
    ) -> Response[DropdownSummariesPaginatedList]:
        return list_dropdowns.sync_detailed(  # type:ignore
            client=self.client, next_token=next_token, page_size=page_size,
        )

    def list(self, *, page_size: Optional[int] = 50,) -> PageIterator[DropdownSummary]:
        def api_call(next_token: NextToken) -> Response[DropdownSummariesPaginatedList]:
            return self.dropdowns_page(next_token=next_token, page_size=page_size,)

        def results_extractor(body: DropdownSummariesPaginatedList) -> Optional[List[DropdownSummary]]:
            return body.dropdowns

        return PageIterator(api_call, results_extractor)

    @api_method
    def list_by_registry(self, registry_id: str) -> List[DropdownSummary]:
        response = list_dropdowns_by_registry.sync_detailed(client=self.client, registry_id=registry_id)
        dropdowns_list = model_from_detailed(response)
        return dropdowns_list.dropdowns

    @api_method
    def create(self, dropdown: DropdownCreate) -> Dropdown:
        response = create_dropdown.sync_detailed(client=self.client, json_body=dropdown)
        return model_from_detailed(response)

    @api_method
    def update(self, dropdown_id: str, dropdown: DropdownUpdate) -> Dropdown:
        response = update_dropdown.sync_detailed(
            client=self.client, dropdown_id=dropdown_id, json_body=dropdown
        )
        return model_from_detailed(response)
