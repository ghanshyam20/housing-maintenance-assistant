from mcp.server.mcpserver import MCPServer
from mcp_types import ToolAnnotations
from maintenance import get_request, update_request,get_team


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
    annotations=ToolAnnotations(
        destructiveHint=True,
        readOnlyHint=False
    )
)
def assign_request(request_id: str, category: str, team: str) -> str:
    """Assign a category and maintenance team to a request."""

    request = get_request(request_id)

    if request is None:
        return "Request not found"
    team = get_team(category)

    update_request(request_id, category, team)

    return f"{request_id} assigned to {team} as {category}"


if __name__ == "__main__":
    mcp_server.run(transport="stdio")