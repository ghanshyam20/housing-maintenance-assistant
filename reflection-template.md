# Reflection: Housing Maintenance Assistant

## Where automation vs. AI judgment was used, and why

I used normal Python rules for steps where the result is clear. The bot reads the request from the CSV file, checks required fields, maps a category to the correct maintenance team, updates the request, and writes a log.

The LLM is used to classify the free-text problem into Plumbing, Electrical, Heating, Building, or Other. I used AI here because residents can describe the same problem in different ways. Simple keyword rules may not understand all these descriptions correctly. The classification runs locally with Ollama using llama3.1:8b. Only the problem description is sent to the model, not the resident's name, phone number or address.

## The agentic pattern, and what I verified

I exposed three maintenance functions as local MCP tools: reading a request, classifying the maintenance problem, and assigning the request. When the workflow starts, it discovers these tools from the local MCP server.

During testing, I found that the LLM could classify the problem correctly, but it did not always pass the result correctly to the next dependent MCP tool. For example, it classified a request as Electrical but did not correctly use Electrical as the category in the next tool call. I fixed this by passing the classification result between the MCP steps in Python. The LLM still makes the classification decision, but Python controls how that result moves to the next step.

I also found that letting the model decide the team could give a wrong team even when the category was correct. Because the team mapping does not need AI judgment, I changed it to a fixed Python mapping. For example, Electrical always goes to Electrical Team and Heating always goes to Heating Team.

## Human-in-the-loop design

Assigning a maintenance request changes the CSV data, so I require human confirmation before this action. The program first shows the request and AI classification, then shows the proposed action and asks whether to continue.

I tested both choices. When I entered `n`, the action was cancelled and the request stayed unchanged. When I entered `y`, the request was assigned to the correct team, the CSV file was updated, and the assignment was written to the local log.

I also added a check for requests that are already assigned. If the request is not Open, the workflow stops and does not classify or assign it again. I also tested an invalid request ID, and the workflow stopped with "Request not found".

## Risks considered

The main risk is that the LLM can give an incorrect or inconsistent classification, especially when the problem description is unclear. I saw this during testing when an unclear request about a strange noise inside a wall did not always receive the same category. Human confirmation, category validation, and fixed Python team mapping help reduce this risk.

I tested the main Python functions with pytest. The tests covered request lookup, an invalid request ID, valid and missing required data, multiple missing fields, team mapping, and the fallback to Manual Review for an unknown category. All 7 tests passed.

Local LLM calls are slower than normal Python rules such as CSV lookup and validation. Everything runs locally and no hosted AI API is used. Ollama must be running and the computer also needs enough resources to run the model.

The project currently uses synthetic data and a CSV file. For a real system, I would use better data storage, user authentication, access control and stronger privacy handling.