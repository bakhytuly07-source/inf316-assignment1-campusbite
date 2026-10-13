from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render


def role_required(role):
    """Allow only logged-in users with the given role; others get 403."""

    def decorator(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapper

    return decorator


def home(request):
    return render(request, "core/home.html")


@login_required
def after_login(request):
    destinations = {"student": "stations", "staff": "staff_board", "admin": "admin_menu"}
    return redirect(destinations.get(request.user.role, "home"))


@role_required("student")
def stations(request):
    return render(
        request,
        "core/placeholder.html",
        {"title": "Stations", "message": "Stations and today's menu will appear here."},
    )


@role_required("staff")
def staff_board(request):
    return render(
        request,
        "core/placeholder.html",
        {"title": "Staff board", "message": "Incoming orders for your station will appear here."},
    )


@role_required("admin")
def admin_menu(request):
    return render(
        request,
        "core/placeholder.html",
        {"title": "Admin menu", "message": "Menu and station management will appear here."},
    )
