import json

import requests

url = "http://localhost:11434/api/generate"

# Ollama streams by default, so we just pass the prompt
payload = json.dumps(
    {"model": "phi3", "prompt": "One statement description for microservices"}
)
headers = {"Content-Type": "application/json"}

# Enable streaming by adding stream=True
response = requests.request("POST", url, headers=headers, data=payload, stream=True)

# Process the stream line by line
for line in response.iter_lines():
    if line:
        # Parse the JSON line sent by Ollama
        json_response = json.loads(line.decode("utf-8"))

        # Get the next token/word
        token = json_response.get("response", "")

        # Print the token immediately without newline or buffering
        print(token, end="", flush=True)

print()  # Final newline when done
