# process.md — AI-Native Development Process for CampusBite

**Course:** INF316  
**Product:** CampusBite (SDU cafeteria and coffee preorder)  
**Companion files:** `chat-brainstorm.md`, `AGENT.md`, `roles/pm.md`

This document describes **how** CampusBite is built with an AI coding agent. It is a delivery playbook, not a feature backlog. The agent and the student follow the same steps.

---

## 0. Why AI-native here

Classical waterfall would freeze a 40-page SRS, then code for weeks. CampusBite does not need that. The painful moment is local and observable: the SDU break queue.

AI-native means:

1. **Intent is written once** (problem, constraints, roles) and reused as agent context.
2. **Implementation happens in vertical slices** the agent can run and the student can click.
3. **The human stays product owner:** accepts, rejects, and redirects; the agent writes and revises code.
4. **Documents stay smaller than the product.** If a rule matters, it lives in `AGENT.md` or a role file, not in a parallel wiki.

---

## 1. Roles in this process

| Role | Who | Responsibility |
|------|-----|----------------|
| Product owner / student | Жақсылық | Priority, campus truth, acceptance |
| Product Manager (virtual) | `roles/pm.md` + agent in PM mode | Scope, MVP, user stories |
| AI coding agent | Cursor (or similar) following `AGENT.md` | Design-in-the-small, code, tests, verification |
| Staff / kitchen advisor | Imagined SDU cafeteria worker | Usability of the staff board (huge buttons, few fields) |

The student may ask the same agent to “act as PM” using `roles/pm.md`, then switch back to implementation. Do not mix a scope increase and a large refactor in one prompt.

---

## 2. Process overview

```
Discover → Freeze MVP → Encode agent rules → Slice → Prompt → Generate
    → Run → Critique → Patch → Accept → Next slice
```

Each cycle should leave the repository **more demoable** than before.

---

## 3. Step-by-step

### Step 1 — Problem capture (done in `chat-brainstorm.md`)

- Describe the SDU queue: who waits, when, what fails.
- List users: student, staff, admin.
- Separate v1 from later ideas.
- Write a north-star metric (time-to-food on break).

**Exit criteria:** a stranger can read the brainstorm and explain CampusBite in one minute.

### Step 2 — Agent constitution (`AGENT.md`)

- Translate product decisions into **inviolable rules** (pickup only, slot caps, mock pay, three roles).
- Fix vocabulary (`Station`, `PickupSlot`, status enum).
- Tell the agent how to slice work and how to verify.

**Exit criteria:** a new chat that only has `AGENT.md` would not build a delivery clone.

### Step 3 — Role cards (`roles/`)

- Start with Product Manager.
- Later roles (designer, backend, QA) may be added the same way: short, operational, CampusBite-specific.

**Exit criteria:** when the student says “act as PM”, the agent knows the MVP freeze and rejection tests.

### Step 4 — Choose a thin vertical slice

The PM (human or agent-as-PM) picks **one** outcome, for example:

> “Seeded student can submit an order for Main Cafeteria in a 12:00–12:10 slot.”

Rules for a valid slice:

- Visible in the UI
- Persisted (survives refresh)
- Has one realistic failure (slot full or sold out)
- Touches at most one new concept beyond what already works

**Anti-pattern:** “Implement the whole REST API.”

### Step 5 — Prompt the agent with context, not novels

A good implementation prompt:

1. Points at `AGENT.md` + the slice outcome
2. Names demo users and stations if relevant
3. Says what **not** to build
4. Asks for verification of happy + failure path

Example:

> Follow `AGENT.md`. Implement slice: student demo user adds one available menu item, selects a pickup slot with remaining capacity, places a mock-paid order, sees `#CB-…` and status `PLACED`. Do not add ratings or Kaspi. Verify slot-full rejection.

### Step 6 — Generate and constrain

The agent should:

- Restate the slice
- Implement
- Seed or migrate data if needed
- Avoid extra files (new markdown, extra UI kits) unless required

The student should interrupt if the agent starts a rewrite of the stack.

### Step 7 — Run-critique-patch loop

1. Start the app.
2. Click the slice as a rushed student on a phone-sized viewport when UI changed.
3. Click the staff path if the order pipeline changed.
4. Note gaps in plain language (“staff cannot see the new order until refresh”).
5. Send **one** correction prompt. Repeat until the slice is honest.

Prefer patching the existing slice over starting a second feature.

### Step 8 — Accept and log the increment

When the slice works, record (in the next prompt or a short commit message if the student asks to commit):

- What a user can do now
- What remains for the north-star loop

Suggested increment order is in `AGENT.md` §5.2.

### Step 9 — Close the full loop, then polish

Do not invest in visual identity until:

- Student order → staff ready → student pickup code is real
- Admin sold-out blocks new carts
- Capacity limits work

After the loop: empty states, copy, accessibility, README.

### Step 10 — Assignment packaging

For INF316 submission, the repository should contain:

| Artifact | Purpose |
|----------|---------|
| `chat-brainstorm.md` | Evidence of AI-assisted discovery |
| `AGENT.md` | Reusable agent instructions |
| `process.md` | This methodology |
| `roles/pm.md` | Role specialization |
| Application code | Executable product |
| README | Run instructions + demo accounts |

The write-up should explain **how the agent was constrained**, not only that “AI wrote the app.”

---

## 4. Cadence (suggested for one assignment week)

| Day | Focus |
|-----|--------|
| 1 | Brainstorm + AGENT + PM role (this folder) |
| 2 | Auth, stations, menu read |
| 3 | Cart, slots, place order |
| 4 | Staff board + status + pickup code |
| 5 | Admin sold-out, hardening, README, demo rehearsal |

Each day ends with a **clickable** increment.

---

## 5. Quality gates (every slice)

- [ ] Matches `AGENT.md` constraints (no delivery, no real payments unless asked)
- [ ] Server enforces role, price, availability, and slot capacity
- [ ] Happy path demonstrated
- [ ] At least one error path demonstrated
- [ ] Student and staff views do not contradict each other
- [ ] Demo still boots with seed data

If a gate fails, the next prompt is a fix, not a new epic.

---

## 6. Prompt patterns that work for CampusBite

**PM mode**

> Read `roles/pm.md` and `chat-brainstorm.md`. Propose the next slice only. Reject anything outside MVP.

**Build mode**

> Read `AGENT.md`. Implement the approved slice. Verify happy + failure paths.

**QA mode**

> Break the order flow like a student in a 12-minute break and like a barista with wet hands. List bugs, then fix the top three.

**Scope guard**

> Is this feature required for the pickup loop? If no, park it.

---

## 7. Risks of AI-native delivery (and counters)

| Risk | Counter |
|------|---------|
| Agent builds Uber Eats | `AGENT.md` non-goals + PM rejection tests |
| Beautiful UI, dead kitchen | Slice order forces staff board before polish |
| Inconsistent domain names | Vocabulary table is mandatory |
| Silent capacity overflow | Quality gate: slot-full test every order-related change |
| Docs drift from code | Human accepts slices; agent updates names in AGENT if statuses change |
| Unrunnable demo on review day | README + seed accounts from day 2 |

---

## 8. Definition of process success

The process succeeded if another student could clone the repo, give `AGENT.md` to an agent, and extend CampusBite **without re-discovering** that SDU needs pickup slots rather than delivery.

The product succeeded if a demo shows: order before the break, skip the choosing queue, collect by number.
