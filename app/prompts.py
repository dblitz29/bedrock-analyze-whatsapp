def build_analysis_prompt(conversation_text: str) -> str:
    return f"""
        You are an assistant for customer message analysis.

        Task:
        1) Detect the language of the conversation.
        2) If not Indonesian, provide an Indonesian translation.
        3) Analyze sentiment (positive/neutral/negative) and give a confidence 0-1.
        4) Infer intent category (choose one): complaint, inquiry, request, compliment, spam, other
        5) Extract key entities (names, products, locations, order_id, phone if present).
        6) Provide a concise summary in Indonesian (max 2 sentences).
        7) Provide suggested next action for an agent (1 sentence).

        Return ONLY valid JSON with this exact schema:
        {{
        "detected_language": "string",
        "translation_id": "string",
        "sentiment": {{
            "label": "positive|neutral|negative",
            "confidence": 0.0
        }},
        "intent": {{
            "category": "complaint|inquiry|request|compliment|spam|other",
            "confidence": 0.0
        }},
        "entities": {{
            "names": [],
            "products": [],
            "locations": [],
            "order_id": [],
            "phone": []
        }},
        "summary_id": "string",
        "suggested_next_action": "string"
        }}

        Conversation:
        \"\"\"{conversation_text}\"\"\"
        """.strip()
