from io import BytesIO

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json, raw
from sanic.views import HTTPMethodView
from tortoise.exceptions import IntegrityError
from web3.exceptions import ContractLogicError

from docuproof.blockchain import DocuProofContract
from docuproof.decorators import token_required
from docuproof.exceptions import Http404, HttpBadRequest, HttpInternalServerError
from docuproof.ipfs import IPFSClient
from docuproof.models import Batch, File
from docuproof.utils import (
    get_bytes_hash,
    get_file_hash,
    get_pdf_metadata,
    write_pdf_metadata,
)


async def health(request: Request) -> HTTPResponse:
    return json({"status": "ok"})


bp = Blueprint("api", url_prefix="/api", version=1)


class StoreView(HTTPMethodView):
    @token_required
    async def post(self, request: Request) -> HTTPResponse:
        def create_file(batch: Batch, uuid: str, sha256: str) -> File:
            return File.create(batch=batch, uuid=uuid, sha256=sha256)

        form = request.form
        files = request.files
        if not form or not files:
            raise HttpBadRequest("Invalid input data")

        if not (uuid := form.get("uuid", None)):
            raise HttpBadRequest("Missing field `uuid`")

        if not (file := files.get("file", None)):
            raise HttpBadRequest("Missing PDF file")

        batch = await Batch.get_current_batch()
        updated_pdf = write_pdf_metadata(
            file=BytesIO(file.body), metadata={"UUID": str(uuid), "ProofID": str(batch.proof_id)}
        )
        sha256 = get_file_hash(updated_pdf)

        try:
            await create_file(batch=batch, uuid=uuid, sha256=sha256)
        except IntegrityError:
            raise HttpBadRequest("File with this UUID already exists")

        return raw(updated_pdf.read(), content_type="application/pdf", headers={"Proof-ID": str(batch.proof_id)})


class ValidateView(HTTPMethodView):
    async def post(self, request: Request) -> HTTPResponse:
        form = request.form
        files = request.files
        if not files or not (file := files.get("file", None)):
            raise HttpBadRequest("Missing PDF file")

        metadata = get_pdf_metadata(file=BytesIO(file.body))
        if not (uuid := metadata.get("/UUID", None)):
            raise HttpBadRequest("Missing UUID in PDF metadata")
        if not (proof_id := metadata.get("/ProofID", None)):
            raise HttpBadRequest("Missing Proof ID in PDF metadata")
        sha256 = get_bytes_hash(file.body)

        if form.get("force_blockchain", None) not in ["True", "true", "1"]:
            if file_obj := await File.filter(uuid=uuid).first():
                if file_obj.sha256 == sha256:
                    return json({"message": "Hash is valid (in local database)", "status": 200})
                else:
                    return json({"message": "Hash is invalid (in local database)", "status": 200})

        # Validate in blockchain if not found locally
        try:
            ipfs_hash = DocuProofContract().get_ipfs_hash(proof_id)
            if ipfs_hash:
                data = IPFSClient().get_json(ipfs_hash)
                for item in data:
                    if item["uuid"] == uuid:
                        if item["sha256"] == sha256:
                            return json({"message": "Hash is valid (on blockchain)", "status": 200})
                        else:
                            return json({"message": "Hash is invalid (on blockchain)", "status": 200})

                raise HttpInternalServerError("UUID not found in IPFS object")
        except ContractLogicError:
            raise Http404("Proof ID not found in blockchain")

        raise Http404


bp.add_route(StoreView.as_view(), "/store")
bp.add_route(ValidateView.as_view(), "/validate")
