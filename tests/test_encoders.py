import json
import uuid

from docuproof.encoders import UUIDEncoder, uuid_aware_json_encode


def test_uuid_encoder() -> None:
    uuid_obj = uuid.uuid4()
    json_data = json.dumps({"uuid": uuid_obj}, cls=UUIDEncoder)
    assert json_data == f'{{"uuid": "{str(uuid_obj)}"}}'


def test_uuid_aware_json_encode() -> None:
    uuid_obj = uuid.uuid4()
    bytes_data = uuid_aware_json_encode({"uuid": uuid_obj})
    assert bytes_data == f'{{"uuid":"{str(uuid_obj)}"}}'.encode("utf-8")
