"""Assignment 2 starter — an MCP server template. Adapt to YOUR chosen process.

Two example tools below: one read-only (a lookup), one consequential (an
action that changes something). Replace both with tools that make sense for
your own process — you don't need exactly one of each, but per spec.md you
need at least one tool overall, and at least one consequential action gated
by human confirmation (agent.py's confirm_and_call already handles the
gating, driven by the annotations= you set here — see is_consequential in
agent.py for exactly how).

Per spec.md requirement 1, at least one tool (or another part of your
pipeline) needs to use a local LLM for a genuine judgment call a rule-based
bot couldn't reliably do — classification, extraction from unstructured
text, or a decision point. See the example below for the Ollama call
pattern (same as Sessions 9-12).

Run standalone to sanity-check imports: python server_template.py (it'll
just sit there waiting for a client — Ctrl+C to stop).
"""
from pathlib import Path

import ollama
from mcp.server.mcpserver import MCPServer
from mcp_types import ToolAnnotations

BASE_DIR = Path(__file__).parent
MODEL = "llama3.1:8b"

mcp_server = MCPServer("your-server-name-here")


# TODO: replace with a read-only tool relevant to your process. This one's
# a placeholder showing the shape: an LLM-judgment tool, annotated read-only
# because it only returns a suggestion, it doesn't change anything.
@mcp_server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def classify_something(text: str) -> str:
    """TODO: describe what this tool does — this docstring becomes what the
    agent sees when deciding whether to call it, so be specific.
    """
    system_prompt = "TODO: define the categories/task and constrain the output format."
    response = ollama.chat(
        model=MODEL,
        options={"temperature": 0},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return response["message"]["content"].strip()


# TODO: replace with a consequential tool relevant to your process — one
# that actually changes something (moves a file, writes a record, sends
# something). Annotated destructiveHint=True so agent.py's confirmation
# gate requires a human "y" before this ever runs.
@mcp_server.tool(annotations=ToolAnnotations(destructiveHint=True, readOnlyHint=False))
def do_something_consequential(identifier: str) -> str:
    """TODO: describe the consequential action this performs, and what
    `identifier` refers to.
    """
    raise NotImplementedError


if __name__ == "__main__":
    mcp_server.run(transport="stdio")
