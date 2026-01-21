import json
from typing import Any, Dict, List

import boto3


def _extract_text_from_converse(resp: Dict[str, Any]) -> str:
    content = (resp.get("output", {}).get("message", {}).get("content", []) or [])
    parts: List[str] = []
    for item in content:
        if "text" in item and item["text"]:
            parts.append(item["text"])
    return "\n".join(parts).strip()


def invoke_nova_pro(
    *,
    aws_region: str,
    model_id: str,
    prompt: str,
    temperature: float,
    max_tokens: int
) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name=aws_region)

    resp = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        inferenceConfig={
            "temperature": float(temperature),
            "maxTokens": int(max_tokens),
        },
    )

    out_text = _extract_text_from_converse(resp)

    # Prompt kamu minta output JSON murni → parse langsung
    return json.loads(out_text)
