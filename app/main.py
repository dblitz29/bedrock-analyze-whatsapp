import json

from app.config import get_settings
from app.prompts import build_analysis_prompt
from app.bedrock_nova import invoke_nova_pro
from app.debug_wa import debug_payload_shape

import app.wa_parser as wa_parser


def main():
    s = get_settings()

    print("main.py running from:", __file__)
    print("wa_parser loaded from:", wa_parser.__file__)
    print("wa_parser.extract_text_messages:", wa_parser.extract_text_messages)

    with open(s.input_json, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # 🔒 Hard-check: pastikan jalur body memang ada
    try:
        direct_body = (
            payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        )
        print("direct body repr:", repr(direct_body))
    except Exception as e:
        print("direct body check failed:", repr(e))

    texts = wa_parser.extract_text_messages(payload)
    print("texts length:", len(texts))
    print("texts repr:", repr(texts))

    if not texts:
        debug_payload_shape(payload)
        raise SystemExit("No text messages found in the input JSON.")

    conversation_text = wa_parser.build_conversation_text(texts)
    prompt = build_analysis_prompt(conversation_text)

    analysis = invoke_nova_pro(
        aws_region=s.aws_region,
        model_id=s.nova_pro_model_id,
        prompt=prompt,
        temperature=s.temperature,
        max_tokens=s.max_tokens
    )

    output = {
        "source": "whatsapp_webhook",
        "messages_extracted": texts,
        "analysis": analysis
    }

    with open(s.output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"DONE -> {s.output_json}")


if __name__ == "__main__":
    main()
