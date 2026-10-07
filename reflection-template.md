# Reflection: Housing Maintenance Assistant



## Where automation vs. AI judgment was used, and why

I used normal Python rules for steps where the result is clear. The bot reads the request from the CSV file, checks required fields, maps a category to the correct maintenance team, updates the request, and writes a log.

The LLM is used to classify the free-text problem into Plumbing, Electrical, Heating, Building, or Other. I used AI here because residents can describe the same problem in many different ways. Simple keyword rules would not always understand these descriptions. The classification runs locally with Ollama using llama3.1:8b. Only the problem description is sent to the model, not the resident's name, phone number or address.

## The agentic pattern, and what you actually verified about it

I exposed maintenance functions as local MCP tools. The agent can discover tools for reading a request, classifying a maintenance problem and assigning a request. I tested the tools through the agent and confirmed that it could call a read-only tool and return request information. I also tested AI classification through an MCP tool.

One limitation I noticed was that the LLM is not always consistent with an unclear description. For example, the request about a strange noise inside a wall was classified as Other in one test and Building in another. I also found that letting the model suggest the team name could produce an incorrect team name, so I changed team selection to a fixed Python mapping instead.


## Human-in-the-loop design

Assigning a maintenance request changes the stored data, so this action requires human confirmation. Before the MCP agent performs the assignment, it shows the proposed action and asks whether to continue. I tested both choices. When I approved it, the request was updated. When I declined it, the request stayed unchanged.

## Risks considered


The main accuracy risk is incorrect or inconsistent LLM classification. Human confirmation and rule-based team mapping reduce the effect of this. Local LLM calls are also slower than the normal Python rules, especially compared with CSV lookup or validation.

Everything runs locally and no hosted AI API is used. This helps keep the data on the local machine, but Ollama must be running and the computer needs enough resources for the model. The project currently uses synthetic data and a CSV file, so a real system would also need stronger access control, data storage and privacy handling.
