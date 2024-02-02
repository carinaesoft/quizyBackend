import uuid
from datetime import datetime

def generate_custom_unique_identifier():
    timestamp = datetime.utcnow().strftime('%Y%m%d-%H:%M:%S%f')
    custom_uuid = f"{uuid.uuid4().hex}_{timestamp}"
    return custom_uuid

