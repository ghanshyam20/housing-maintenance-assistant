from mcp.server.mcpserver import MCPServer
from mcp_types import ToolAnnotations
from maintenance import get_request, update_request,get_team
from classifier import classify_request


mcp_server = MCPServer("housing-maintenance")


@mcp_server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_request_details(request_id: str) -> str:
    """Get one maintenance request using its request ID."""

    request = get_request(request_id)

    if request is None:
        return "Request not found"

    return (
        f"Request: {request['request_id']}\n"
        f"Problem: {request['description']}\n"
        f"Status: {request['status']}\n"
        f"Category: {request['category']}\n"
        f"Team: {request['assigned_team']}"
    )


@mcp_server.tool(
        annotations=ToolAnnotations
        (readOnlyHint=True))
def classify_maintenance_request(request_id: str) -> str:
    """Classify a maintenance request using the local AI model."""

    request = get_request(request_id)

    if request is None:
        return "Request not found"

    category = classify_request(request["description"])
    team = get_team(category)

    return (
        f"Request: {request_id}\n"
        f"Category: {category}\n"
        f"Suggested team: {team}"
    )


@mcp_server.tool(
    annotations=ToolAnnotations(
        destructiveHint=True,
        readOnlyHint=False
    )
)
def assign_request(request_id: str, category: str ) -> str:
    """Assign a maintenance request. Use the actual category returned by
    classify_maintenance_request, such as Plumbing, Electrical, Heating,
    Building, or Other. Do not use placeholder values."""

    request = get_request(request_id)

    if request is None:
        return "Request not found"

    if request["status"] != "Open":
        return f"Request {request_id} is already {request['status']}."

    valid_categories = ["Plumbing", "Electrical", "Heating", "Building", "Other"]

    if category not in valid_categories:
        return f"Invalid category:{category}.Assignment not performed."
    team = get_team(category)


    update_request(request_id, category, team)

    return f"{request_id} assigned to {team} as {category}"


if __name__ == "__main__":
    mcp_server.run(transport="stdio")