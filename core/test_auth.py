from django.core.management import call_command
from django.test import TestCase


class AuthTests(TestCase):
    def setUp(self):
        call_command("seed")

    def login_via_form(self, username, password="demo1234"):
        return self.client.post(
            "/login/", {"username": username, "password": password}, follow=True
        )

    def test_login_page_returns_200(self):
        self.assertEqual(self.client.get("/login/").status_code, 200)

    def test_student_lands_on_stations(self):
        response = self.login_via_form("aigerim")
        self.assertEqual(response.redirect_chain[-1][0], "/stations/")
        self.assertEqual(response.status_code, 200)

    def test_staff_lands_on_staff_board(self):
        response = self.login_via_form("nurlan")
        self.assertEqual(response.redirect_chain[-1][0], "/staff/")
        self.assertEqual(response.status_code, 200)

    def test_admin_lands_on_admin_menu(self):
        response = self.login_via_form("dana")
        self.assertEqual(response.redirect_chain[-1][0], "/manage/")
        self.assertEqual(response.status_code, 200)

    def test_wrong_password_shows_error(self):
        response = self.login_via_form("aigerim", "wrong-password")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_student_cannot_open_staff_or_admin_pages(self):
        self.client.login(username="aigerim", password="demo1234")
        self.assertEqual(self.client.get("/staff/").status_code, 403)
        self.assertEqual(self.client.get("/manage/").status_code, 403)

    def test_staff_cannot_open_admin_page(self):
        self.client.login(username="nurlan", password="demo1234")
        self.assertEqual(self.client.get("/manage/").status_code, 403)

    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get("/stations/")
        self.assertRedirects(response, "/login/?next=/stations/")

    def test_logout_then_protected_page_requires_login(self):
        self.client.login(username="aigerim", password="demo1234")
        response = self.client.post("/logout/")
        self.assertRedirects(response, "/login/")
        self.assertEqual(self.client.get("/stations/").status_code, 302)
