import os
from openai import OpenAI

# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt template
SYSTEM_PROMPT = """
You are an expert AI tutor for vocational training students.
Explain concepts using simple language, diagrams (text-based), steps, examples, safety tips, and practical applications.
Always tailor explanations to the selected vocational stream.
Format responses clearly.
"""

def get_tutor_response(query, stream):
    prompt = f"""
    Vocational Stream: {stream}
    Student Question: {query}

    Provide a step-by-step explanation suitable for a student.
    """

    response = client.chat.completions.create(
        model="gpt-4.1",   # or gpt-5.1 if you have access
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message["content"]


