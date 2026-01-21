from typing import Any, Dict, List

def extract_text_messages(payload: Dict[str, Any]) -> List[str]:
    texts: List[str] = []

    for entry in (payload.get("entry") or []):
        for change in (entry.get("changes") or []):
            value = change.get("value") or {}
            for msg in (value.get("messages") or []):
                if (msg.get("type") or "").strip() == "text":
                    text_obj = msg.get("text") or {}
                    body = text_obj.get("body", "")
                    body = "" if body is None else str(body)
                    body = body.strip()
                    if body:
                        texts.append(body)

    return texts

def build_conversation_text(texts: List[str]) -> str:
    return "\n".join([f"- {t}" for t in texts]).strip()
