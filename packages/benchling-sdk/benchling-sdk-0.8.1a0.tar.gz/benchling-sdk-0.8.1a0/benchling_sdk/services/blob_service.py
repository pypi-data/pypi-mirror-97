from io import BytesIO
import mimetypes
from pathlib import Path
from typing import Iterable, List, Optional, Union

from benchling_api_client.api.blobs import (
    abort_multipart_blob,
    bulk_get_blobs,
    complete_multipart_blob,
    create_blob,
    create_blob_part,
    create_multipart_blob,
    get_blob,
    get_blob_url,
)

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.file_helpers import calculate_md5, encode_base64
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import array_query_param
from benchling_sdk.models import (
    Blob,
    BlobComplete,
    BlobCreate,
    BlobCreateType,
    BlobMultipartCreate,
    BlobPart,
    BlobPartCreate,
    BlobUrl,
)
from benchling_sdk.services.base_service import BaseService

DEFAULT_HTTP_TIMEOUT: float = 60.0


class BlobService(BaseService):
    @api_method
    def get_by_id(self, blob_id: str) -> Blob:
        response = get_blob.sync_detailed(client=self.client, blob_id=blob_id)
        return model_from_detailed(response)

    @api_method
    def create(self, blob: BlobCreate, timeout_seconds: float = DEFAULT_HTTP_TIMEOUT) -> Blob:
        timeout_client = self.client.with_timeout(timeout_seconds)
        response = create_blob.sync_detailed(client=timeout_client, json_body=blob)
        return model_from_detailed(response)

    @api_method
    def create_from_bytes(
        self,
        input_bytes: Union[BytesIO, bytes],
        name: str,
        mime_type: Optional[str] = None,
        blob_type: BlobCreateType = BlobCreateType.RAW_FILE,
        timeout_seconds: float = DEFAULT_HTTP_TIMEOUT,
    ) -> Blob:
        if isinstance(input_bytes, BytesIO):
            contents = input_bytes.read()
        else:
            contents = input_bytes
        return self._create_blob(
            blob_input=contents,
            name=name,
            blob_type=blob_type,
            mime_type=mime_type,
            timeout_seconds=timeout_seconds,
        )

    @api_method
    def create_from_file(
        self,
        file_path: Path,
        name: Optional[str] = None,
        mime_type: Optional[str] = None,
        blob_type: BlobCreateType = BlobCreateType.RAW_FILE,
        auto_detect: bool = True,
        timeout_seconds: float = DEFAULT_HTTP_TIMEOUT,
    ) -> Blob:
        if not (file_path.exists() and file_path.is_file()):
            raise FileNotFoundError(f"{file_path} does not exist or is not a valid file")
        if auto_detect:
            if not name:
                name = file_path.name
            if not mime_type:
                mime_type = mimetypes.guess_type(str(file_path))[0]
        else:
            assert name, "name must be provided if auto_detect is not set to True"
        with open(file_path, "rb") as file:
            file_contents = file.read()
        return self.create_from_bytes(
            input_bytes=file_contents,
            name=name,
            blob_type=blob_type,
            mime_type=mime_type,
            timeout_seconds=timeout_seconds,
        )

    @api_method
    def download_url(self, blob_id: str) -> BlobUrl:
        response = get_blob_url.sync_detailed(client=self.client, blob_id=blob_id)
        return model_from_detailed(response)

    @api_method
    def bulk_get(self, blob_ids: Iterable[str]) -> List[Blob]:
        blob_ids_string = array_query_param(blob_ids)
        response = bulk_get_blobs.sync_detailed(client=self.client, blob_ids=blob_ids_string)
        results_list = model_from_detailed(response)
        return results_list.blobs

    @api_method
    def create_multipart_upload(self, multipart_blob: BlobMultipartCreate) -> Blob:
        response = create_multipart_blob.sync_detailed(client=self.client, json_body=multipart_blob)
        return model_from_detailed(response)

    @api_method
    def create_part(
        self, blob_id: str, blob_part: BlobPartCreate, timeout_seconds: float = DEFAULT_HTTP_TIMEOUT
    ) -> BlobPart:
        """Uploads a BLOB part. Larger files and slower connections will likely need to set a higher
        timeout_seconds value in order to complete successful part uploads."""
        timeout_client = self.client.with_timeout(timeout_seconds)
        response = create_blob_part.sync_detailed(client=timeout_client, blob_id=blob_id, json_body=blob_part)
        return model_from_detailed(response)

    @api_method
    def complete_multipart_upload(self, blob_id: str, blob_parts: Iterable[BlobPart]) -> Blob:
        blob_complete = BlobComplete(parts=list(blob_parts))
        response = complete_multipart_blob.sync_detailed(
            client=self.client, blob_id=blob_id, json_body=blob_complete
        )
        return model_from_detailed(response)

    @api_method
    def abort_multipart_upload(self, blob_id: str) -> None:
        response = abort_multipart_blob.sync_detailed(client=self.client, blob_id=blob_id)
        # Even though we won't return, will do the other processing such as status checking
        empty_object = model_from_detailed(response)  # noqa: F841

    def _create_blob(
        self,
        blob_input: bytes,
        name: str,
        blob_type: BlobCreateType,
        mime_type: Optional[str],
        timeout_seconds: float,
    ) -> Blob:
        data = encode_base64(blob_input)
        md5 = calculate_md5(blob_input)
        blob_create = BlobCreate(name=name, type=blob_type, data64=data, md5=md5)
        # Use BlobCreate's default mime type unless we specified one
        if mime_type is not None:
            blob_create.mime_type = mime_type
        return self.create(blob=blob_create, timeout_seconds=timeout_seconds)
