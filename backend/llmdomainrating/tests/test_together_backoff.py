"""No-network tests for TogetherClient's 429/503 rate-limit backoff.

The repo has no configured test framework, so the supported (verified) runner
is a plain script from the `backend/` dir:

    uv run python llmdomainrating/tests/test_together_backoff.py

The functions are also pytest-style, so `uv run pytest` works in any env that
has the package's provider deps (anthropic, google, etc.) installed.
"""
import types

from llmdomainrating import api
from llmdomainrating.api import TogetherClient as TC


# --- header/status extraction -------------------------------------------------

def test_status_and_reset_together_sdk_shape():
    """Regression: the Together SDK stores headers + http_status directly on the
    exception (no .response). _status_and_reset must honor x-ratelimit-reset
    from exc.headers, not only exc.response.headers."""
    from together import error as terr

    exc = terr.RateLimitError(
        message="rate limited", headers={"x-ratelimit-reset": "37"}, http_status=429
    )
    status, reset = TC._status_and_reset(exc)
    assert status == 429, status
    assert reset == 37.0, reset


def test_status_and_reset_httpx_shape():
    """Fallback path: headers on exc.response.headers (httpx/openai style)."""
    exc = types.SimpleNamespace(
        status_code=429,
        response=types.SimpleNamespace(
            status_code=429, headers={"x-ratelimit-reset": "12"}
        ),
    )
    status, reset = TC._status_and_reset(exc)
    assert status == 429 and reset == 12.0, (status, reset)


def test_status_and_reset_no_header():
    exc = types.SimpleNamespace(http_status=503, headers=None, response=None)
    status, reset = TC._status_and_reset(exc)
    assert status == 503 and reset is None, (status, reset)


# --- retry / backoff loop -----------------------------------------------------

class _FakeExc(Exception):
    def __init__(self, status, headers=None):
        self.http_status = status
        self.headers = headers or {}


def _make_client(seq):
    """seq: exceptions to raise in order, then return the sentinel string."""
    calls = {"n": 0}

    class _Create:
        def create(self, **kw):
            i = calls["n"]
            calls["n"] += 1
            if i < len(seq):
                raise seq[i]
            return "SENTINEL"

    c = TC.__new__(TC)
    c.client = types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=_Create())
    )
    return c, calls


def _patch_sleep():
    slept = []
    api.time.sleep = lambda d: slept.append(d)
    return slept


def test_retries_then_succeeds_and_honors_reset():
    slept = _patch_sleep()
    c, calls = _make_client(
        [_FakeExc(429, {"x-ratelimit-reset": "3"}), _FakeExc(503)]
    )
    out = c._create_with_backoff(model="m", messages=[])
    assert out == "SENTINEL"
    assert calls["n"] == 3
    assert len(slept) == 2
    assert slept[0] >= 3.0  # honored reset=3 (+jitter)


def test_non_retriable_reraises_immediately():
    slept = _patch_sleep()
    c, _ = _make_client([_FakeExc(400)])
    try:
        c._create_with_backoff(model="m", messages=[])
        raise AssertionError("should have raised")
    except _FakeExc:
        pass
    assert slept == []


def test_exhausts_after_max_retries():
    slept = _patch_sleep()
    c, calls = _make_client([_FakeExc(429) for _ in range(20)])
    try:
        c._create_with_backoff(model="m", messages=[])
        raise AssertionError("should have raised")
    except _FakeExc:
        pass
    assert calls["n"] == TC.MAX_RETRIES
    assert len(slept) == TC.MAX_RETRIES - 1


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS  {t.__name__}")
    print(f"\nAll {len(tests)} tests passed")
