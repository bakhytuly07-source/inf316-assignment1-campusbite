# AGENT.md — CampusBite

Instructions for any AI coding agent that implements, reviews, or extends **CampusBite**.

Read this file before writing code. If a request conflicts with this file, follow this file and state the conflict.

---

## 1. Mission

CampusBite is a campus preorder product for **Suleyman Demirel University**. Students browse today’s menu at the cafeteria and coffee stations, pay (mocked in v1), and pick up food when it is ready so they do not spend the lecture break in a physical queue.

The agent’s job is to ship a **working vertical slice** of that loop, not a marketing site.

North star: *a student who ordered before the break collects food in under three minutes.*

---

## 2. Source of truth

Priority of documents (highest first):

1. This file (`AGENT.md`)
2. `process.md` — how work is sliced and verified
3. `roles/*.md` — role-specific constraints (start with Product Manager)
4. `chat-brainstorm.md` — problem context, MVP freeze, domain sketch

Do not invent a delivery service, social feed, or loyalty program. Those were explicitly cut from v1.

---

## 3. Product constraints the agent must not violate

- **Pickup only.** No courier, no dorm delivery.
- **Stations.** Orders belong to a station (main cafeteria, coffee, bakery, or equivalent).
- **Time slots with capacity.** Do not allow unbounded orders for the same pickup window.
- **One active order per student per station.**
- **Cancel only before `PREPARING`.**
- **Sold-out items cannot be added to a cart.**
- **Three roles:** `student`, `staff`, `admin`. Staff see only their station. Admin manages menu and stations.
- **Mock payment** is acceptable and expected for the assignment. Persist a payment status (`PENDING | PAID | FAILED`), do not integrate a real acquirer unless the human explicitly asks.
- **Demo auth is enough.** No real SDU SSO.
- **Web-first.** Prefer one web application with role-based routes over three native apps.

---

## 4. Domain vocabulary (use these names)

| Term | Meaning |
|------|---------|
| Station | Physical selling point on campus |
| MenuItem | Product sold today at a station |
| PickupSlot | Bounded time window with a max order count |
| Order | Placed cart with status pipeline |
| Pickup code | Human-readable number plus optional QR payload |
| Staff board | Kitchen/barista list of incoming orders |

Order status **must** follow:

`PLACED → PREPARING → READY → COLLECTED`  
with `CANCELLED` as a terminal exception from `PLACED` only.

Do not rename these statuses in APIs or UI without updating this file.

---

## 5. How the agent should work

### 5.1 Plan before large edits

For any task larger than a trivial copy change:

1. Restate the user-visible outcome in one sentence.
2. List files you expect to touch.
3. Name the smallest vertical slice (UI + data + one happy path).
4. Implement that slice.
5. Verify it (see §7).

Do not generate a full architecture essay and then no running code.

### 5.2 Vertical slices, not layers

Bad: “I created all database tables and empty controllers.”  
Good: “A student can log in, open Main Cafeteria, add plov, pick 12:00–12:10, place an order, and see status PLACED.”

Preferred implementation order:

1. Auth + roles (seed demo users)
2. Stations + menu read
3. Cart + place order + slot capacity
4. Student order tracking
5. Staff status transitions
6. Admin menu availability / sold-out
7. Pickup code display
8. Polish (empty states, validation messages)

### 5.3 When requirements are missing

- Infer the **smallest** behavior consistent with the brainstorm MVP.
- Prefer campus-realistic defaults (KZT prices, 10-minute slots, SDU break-oriented copy).
- Ask the human only if the choice changes architecture (e.g. real payments, native apps, multi-campus).

### 5.4 Code quality bar

- Keep modules aligned with domain terms (`orders`, `stations`, `menu`, `slots`).
- Validate on the server even if the UI already checks.
- Never trust the client for role, price, or capacity.
- Use clear empty and error states: sold out, slot full, unauthorized, order not found.
- Avoid unrelated refactors and extra libraries.
- Comments explain *why* when the rule is a campus constraint, not *what* the code does.

---

## 6. Tech defaults (unless the human overrides)

If the repository is empty and the human asks to implement:

- **Stack:** TypeScript, Next.js (App Router) or equivalent React + API, SQLite or Postgres via an ORM.
- **Styling:** simple, high-contrast, large tap targets (students on phones in a crowd; staff on a counter tablet).
- **Seed data:** SDU-flavored menu (plov, lagman, samsa, coffee, tea) with KZT prices and at least two stations.
- **Demo accounts:**
  - `student@sdu.edu.kz`
  - `staff@sdu.edu.kz`
  - `admin@sdu.edu.kz`
  - shared demo password documented in README

If a stack is already present, **do not rewrite it**. Extend it.

---

## 7. Verification the agent must perform

After a feature slice:

1. Run the project (or tests) and fix failures you introduced.
2. Walk the happy path for the affected role.
3. Walk one failure path (sold out, full slot, wrong role, cancel too late).
4. If the change is UI-visible and a browser is available, click through it; do not rely on a single screenshot.
5. Confirm staff and student views of the **same order** stay consistent.

Do not claim “done” if the student cannot complete a preorder or staff cannot mark it ready.

---

## 8. Security and academic integrity

- No real payment keys, no production Kaspi credentials.
- Do not scrape or copy a commercial food-delivery app’s copyrighted assets.
- Do not store secrets in git.
- This is coursework: keep the solution original to CampusBite / SDU, not a clone of an existing vendor.

---

## 9. Communication with the human

- Speak in the language the student uses (Russian or English).
- Lead with what works now and what is still out of scope.
- When proposing new features, map them to MVP / later using the brainstorm table.
- Update `process.md` checkboxes or a short status note only if asked; do not create extra markdown files unless requested.

---

## 10. Definition of done (assignment-level)

CampusBite is “agent-complete” for INF316 when:

- [ ] Demo users for all three roles can sign in
- [ ] Student can place a capacity-checked pickup order from a seeded menu
- [ ] Staff can move that order to `READY`
- [ ] Student sees `READY` and a pickup code
- [ ] Admin can hide or mark an item sold out and it disappears from new carts
- [ ] README explains how to run and which demo accounts to use

Until those boxes are true, prefer finishing the loop over adding ratings, maps, or visual flair.
