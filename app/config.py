import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _get_float(name: str, default: float) -> float:
    val = os.getenv(name, str(default)).strip()
    try:
        return float(val)
    except ValueError:
        return default

def _get_int(name: str, default: int) -> int:
    val = os.getenv(name, str(default)).strip()
    try:
        return int(val)
    except ValueError:
        return default
    
@dataclass(frozen=True)
class Settings:
    aws_region: str
    nova_pro_model_id: str
    temperature: float
    max_tokens: int
    input_json: str
    output_json: str

def get_settings() -> Settings:
    return Settings(
        aws_region=os.getenv("AWS_REGION", "ap-southeast-2").strip(),
        nova_pro_model_id=os.getenv("NOVA_PRO_MODEL_ID", "amazon.nova-pro-v1:0").strip(),
        temperature=_get_float("TEMPERATURE", 0.2),
        max_tokens=_get_int("MAX_TOKENS", 800),
        input_json=os.getenv("INPUT_JSON", "whatsapp_payload.json").strip(),
        output_json=os.getenv("OUTPUT_JSON", "result.json").strip(),
    )