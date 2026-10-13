from django.core.management import call_command
from django.test import TestCase

from core.models import MenuItem, OrderStatus, PickupSlot, Station, User


class SeedTests(TestCase):
    def setUp(self):
        call_command("seed")

    def test_stations_created(self):
        self.assertEqual(
            set(Station.objects.values_list("name", flat=True)),
            {"Main Cafeteria", "Coffee Point"},
        )

    def test_menu_has_enough_items_and_lagman_sold_out(self):
        self.assertGreaterEqual(MenuItem.objects.count(), 6)
        self.assertFalse(MenuItem.objects.get(name="Lagman").available)

    def test_slots_created(self):
        main = Station.objects.get(name="Main Cafeteria")
        self.assertEqual(PickupSlot.objects.filter(station=main).count(), 2)
        self.assertTrue(
            PickupSlot.objects.filter(station=main, start_time="12:00", end_time="12:10").exists()
        )

    def test_demo_users_and_roles(self):
        self.assertEqual(User.objects.get(username="aigerim").role, "student")
        nurlan = User.objects.get(username="nurlan")
        self.assertEqual(nurlan.role, "staff")
        self.assertEqual(nurlan.station.name, "Main Cafeteria")
        self.assertEqual(User.objects.get(username="dana").role, "admin")
        self.assertTrue(User.objects.get(username="aigerim").check_password("demo1234"))

    def test_seed_twice_does_not_duplicate(self):
        counts = (
            Station.objects.count(),
            MenuItem.objects.count(),
            PickupSlot.objects.count(),
            User.objects.count(),
        )
        call_command("seed")
        self.assertEqual(
            counts,
            (
                Station.objects.count(),
                MenuItem.objects.count(),
                PickupSlot.objects.count(),
                User.objects.count(),
            ),
        )


class OrderStatusTests(TestCase):
    def test_status_values(self):
        self.assertEqual(
            [s.value for s in OrderStatus],
            ["PLACED", "PREPARING", "READY", "COLLECTED", "CANCELLED"],
        )
