from django.core.management.base import BaseCommand

from core.models import MenuItem, PickupSlot, Station, User

DEMO_PASSWORD = "demo1234"

MENU = {
    "Main Cafeteria": [
        ("Plov", 1800, "Hot dishes", True),
        ("Lagman", 1600, "Hot dishes", False),
        ("Set lunch", 2200, "Set meals", True),
        ("Chicken soup", 1200, "Soups", True),
        ("Grilled chicken", 2500, "Grill", True),
        ("Salad", 900, "Salads", True),
        ("Tea", 300, "Drinks", True),
    ],
    "Coffee Point": [
        ("Americano", 800, "Coffee", True),
        ("Latte", 1100, "Coffee", True),
        ("Croissant", 700, "Bakery", True),
    ],
}

SLOTS = [("12:00", "12:10"), ("12:10", "12:20")]


class Command(BaseCommand):
    help = "Seed demo stations, menu, pickup slots and demo users (safe to run twice)."

    def handle(self, *args, **options):
        stations = {}
        for name, items in MENU.items():
            station, _ = Station.objects.get_or_create(name=name)
            stations[name] = station
            for item_name, price, category, available in items:
                MenuItem.objects.update_or_create(
                    station=station,
                    name=item_name,
                    defaults={"price": price, "category": category, "available": available},
                )
            for start, end in SLOTS:
                PickupSlot.objects.get_or_create(
                    station=station, start_time=start, end_time=end, defaults={"capacity": 12}
                )

        users = [
            ("aigerim", User.Role.STUDENT, None),
            ("nurlan", User.Role.STAFF, stations["Main Cafeteria"]),
            ("dana", User.Role.ADMIN, None),
        ]
        for username, role, station in users:
            user, created = User.objects.get_or_create(
                username=username, defaults={"role": role, "station": station}
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()

        self.stdout.write(self.style.SUCCESS("Seed complete."))
