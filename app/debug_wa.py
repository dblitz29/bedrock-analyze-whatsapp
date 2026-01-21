# app/debug_wa.py
from typing import Any, Dict

def debug_payload_shape(payload: Dict[str, Any]) -> None:
    print("Top-level keys:", list(payload.keys()))

    entry = payload.get("entry", [])
    if not entry:
        print("entry empty")
        return

    e0 = entry[0]
    changes = e0.get("changes", [])
    if not changes:
        print("changes empty")
        return

    c0 = changes[0]
    value = c0.get("value") or {}
    print("value keys:", list(value.keys()))

    messages = value.get("messages", []) or []
    print("value.messages exists; len:", len(messages))
    if not messages:
        return

    m0 = messages[0] or {}
    print("first message keys:", list(m0.keys()))
    print("first message type:", m0.get("type"))

    txt = m0.get("text") or {}
    print("text keys:", list(txt.keys()))
    body = txt.get("body")
    print("text.body repr:", repr(body))
