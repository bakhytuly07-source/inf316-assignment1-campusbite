#!/usr/bin/env bash
# Usage: run inside your cloned repo after `gh auth login`:  bash create_issues.sh
set -e
LAST=$(gh issue list --state all --limit 1 --json number -q '.[0].number')
LAST=${LAST:-0}
N() { echo $((LAST + $1)); }   # task number -> issue number (issues are created in order)

mk() { gh issue create --title "$1" --body "$2"; sleep 1; }

mk "Bootstrap empty Django project with a passing test" "## Goal

An empty Django project runs locally and the test suite passes, so every later task starts from a green baseline.

## Acceptance criteria

- [ ] python manage.py runserver starts and the home page returns HTTP 200
- [ ] python manage.py test runs and passes with at least one test
- [ ] requirements.txt lists all dependencies
- [ ] .gitignore excludes db.sqlite3 and virtualenv

## Out of scope

- Any models or business logic (see #$(N 2))
- Styling and templates beyond a plain home page

## Constraints

- Django + SQLite only; no extra dependencies without asking
- Follow AGENT.md"

mk "Domain models and seed data (User roles, Station, MenuItem, PickupSlot, Order)" "## Goal

The data model from the brainstorm exists and a seed command fills a demo campus: 2 stations, a daily menu, slots, and three demo users.

## Acceptance criteria

- [ ] Models exist: User role (student|staff|admin), Station, MenuItem (name, price in KZT, category, available, prepMinutes), PickupSlot (station, start, end, capacity), Order, OrderLine
- [ ] OrderStatus values are PLACED, PREPARING, READY, COLLECTED, CANCELLED
- [ ] python manage.py seed creates Main Cafeteria and Coffee Point, at least 6 menu items (Lagman marked sold out), slots 12:00-12:10 and 12:10-12:20
- [ ] Seed creates accounts: aigerim (student), nurlan (staff, Main Cafeteria), dana (admin)
- [ ] Running seed twice does not duplicate data
- [ ] Model tests pass

## Out of scope

- Views and UI (see #$(N 3), #$(N 4))
- Payment model beyond a status field (decision D4)

## Constraints

- Prices are integers in KZT
- Staff user is linked to exactly one station
- Follow AGENT.md and chat-brainstorm.md session 7"

mk "Demo login with three roles and role-based redirect" "## Goal

Aigerim, Nurlan and Dana can log in and land on the correct screen for their role.

## Acceptance criteria

- [ ] Login page accepts username and password for seeded users
- [ ] Student lands on the stations page, staff on the staff board, admin on the admin menu page
- [ ] Wrong password shows a visible error
- [ ] A student opening a staff or admin URL gets a 403 or redirect
- [ ] Logout works and protected pages require login

## Out of scope

- SDU SSO, registration, password reset (decision: demo login only)
- The pages themselves (see #$(N 4), #$(N 9), #$(N 11))

## Constraints

- Use Django built-in auth
- Follow AGENT.md"

mk "Student sees stations and today's menu" "## Goal

Aigerim sees open stations and the day's menu with prices, categories and sold-out honesty.

## Acceptance criteria

- [ ] Stations page lists all stations with Open or Closed status
- [ ] Station menu page lists items grouped by category with price in KZT
- [ ] Sold-out items are visibly marked and have no add button
- [ ] A closed station shows a message and cannot be ordered from
- [ ] Page loads from seed data after refresh

## Out of scope

- Photos, allergens filters, ratings (see #$(N 13) for polish)
- Cart behaviour (see #$(N 5))

## Constraints

- Server-rendered templates; mobile-friendly layout
- English copy"

mk "Cart: add and remove items" "## Goal

Aigerim can build a cart from one station's menu before choosing a slot.

## Acceptance criteria

- [ ] Add an available item increases quantity and cart total
- [ ] Remove or decrease an item updates the total
- [ ] A sold-out item cannot be added even by posting directly to the URL
- [ ] Cart holds items from one station only; adding from another station asks to clear the cart
- [ ] Cart survives page refresh

## Out of scope

- Slot selection (see #$(N 6))
- Payment (see #$(N 7))

## Constraints

- Session-based cart
- Business rule: cannot add a sold-out item (brainstorm session 7)"

mk "Pickup slots with capacity" "## Goal

The student chooses a pickup slot, and full slots are blocked to protect the kitchen.

## Acceptance criteria

- [ ] Cart page lists slots for the station with remaining capacity
- [ ] A slot with zero remaining capacity is disabled with a clear message
- [ ] Slots outside station working hours are not offered
- [ ] Remaining count is computed from non-cancelled orders in that slot

## Out of scope

- Placing the order (see #$(N 7))
- Dynamic capacity tuning or analytics

## Constraints

- Default capacity 12 per 10-minute slot (decision D2)"

mk "Place order with mock payment and pickup code" "## Goal

Aigerim confirms a mock payment and receives order PLACED with a pickup code.

## Acceptance criteria

- [ ] Confirm payment creates an Order with status PLACED and paid flag true
- [ ] A pickup code like CB-1042 is shown and also encoded as a QR image
- [ ] The chosen slot remaining count decreases by one
- [ ] If the slot became full or an item became sold out meanwhile, the order is rejected with a clear message
- [ ] A student cannot have two active orders at the same station
- [ ] Order is visible after refresh

## Out of scope

- Real Kaspi or card acquiring (decision D4)
- Notifications (see #$(N 8) for status page)

## Constraints

- Order creation must be atomic (check capacity and create in one transaction)
- Follow chat-brainstorm.md session 7 business rules"

mk "Student order tracking page" "## Goal

Aigerim sees her order status and pickup code without asking the kitchen.

## Acceptance criteria

- [ ] My order page shows code, station, slot, items, total and current status
- [ ] Status updates on refresh or with simple polling every 10 seconds
- [ ] READY status is visually prominent
- [ ] A student cannot open another student's order

## Out of scope

- Push notifications (post-MVP)
- Order history analytics

## Constraints

- Polling only, no websockets"

mk "Staff board: orders for my station" "## Goal

Nurlan sees incoming orders for his own station sorted by pickup time.

## Acceptance criteria

- [ ] Board lists PLACED and PREPARING orders sorted by slot start time
- [ ] Each card shows code, items and slot
- [ ] Staff sees only orders of the assigned station
- [ ] Empty state message when there are no orders
- [ ] Buttons are large and usable on a tablet

## Out of scope

- Status changes (see #$(N 10))
- Reports

## Constraints

- No typing required on the board"

mk "Staff status transitions PLACED to PREPARING to READY to COLLECTED" "## Goal

Nurlan moves an order through the pipeline and Aigerim's screen reflects it.

## Acceptance criteria

- [ ] Start moves PLACED to PREPARING; Ready moves PREPARING to READY; Collected moves READY to COLLECTED
- [ ] Invalid jumps (for example PLACED to READY) are rejected
- [ ] The student's tracking page shows the new status
- [ ] Staff cannot change orders of another station

## Out of scope

- Cancellation (see #$(N 12))
- No-show strike policy (post-MVP)

## Constraints

- Transition rules enforced on the server, not only by hiding buttons"

mk "Admin: menu management and sold-out toggle" "## Goal

Dana can fix the menu in under a minute and stop selling items that ran out.

## Acceptance criteria

- [ ] Admin can create, edit and delete a menu item (name, price, category)
- [ ] Admin can toggle available on and off from the list
- [ ] Admin can set a station Open or Closed
- [ ] A toggled-off item immediately disappears from ordering for students
- [ ] Non-admin users cannot access these pages

## Out of scope

- Bulk menu upload, photos
- Daily report with order counts (post-MVP, P2; will be filed as a follow-up issue)

## Constraints

- Prefer custom simple pages over Django admin for the demo"

mk "Student cancels an order while PLACED" "## Goal

Aigerim can cancel before the kitchen starts, freeing the slot.

## Acceptance criteria

- [ ] Cancel button appears only while status is PLACED
- [ ] Cancel sets status CANCELLED and increases slot remaining count
- [ ] After PREPARING the cancel attempt is rejected with a clear message
- [ ] Cancelled orders disappear from the staff board

## Out of scope

- Refunds (payment is mocked)
- No-show handling

## Constraints

- Rule: cancel allowed only until PREPARING (decision from brainstorm session 7)"

mk "Clear empty and error states" "## Goal

The demo survives reviewer mistakes with readable messages instead of crashes.

## Acceptance criteria

- [ ] Empty cart, no slots, closed station, full slot and sold-out item each show a clear message
- [ ] 403 and 404 pages are friendly and include a link home
- [ ] No unhandled server error on any path covered by earlier acceptance criteria

## Out of scope

- Visual redesign, animations, dark theme
- Translations (decision D7)

## Constraints

- English copy only"

mk "README, seed accounts and demo script" "## Goal

A reviewer can clone, run and demo the full loop in five minutes.

## Acceptance criteria

- [ ] README explains setup (install, migrate, seed, runserver, test)
- [ ] README lists the seeded accounts and passwords for aigerim, nurlan and dana
- [ ] README contains a demo script: order, staff moves status, student sees READY, admin marks item sold out
- [ ] A fresh clone follows README and works

## Out of scope

- Deployment and CI/CD
- Simple admin counts report (post-MVP, P2)

## Constraints

- Keep README under 100 lines"

echo "Done. Issues created: $(gh issue list --state open --json number -q length)"
