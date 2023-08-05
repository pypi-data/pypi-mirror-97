from benchling_api_client.api.lab_automation import (
    generate_input_with_automation_input_generator,
    get_automation_input_generator,
    get_automation_output_processor,
    process_output_with_automation_output_processor,
    update_automation_output_processor,
)

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import (
    AsyncTaskLink,
    AutomationInputGenerator,
    AutomationOutputProcessor,
    AutomationOutputProcessorUpdate,
)
from benchling_sdk.services.base_service import BaseService


class LabAutomationService(BaseService):
    @api_method
    def input_generator_by_id(self, input_generator_id: str) -> AutomationInputGenerator:
        response = get_automation_input_generator.sync_detailed(
            client=self.client, input_generator_id=input_generator_id
        )
        return model_from_detailed(response)

    @api_method
    def output_processor_by_id(self, output_processor_id: str) -> AutomationOutputProcessor:
        response = get_automation_output_processor.sync_detailed(
            client=self.client, output_processor_id=output_processor_id
        )
        return model_from_detailed(response)

    @api_method
    def update_output_processor(self, output_processor_id: str, file_id: str) -> AutomationOutputProcessor:
        update = AutomationOutputProcessorUpdate(file_id=file_id)
        response = update_automation_output_processor.sync_detailed(
            client=self.client, output_processor_id=output_processor_id, json_body=update
        )
        return model_from_detailed(response)

    @api_method
    def generate_input(self, input_generator_id: str) -> AsyncTaskLink:
        response = generate_input_with_automation_input_generator.sync_detailed(
            client=self.client, input_generator_id=input_generator_id
        )
        return model_from_detailed(response)

    @api_method
    def process_output(self, output_processor_id: str) -> AsyncTaskLink:
        response = process_output_with_automation_output_processor.sync_detailed(
            client=self.client, output_processor_id=output_processor_id
        )
        return model_from_detailed(response)
