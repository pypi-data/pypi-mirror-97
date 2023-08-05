import os
from contextlib import contextmanager

SHOULD_USE_SPAN = False
use_span_env = os.getenv("USE_SPAN", "true").lower()
use_span = "true" in use_span_env or "1" in use_span_env

try:
    if use_span:
        from serverless_sdk import span

        SHOULD_USE_SPAN = True
except ModuleNotFoundError as e:
    SHOULD_USE_SPAN = False

print("SHOULD_USE_SPAN", SHOULD_USE_SPAN)

import time

PRINT_SPAN = int(os.getenv("PRINT_SPAN", "1"))
print("PRINT_SPAN", PRINT_SPAN)


@contextmanager
def print_span(label: str):
    start = time.time()
    yield
    time_took = time.time() - start
    if PRINT_SPAN:
        print(f"{label} took {time_took*1_000:.5f} ms.")


@contextmanager
def safe_span(label, use=True):
    if not SHOULD_USE_SPAN or not use:
        with print_span(label):
            yield
    else:
        with span(label):
            yield
