import json
from typing import Any, Dict, List
import boto3

def _extract_output_text(nova_response_json: Dict[str, Any]) -> str:
    parts: List[str] = []
    content = {
        nova_response_json.get("output", {})
        .get("message", {})
        .get("content", []))
    } or []

    for item in content:
        txt = item.get("text")
        if txt:
            parts.append(txt)
    return "\n".join(parts).strip()

def invoke_nova_pro(
        *,
        aws_region: str,
        model_id: str,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
    client = boto3.client("bedrock", region_name=aws_region)
    body = {
        "messages" : [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ],
                "inferenceConfig": {
                    "temperature": float(temperature),
                    "maxTokens": int(max_tokens)
                }
            }
        ]
    }

    resp = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),encoded("utf-8")
    )

    raw = resp["body"].read().decode("utf-8")
    data = json.loads(raw)

    out_text = _extract_output_text(data)
    return json.loads(out_text)