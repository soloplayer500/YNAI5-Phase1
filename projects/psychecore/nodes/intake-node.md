# Intake Node
**Role:** Raw thought organization — capture and categorize incoming ideas

---

## Purpose
The Intake Node is the entry point for PsycheCore. It receives raw, unorganized thoughts and transforms them into structured inputs that can be routed to the correct specialized node.

## Responsibilities
- Capture raw thoughts without judgment
- Categorize by type: idea, problem, decision, task, question, emotion
- Identify which node(s) should process the input
- Flag urgency and complexity level
- Extract key entities and topics

## Input Format
Any raw thought, idea, or question.

## Output Format
```
Category: [idea|problem|decision|task|question|emotion|mixed]
Route to: [Anchor|Forge|Ledger|multi-node]
Urgency: [high|medium|low]
Complexity: [high|medium|low]
Structured summary: [clear restatement of the input]
Key entities: [list of people, projects, tools, amounts mentioned]
```

## Routing Logic
- Decision needed → Anchor (for reflection) then Forge (for execution)
- Financial topic → Ledger
- Feeling overwhelmed or unclear → Anchor
- Have an idea and need a plan → Forge
- Complex trade decision → Anchor + Ledger
- Simple task → Forge directly

## Notes
[Add observations as you experiment with this node]
