from dataclasses import dataclass
from typing import Any

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from docuproof.blockchain import DocuProofContract
from docuproof.decorators import token_required
from docuproof.exceptions import Http404, HttpBadRequest, HttpInternalServerError
from docuproof.ipfs import IPFSClient
from docuproof.models import Batch, File

bp = Blueprint("api", url_prefix="/api", version=1)


@dataclass
class InputData:
    uuid: str
    sha256: str


class SaveHashView(HTTPMethodView):
    def _validate(self, data: dict[str, Any]) -> None:
        input_data = InputData(**data)
        if not input_data.uuid:
            raise HttpBadRequest("Missing field `uuid`")

        if not input_data.sha256:
            raise HttpBadRequest("Missing field `sha256`")

    @token_required
    async def post(self, request: Request) -> HTTPResponse:
        def create_file(batch: Batch, uuid: str, sha256: str) -> File:
            return File.create(batch=batch, uuid=uuid, sha256=sha256)

        data = request.json
        batch = await Batch.get_current_batch()

        if isinstance(data, list):
            for d in data:
                self._validate(d)

            for d in data:
                await create_file(batch=batch, uuid=d["uuid"], sha256=d["sha256"])
        else:
            self._validate(data)
            await create_file(batch=batch, uuid=data["uuid"], sha256=data["sha256"])

        return json({"message": "Hash saved successfully", "status": 200})


class ValidateView(HTTPMethodView):
    @validate(json=InputData)
    async def post(self, request: Request, body: InputData) -> HTTPResponse:
        def compare_hashes_and_create_response(a: str, b: str) -> HTTPResponse:
            if a == b:
                return json({"message": "Hash is valid", "status": 200})
            else:
                return json({"message": "Hash is invalid", "status": 200})

        if file := await File.filter(uuid=body.uuid).first():
            return compare_hashes_and_create_response(file.sha256, body.sha256)

        # Validate in blockchain if not found locally
        ipfs_hash = DocuProofContract().get_ipfs_hash(body.uuid)
        if ipfs_hash:
            data = IPFSClient().get_json(ipfs_hash)
            for item in data:
                if item["uuid"] == body.uuid:
                    return compare_hashes_and_create_response(item["sha256"], body.sha256)

            raise HttpInternalServerError("UUID not found in IPFS object")

        raise Http404


bp.add_route(SaveHashView.as_view(), "/save")
bp.add_route(ValidateView.as_view(), "/validate")
