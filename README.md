# Local LLM API (Ollama + FastAPI)

## Features

- Local model (Mistral via Ollama)
- REST APIs (/generate, /health)
- Timeout handling
- Logging

## Run

1. Install Ollama
2. ollama serve
3. ollama pull mistral or ollama pull phi3
4. ollama run mistral or ollama run phi3
5. pip install -r requirements.txt
6. uvicorn app.main:app --reload

## Ollama Concurrency

Set environment variables
```
OLLAMA_MAX_LOADED_MODELS="2"
OLLAMA_NUM_PARALLEL="2"
```

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
