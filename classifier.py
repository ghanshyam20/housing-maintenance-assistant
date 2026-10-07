import subprocess

MODEL = "llama3.1:8b"

CATEGORIES = [
    "Plumbing",
    "Electrical",
    "Heating",
    "Building",
    "Other",
]


def classify_request(description):
    prompt = f"""Classify this housing maintenance request into exactly one category:
Plumbing, Electrical, Heating, Building, Other.

Return only the category name.

Request: {description}
"""

    result = subprocess.run(
        ["ollama", "run", MODEL],
        input=prompt,
        text=True,
        capture_output=True,
    )

    category = result.stdout.strip()

    if category not in CATEGORIES:
        return "Other"

    return category
