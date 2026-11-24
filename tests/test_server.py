"""HTTP route tests using a background local server and urllib."""

import socket
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from onboarding.server import make_server
except ImportError:
    from server import make_server


class OnboardingServerTests(unittest.TestCase):
    """Exercise the form, validation, result page, and downloads over HTTP."""

    def setUp(self) -> None:
        """Start a test server on an available loopback port."""
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        static_dir = Path(__file__).resolve().parents[1] / "static"
        self.server = make_server("127.0.0.1", port, static_dir)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self) -> None:
        """Stop and close the test server."""
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def post(self, path: str, values: dict[str, str]):
        """Send a URL-encoded form and return the HTTP response."""
        request = Request(
            self.base_url + path,
            data=urlencode(values).encode("utf-8"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        return urlopen(request, timeout=3)

    def employee_values(self) -> dict[str, str]:
        """Return valid form values for a representative new hire."""
        return {
            "name": "Taylor Reed",
            "role": "Software Engineer",
            "role_other": "",
            "department": "Engineering",
            "department_other": "",
            "start_date": "2026-12-01",
        }

    def test_form_results_validation_and_downloads(self) -> None:
        """Verify all required page headings, errors, and attachment responses."""
        with urlopen(self.base_url + "/", timeout=3) as response:
            form_html = response.read().decode("utf-8")
        self.assertIn("Employee onboarding", form_html)
        self.assertIn('name="start_date"', form_html)
        self.assertIn("type=\"date\"", form_html)

        with self.post("/generate", self.employee_values()) as response:
            result_html = response.read().decode("utf-8")
        for heading in (
            "1. Welcome email", "2. 7-day onboarding plan", "3. Required documents checklist",
            "4. IT access checklist", "5. Frequently asked questions", "6. Training resources",
        ):
            self.assertIn(heading, result_html)
        self.assertIn("Taylor Reed", result_html)

        empty_name = self.employee_values()
        empty_name["name"] = ""
        with self.assertRaises(HTTPError) as name_error:
            self.post("/generate", empty_name)
        self.assertEqual(name_error.exception.code, 400)
        self.assertIn("Please enter the employee&#x27;s name.", name_error.exception.read().decode("utf-8"))

        empty_other = self.employee_values()
        empty_other.update({"role": "Other", "role_other": "", "department": "Other", "department_other": ""})
        with self.assertRaises(HTTPError) as other_error:
            self.post("/generate", empty_other)
        other_html = other_error.exception.read().decode("utf-8")
        self.assertIn("Please enter the employee&#x27;s role.", other_html)
        self.assertIn("Please enter the employee&#x27;s department.", other_html)

        with self.post("/download/email", self.employee_values()) as response:
            email = response.read().decode("utf-8")
            self.assertIn("attachment; filename=\"welcome-email.txt\"", response.headers.get("Content-Disposition", ""))
        self.assertIn("Subject: Welcome to the team, Taylor Reed!", email)

        with self.post("/download/pack", self.employee_values()) as response:
            markdown = response.read().decode("utf-8")
            self.assertIn("attachment; filename=\"onboarding-pack.md\"", response.headers.get("Content-Disposition", ""))
        self.assertIn("# Onboarding pack: Taylor Reed", markdown)


if __name__ == "__main__":
    unittest.main()
