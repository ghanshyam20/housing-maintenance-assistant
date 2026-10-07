"""Assignment 2 starter — the agent loop, given complete.

Connects to whatever MCP servers you list in SERVER_SCRIPTS, discovers their
tools, and drives a local LLM (Ollama) through a genuine multi-round loop —
not a single prompt/response. Any tool call is gated by a human confirmation
prompt unless its annotations say it's read-only (see is_consequential).

You shouldn't need to edit this file for most projects — write your own
MCP server(s) (see server_template.py) and point SERVER_SCRIPTS at them.
If your process genuinely needs something this loop doesn't do, that's a
legitimate reason to change it — just document why in your reflection.

Known limitation, tested directly while building this course's reference
solution (see Session 11/12, and Assignment 2's own spec discussion): this
model does not reliably chain a tool's *result value* into a *subsequent*
tool call's argument within one turn. It reliably handles (a) one tool call
per request, and (b) several *independent* tool calls in one request (calls
that don't depend on each other's output). If your process needs step 2's
input to come from step 1's output, do that data-passing in Python — write
two separate agent calls, or a plain function that calls both tools in
sequence — rather than relying on the model to do it inside one turn.

Run: python agent.py
"""
import asyncio
import sys
from contextlib import AsyncExitStack
from pathlib import Path

import ollama
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

MODEL = "llama3.1:8b"
MAX_ROUNDS = 5
BASE_DIR = Path(__file__).parent

# TODO: point this at your own MCP server file(s) — one or more.
SERVER_SCRIPTS = [BASE_DIR / "server_template.py"]


def mcp_tool_to_ollama(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        },
    }


def is_consequential(tool):
    """A tool is safe to call without asking first only if it's explicitly
    marked read-only. No annotations at all -> treated as consequential
    (the safest default, matching the AI Act's own risk-tiering philosophy —
    see Session 14)."""
    ann = tool.annotations
    if ann is None:
        return True
    if ann.read_only_hint:
        return False
    return bool(ann.destructive_hint) or ann.read_only_hint is False


async def confirm_and_call(session, tool, name, args):
    """Returns (text, cancelled). Never asks the LLM to summarize a decline —
    see Session 12's finding on why that's unreliable."""
    if is_consequential(tool):
        print(f"\nThe agent wants to call '{name}' with {args} — this changes data.")
        answer = input("Proceed? [y/N]: ").strip().lower()
        if answer != "y":
            print("Cancelled.")
            return "Action cancelled by the user — did not proceed.", True
    result = await session.call_tool(name, args)
    text = "\n".join(c.text for c in result.content if hasattr(c, "text"))
    return text, False


async def connect_all(stack):
    sessions = []
    for script in SERVER_SCRIPTS:
        params = StdioServerParameters(command=sys.executable, args=[str(script)])
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        sessions.append(session)
    return sessions


async def run_agent(question):
    async with AsyncExitStack() as stack:
        sessions = await connect_all(stack)

        all_tools = []
        tool_session = {}
        tool_obj = {}
        for session in sessions:
            result = await session.list_tools()
            for t in result.tools:
                all_tools.append(mcp_tool_to_ollama(t))
                tool_session[t.name] = session
                tool_obj[t.name] = t
        print(f"Discovered {len(all_tools)} tool(s) across {len(sessions)} server(s): "
              f"{[t['function']['name'] for t in all_tools]}")

        messages = [{"role": "user", "content": question}]

        for round_num in range(1, MAX_ROUNDS + 1):
            response = ollama.chat(model=MODEL, messages=messages, tools=all_tools,
                                    options={"temperature": 0})
            messages.append(response["message"])

            tool_calls = response["message"].get("tool_calls")
            if not tool_calls:
                print(f"FINAL (round {round_num}):", response["message"]["content"])
                return

            round_results = []
            for call in tool_calls:
                name = call["function"]["name"]
                args = call["function"]["arguments"]
                session = tool_session[name]
                tool = tool_obj[name]
                print(f"[round {round_num}] Model wants to call {name} with {args}")
                text, cancelled = await confirm_and_call(session, tool, name, args)
                print(f"[round {round_num}]   -> {text}")
                round_results.append((name, text, cancelled))
                messages.append({"role": "tool", "content": text, "tool_name": name})

            if any(cancelled for _, _, cancelled in round_results):
                print("FINAL:")
                for name, text, cancelled in round_results:
                    tag = "cancelled" if cancelled else "completed"
                    print(f"  [{tag}] {name}: {text}")
                return

        print(f"FINAL: gave up after {MAX_ROUNDS} rounds without a final answer.")


if __name__ == "__main__":
    # TODO: replace with a question relevant to your own process.
    asyncio.run(run_agent("Classify maintenance request M005 and assign it to the appropriate maintenance team."))
