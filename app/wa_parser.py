from typing import Any, Dict, List

def extract_text_messages(payload: Dict[str, Any]) -> List[str]:
    texts: List[str] = []
    for entry in payload.get("entry", []) or []:
        value = entry.get("value", {})
        messages = value.get("messages", []) or []
        for msg in messages:
            if msg.get("type") == "text":
                body = (msg.get("text") or {}).get("body", "") or ""
                body = body.strip()
                if body:
                    texts.append(body)

    return texts

def build_conversation_text(texts: List[str]) -> str:
    return "\n".join([f" - {t}" for t in texts]).strip()
"