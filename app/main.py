import json
from app.config import get_settings
from app.wa_parser import extract_text_messages, build_conversation_text
from app.prompts import build_analysis_prompt
from app.bedrock_nova import invoke_nova_pro

def main():
    s = get_settings()

    with open(s.input_json, "r", encoding="utf-8") as f:
        payload = json.load(f)
    
    texts = extract_text_messages(payload)
    if not texts:
        raise SystemExit("No text messages found in the input JSON.")

    conversation_text = build_conversation_text(texts)
    prompt = build_analysis_prompt(conversation_text)

    analysis = invoke_nova_pro(
        aws_region=s.aws_region,
        model_id=s.nova_pro_model_id,
        prompt=prompt,
        temperature=s.temperature,
        max_tokens=s.max_tokens
    )

    output = {
        "source" : "whatsapp_webhook",
        "messages_extracted": texts,
        "analysis": analysis
    }

    with open(s.output_json, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"DONW -> {s.output_json}")

if __name__ == "__main__":
    main()