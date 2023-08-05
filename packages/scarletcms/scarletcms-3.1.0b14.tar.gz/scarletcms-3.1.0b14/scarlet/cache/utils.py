import json
import logging
from typing import Optional, List, Tuple

from django.conf import settings
import requests

BASE_URL = "https://api.cloudflare.com/client/v4"
HEADERS = {
    "Authorization": f"Bearer {settings.CLOUDFLARE['AUTHORIZATION']}",
    "Content-Type": "application/json",
}


def purge_remote_cache(urls: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Function to purge saved pages on remote cache.
    At the moment only Cloudflare is supported.
    """
    api_endpoint = f"{BASE_URL}/zones/{settings.CLOUDFLARE['ZONE_ID']}/purge_cache"
    data = (
        json.dumps({"files": urls}) if urls else json.dumps({"purge_everything": True})
    )
    r = requests.post(url=api_endpoint, data=data, headers=HEADERS, timeout=6.0)
    log_func = logging.info if r.ok else logging.error
    log_func(r.json())

    if r.ok:
        return True, "Cache flushed successfully"
    else:
        return False, f"Something went wrong. Response: {r.json()}"
