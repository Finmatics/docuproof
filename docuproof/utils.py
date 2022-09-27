import hashlib
from datetime import datetime, timedelta
from io import BytesIO
from urllib.parse import urlparse

from PyPDF2 import DocumentInformation, PdfReader, PdfWriter
from tortoise import timezone

from docuproof.config import Config


def get_batch_threshold_dt() -> datetime:
    timedelta_kwargs = {Config.BATCH_TIME_UNIT: Config.BATCH_TIME}
    return timezone.now() - timedelta(**timedelta_kwargs)


def convert_url_to_multiaddr(url: str) -> str:
    parsed_url = urlparse(url)
    return f"/dns/{parsed_url.hostname}/tcp/{parsed_url.port}/{parsed_url.scheme}"


def write_pdf_metadata(file: BytesIO, metadata: dict[str, str]) -> BytesIO:
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata({f"/{k}": v for k, v in metadata.items()})

    buffer = BytesIO()
    writer.write_stream(buffer)
    buffer.seek(0)

    return buffer


def get_pdf_metadata(file: BytesIO) -> DocumentInformation | None:
    reader = PdfReader(file)
    return reader.getDocumentInfo()


def get_file_hash(file: BytesIO) -> str:
    content = file.read()
    file.seek(0)
    return hashlib.sha256(content).hexdigest()


def get_bytes_hash(by: bytes) -> str:
    return hashlib.sha256(by).hexdigest()
