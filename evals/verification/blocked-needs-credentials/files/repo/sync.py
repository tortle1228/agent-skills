import os
import time
import urllib.request

MAX_RETRIES = 3


def push(payload):
    token = os.environ["SYNC_TOKEN"]
    request = urllib.request.Request(
        "https://sync.example.invalid/v1/push",
        data=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    for attempt in range(MAX_RETRIES):
        try:
            return urllib.request.urlopen(request, timeout=5).read()
        except OSError:
            time.sleep(2 ** attempt)
    raise RuntimeError("push failed")
