# CampusBite — Brainstorm Chat History

**Course:** INF316 — AI-Native Development  
**Project:** CampusBite  
**Campus:** Suleyman Demirel University (SDU), Kaskelen  
**Participants:** Жақсылық (student / product owner), AI assistant (brainstorm partner)  
**Format:** reconstructed design conversation used as the seed for AI-native development artifacts (`AGENT.md`, `process.md`, `roles/pm.md`)

---

## Session 1 — Problem discovery

**Student:** I want to build something useful for SDU, not a generic todo app. Every day between lectures the cafeteria and coffee corners turn into a traffic jam. I lose 15–20 minutes of a 20-minute break just standing in line.

**AI:** That is a strong campus problem. Who is waiting, and what are they waiting for?

**Student:** Mostly bachelor students between 11:40 and 13:30. There is one main dining hall plus smaller coffee points. People first queue to choose food, then queue again to pay, then wait for the order if it is cooked to order. Coffee lines are even worse right before seminars.

**AI:** So the bottleneck is not only cooking. It is decision + payment + pickup colliding in the same physical space during a short break.

**Student:** Exactly. If I already knew the menu, prepaid, and only came to grab a numbered order, I could eat and still make it to class.

---

## Session 2 — Who suffers and who would use it

**Student:** Primary users are students. Secondary: cafeteria staff who take orders and prepare food. Admins of the dining service need a way to update the menu and pause items that ran out.

**AI:** Any constraints unique to SDU?

**Student:** Yes:

- Breaks are short and the schedule is dense.
- Many students pay with Kaspi / card, some still cash — but the app should not force cash.
- Menu changes daily; some items sell out before 13:00.
- Not everyone has perfect campus Wi-Fi, so the order flow must be simple and recoverable.
- Pickup must work without shouting names over a noisy hall — order number + status is better.
- Language: students mix Kazakh, Russian, and English. UI should be simple English first, with room for later localization.

**AI:** Non-goals would help too. What should CampusBite *not* become in v1?

**Student:** Not a full social network. Not a grocery marketplace. Not a delivery-to-dorm service. Not a loyalty-points casino. v1 is: see today’s menu, preorder, pay, pick up, skip the decision queue.

---

## Session 3 — Core product idea

**Working name:** CampusBite — preorder food from the SDU cafeteria and campus coffee points so you do not spend the whole break in line.

**One-sentence pitch:** CampusBite lets SDU students browse today’s campus menu, place a pickup order before the break, and collect it when the status says ready.

**Success metric for a typical user:** time from entering the dining area to holding food drops from ~15 minutes to under 3 minutes.

---

## Session 4 — Feature brainstorm (divergent)

Ideas that came up, including ones we later cut:

| Idea | Keep for v1? | Notes |
|------|----------------|-------|
| Daily menu with prices, photos, allergens | Yes | Foundation of the product |
| Filter by cafe / station (main hall, coffee, bakery) | Yes | SDU has more than one point |
| Estimated prep time / “ready in ~8 min” | Yes (simple) | Can be a static estimate per category at first |
| Preorder with pickup slot (e.g. 12:10–12:20) | Yes | Aligns with lecture timetable |
| In-app payment (Kaspi / card mock in prototype) | Partial | Real Kaspi later; v1 can use mock checkout + “paid” flag |
| Order status: placed → preparing → ready → collected | Yes | Replaces shouting names |
| Push / in-app notification when ready | Nice-to-have | Can be polling in prototype |
| QR code at pickup counter | Yes | Staff scans or student shows code |
| Sold-out flag from kitchen | Yes | Prevents ordering empty dishes |
| Ratings and comments | Later | Risk of noise; not needed to skip queues |
| Group order for friends | Later | Useful, but complicates payment |
| Calorie tracking / diet plans | No for v1 | Scope creep |
| Live map of queue length | Later | Needs sensors or unreliable self-report |
| Student ID / campus login | Yes (simplified) | Email or student ID + password is enough for assignment |
| Staff dashboard: incoming orders | Yes | Without this, preorder is theater |
| Admin: menu CRUD, open/close station | Yes | Daily operations |
| Dark theme, animations, gamification | No | Polish after the loop works |

---

## Session 5 — User journeys we agreed on

### Journey A — Student on a busy Tuesday

