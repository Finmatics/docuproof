from docuproof.models import Batch
from docuproof.utils import get_batch_threshold_dt


async def upload_batches() -> None:
    threshold_dt = get_batch_threshold_dt()
    batches = Batch.filter(created_at__lt=threshold_dt)
    for batch in batches:
        await batch.upload()
