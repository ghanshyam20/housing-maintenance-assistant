# Housing Maintenance Assistant

This project is an AI-augmented RPA solution for handling housing maintenance requests.

The requests are stored in a local CSV file. The program checks the request, uses a local LLM to classify the problem, selects the maintenance team using Python rules, and asks for human approval before updating the request.

## Main Features

- Reads maintenance requests from a CSV file
- Checks required request fields
- Uses Ollama with llama3.1:8b for text classification
- Classifies requests as Plumbing, Electrical, Heating, Building, or Other
- Uses rule-based team assignment
- Requires human approval before changing request data
- Provides maintenance functions as local MCP tools
- Logs assignment actions
- Uses synthetic test data

## Requirements

- Python 3
- Ollama
- llama3.1:8b
- MCP
- pytest

Install the Python requirements:

```bash
pip install -r requirements.txt
```

Install the local Ollama model:

```bash
ollama pull llama3.1:8b
```

## Run the Project

Run the normal maintenance bot:

```bash
python bot.py
```

Run the MCP agent:

```bash
python agent.py
```

Run the tests:

```bash
pytest -v
```

## How It Works

1. A maintenance request is read from the CSV file.
2. Required fields are checked using Python rules.
3. The problem description is classified by the local LLM.
4. Python rules select the correct maintenance team.
5. Human confirmation is required before the request is assigned.
6. Approved assignments are saved and logged.

The LLM runs locally with Ollama. No hosted AI API is used.
