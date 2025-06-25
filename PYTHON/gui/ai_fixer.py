import openai
import os

def fix_json_with_llm(broken_json):
    openai.api_key = os.getenv("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")  # Do NOT hardcode API key

    prompt = (
        "The following JSON is broken or invalid. Fix it and return only the corrected JSON.\n\n"
        f"{broken_json}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=2048
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"LLM Error: {str(e)}"
