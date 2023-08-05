from typing import Iterable, List, Optional

from benchling_api_client.api.assay_runs import (
    bulk_get_assay_runs,
    create_assay_runs,
    get_assay_run,
    list_assay_runs,
    list_automation_input_generators,
    list_automation_output_processors,
    update_assay_run,
)
from benchling_api_client.types import Response

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import (
    AssayRun,
    AssayRunCreate,
    AssayRunsBulkCreateRequest,
    AssayRunsBulkCreateResponse,
    AssayRunsPaginatedList,
    AssayRunUpdate,
    AutomationFileInputsPaginatedList,
    AutomationFileOutputsPaginatedList,
    AutomationInputGenerator,
    AutomationOutputProcessor,
)
from benchling_sdk.services.base_service import BaseService


class AssayRunService(BaseService):
    @api_method
    def get_by_id(self, assay_run_id: str) -> AssayRun:
        response = get_assay_run.sync_detailed(client=self.client, assay_run_id=assay_run_id)
        return model_from_detailed(response)

    @api_method
    def assay_runs_page(
        self,
        schema_id: str,
        min_created_time: Optional[int] = None,
        max_created_time: Optional[int] = None,
        next_token: NextToken = None,
        page_size: Optional[int] = None,
    ) -> Response[AssayRunsPaginatedList]:
        return list_assay_runs.sync_detailed(
            client=self.client,
            schema_id=schema_id,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            next_token=next_token,
            page_size=page_size,
        )

    def list(
        self,
        schema_id: str,
        min_created_time: Optional[int] = None,
        max_created_time: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[AssayRun]:
        def api_call(next_token: NextToken) -> Response[AssayRunsPaginatedList]:
            return self.assay_runs_page(
                schema_id=schema_id,
                min_created_time=min_created_time,
                max_created_time=max_created_time,
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: AssayRunsPaginatedList) -> Optional[List[AssayRun]]:
            return body.assay_runs

        return PageIterator(api_call, results_extractor)

    @api_method
    def bulk_get(self, assay_run_ids: Iterable[str]) -> Optional[List[AssayRun]]:
        response = bulk_get_assay_runs.sync_detailed(client=self.client, assay_run_ids=list(assay_run_ids))
        runs_list = model_from_detailed(response)
        return runs_list.assay_runs

    @api_method
    def create(self, assay_runs: Iterable[AssayRunCreate]) -> AssayRunsBulkCreateResponse:
        create_runs = AssayRunsBulkCreateRequest(assay_runs=list(assay_runs))
        response = create_assay_runs.sync_detailed(client=self.client, json_body=create_runs)
        return model_from_detailed(response)

    @api_method
    def update(self, assay_run_id: str, assay_run: AssayRunUpdate) -> AssayRun:
        response = update_assay_run.sync_detailed(
            client=self.client, assay_run_id=assay_run_id, json_body=assay_run
        )
        return model_from_detailed(response)

    @api_method
    def automation_input_generators_page(
        self, assay_run_id: str, next_token: NextToken = None,
    ) -> Response[AutomationFileInputsPaginatedList]:
        return list_automation_input_generators.sync_detailed(  # type: ignore
            client=self.client, assay_run_id=assay_run_id, next_token=next_token,
        )

    def automation_input_generators(self, assay_run_id: str) -> PageIterator[AutomationInputGenerator]:
        def api_call(next_token: NextToken) -> Response[AutomationFileInputsPaginatedList]:
            return self.automation_input_generators_page(assay_run_id=assay_run_id, next_token=next_token)

        def results_extractor(body: AutomationFileInputsPaginatedList) -> List[AutomationInputGenerator]:
            return body.automation_input_generators

        return PageIterator(api_call, results_extractor)

    @api_method
    def automation_output_processors_page(
        self, assay_run_id: str, next_token: NextToken = None,
    ) -> Response[AutomationFileOutputsPaginatedList]:
        return list_automation_output_processors.sync_detailed(  # type: ignore
            client=self.client, assay_run_id=assay_run_id, next_token=next_token,
        )

    def automation_output_processors(self, assay_run_id: str) -> PageIterator[AutomationOutputProcessor]:
        def api_call(next_token: NextToken) -> Response[AutomationFileOutputsPaginatedList]:
            return self.automation_output_processors_page(assay_run_id=assay_run_id, next_token=next_token)

        def results_extractor(body: AutomationFileOutputsPaginatedList) -> List[AutomationOutputProcessor]:
            return body.automation_output_processors

        return PageIterator(api_call, results_extractor)
