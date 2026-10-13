from django.contrib.auth.models import AbstractUser
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_open = models.BooleanField(default=True)
    opens_at = models.TimeField(default="08:30")
    closes_at = models.TimeField(default="17:00")

    def __str__(self):
        return self.name


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    station = models.ForeignKey(
        Station, null=True, blank=True, on_delete=models.SET_NULL, related_name="staff_members"
    )


class MenuItem(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField(help_text="Price in KZT")
    category = models.CharField(max_length=50)
    available = models.BooleanField(default=True)
    prep_minutes = models.PositiveIntegerField(default=5)
    allergens = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("station", "name")

    def __str__(self):
        return f"{self.name} ({self.station})"


class PickupSlot(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="slots")
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=12)

    class Meta:
        unique_together = ("station", "start_time", "end_time")
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.station} {self.start_time:%H:%M}-{self.end_time:%H:%M}"


class OrderStatus(models.TextChoices):
    PLACED = "PLACED", "Placed"
    PREPARING = "PREPARING", "Preparing"
    READY = "READY", "Ready"
    COLLECTED = "COLLECTED", "Collected"
    CANCELLED = "CANCELLED", "Cancelled"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="orders")
    slot = models.ForeignKey(PickupSlot, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PLACED)
    paid = models.BooleanField(default=False)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.code or self.pk} ({self.status})"


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField()
