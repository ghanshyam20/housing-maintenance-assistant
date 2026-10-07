# Reflection: [your project name]

*(1 page max, per spec.md requirement 4. Fill in after your solution works, not before —
concrete answers are much easier to write about something real than something planned.)*

## Where automation vs. AI judgment was used, and why

Which steps are rule-based, and which use the LLM? For each AI-judgment step, why couldn't a
rule-based approach handle it reliably?

## The agentic pattern, and what you actually verified about it

What does your tool-use loop actually do? If you tested it against multiple scenarios (a single
tool call, several tool calls in one request, anything else), say what you found — including
anything that *didn't* work the way you expected. A specific, honest account of a real limitation
is worth more here than a claim that everything worked perfectly.

## Human-in-the-loop design

Where, specifically, does your system require human confirmation before a consequential action?
What happens if the human declines?

## Risks considered

Accuracy (can your AI-judgment step be wrong, and what happens if it is?), latency (how long do
your LLM calls actually take?), and anything specific to running everything locally that came up
while building this.