1. At 11:20, still in lecture, the student opens CampusBite.
2. Selects **Main Cafeteria**.
3. Sees today’s set lunch, soups, and grill; “Lagman” is marked sold out.
4. Adds plov + salad + tea, chooses pickup window **12:00–12:10** (right after lecture).
5. Confirms mock payment.
6. Receives order `#CB-1042` with status **Preparing**.
7. Walks in at 12:03, sees **Ready**, shows QR / number at the pickup desk.
8. Leaves. Did not stand in the choosing-and-paying queue.

### Journey B — Barista at the coffee point

1. Staff opens the **Kitchen / Station** view.
2. New orders appear in time order.
3. Staff taps **Start** then **Ready**.
4. If oat milk is gone, staff marks that modifier sold out so new orders cannot include it.

### Journey C — Dining admin in the morning

1. Uploads or edits today’s menu before 08:30.
2. Sets each station Open.
3. At 14:00 marks the grill station Closed.

---

## Session 6 — Information architecture (v1 screens)

**Student app**

- Home: stations + “order again”
- Menu: categories, item detail, add to cart
- Cart + pickup slot + pay
- Order tracking
- Profile / student ID

**Staff app (can be a separate route in the same web app)**

- Live order list
- Order detail + status buttons
- Sold-out toggles

**Admin**

- Stations
- Menu items
- Simple daily report: orders count, popular items, missed pickups

---

## Session 7 — Domain model sketch

Entities we expect in the first implementation:

- `User` (role: student | staff | admin)
- `Station` (cafeteria, coffee, bakery)
- `MenuItem` (name, price, category, available, prepMinutes, allergens)
- `Cart` / `Order` / `OrderLine`
- `PickupSlot`
- `Payment` (status only in v1)
- `OrderStatus` enum: `PLACED | PREPARING | READY | COLLECTED | CANCELLED`

Business rules:

- Cannot add a sold-out item.
- Pickup slot must be in the station’s working hours.
- Student can have at most one active (non-collected, non-cancelled) order per station.
- Staff can only see orders for their assigned station.
- Cancel allowed until status is `PREPARING`.

---

## Session 8 — Risks and open questions

1. **Kitchen load:** if everyone preorders for 12:05, we recreate the queue in the kitchen. Mitigation: capped slots (e.g. 12 orders per 10-minute window).
2. **No-shows:** food wasted. Mitigation: cancel window + mark no-show; later a strike policy.
3. **Payments:** university assignment may use simulated payment. Production would need Kaspi / acquiring and refunds.
4. **Trust of staff:** if the tablet is slow, they will ignore it. Staff UI must be huge buttons, few fields.
5. **Menu freshness:** wrong prices destroy trust. Admin must be able to patch an item in under a minute.
6. **Identity:** we will not integrate real SDU SSO in this assignment; a demo login is enough.

---

## Session 9 — MVP scope freeze

**In MVP**

- Auth with three roles
- Stations + daily menu
- Cart, pickup slot, place order
- Status pipeline and pickup code
- Staff board
- Admin menu management
- Slot capacity to protect the kitchen

**Out of MVP**

- Real Kaspi payments
- Push notifications
- Ratings, chat, group orders
- Analytics beyond a simple counter
- Native iOS/Android (web-first is enough)
- Multilingual UI (English copy, structure ready for i18n)

---

## Session 10 — Why this fits AI-native development

We will not specify every pixel up front. Instead we capture:

- the problem and constraints (this file)
- agent operating rules (`AGENT.md`)
- a repeatable AI-native process (`process.md`)
- a Product Manager role card (`roles/pm.md`)

The agent should implement against these documents, propose small vertical slices, and keep the “skip the SDU break queue” outcome as the north star.

---

## Decisions log

| ID | Decision | Rationale |
|----|----------|-----------|
| D1 | Pickup, not delivery | Campus is compact; the pain is the line, not distance |
| D2 | Time slots with capacity | Protects kitchen from a 12:00 stampede |
| D3 | Web app first | Fastest path for an INF316 assignment; phones still work in browser |
| D4 | Mock payments in v1 | Real acquiring is out of assignment scope |
| D5 | Order number + QR | Works in a noisy dining hall |
| D6 | Three roles in one product | Students, kitchen, admin must close the loop |
| D7 | English UI for the prototype | Matches course artifacts; localization later |

---

## Next artifacts

After this brainstorm, generate and maintain:

1. `AGENT.md` — how an AI agent must work on CampusBite  
2. `process.md` — AI-native delivery steps for this service  
3. `roles/pm.md` — Product Manager instructions aligned with the MVP freeze  
