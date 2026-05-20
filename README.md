# Local LLM API (Ollama + FastAPI)

## Features

- Local model (Mistral via Ollama)
- REST APIs (/generate, /health)
- Timeout handling
- Logging

## Run

1. Install Ollama
2. ollama serve
3. ollama pull mistral
4. ollama run mistral
5. pip install -r requirements.txt
6. Add `OLLAMA_URL` in .env file with value as `http://localhost:11434/api/generate`
7. uvicorn app.main:app --reload

## Test

### Generate text response
```
curl --location 'http://localhost:8000/generate-text' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "One statement desciption for microservices"
}'
```

### Generate stream response
```
http://localhost:8000
```