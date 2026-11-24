"""HTTP routing for the employee onboarding application."""

from datetime import date
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Mapping
from urllib.parse import parse_qs, urlsplit

try:
    from .models import EmployeeForm
    from .service import build_markdown_pack, generate_onboarding_pack, generate_welcome_email, validate_employee_form
    from .views import render_error_page, render_form, render_results
except ImportError:
    from models import EmployeeForm
    from service import build_markdown_pack, generate_onboarding_pack, generate_welcome_email, validate_employee_form
    from views import render_error_page, render_form, render_results


class OnboardingRequestHandler(BaseHTTPRequestHandler):
    """Route onboarding requests to the service and HTML views."""

    def __init__(self, *args: object, static_dir: Path | None = None, **kwargs: object) -> None:
        self.static_dir = static_dir or Path(__file__).resolve().parent / "static"
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        """Serve the form or the stylesheet for a GET request."""
        path = urlsplit(self.path).path
        if path == "/":
            self._send_html(render_form(None, {}, date.today().isoformat()))
        elif path == "/static/style.css":
            self._send_static_css()
        else:
            self._send_html(render_error_page("The requested page could not be found."), status=404)

    def do_POST(self) -> None:
        """Route form generation and file download requests."""
        path = urlsplit(self.path).path
        form = self._read_form()
        employee = _employee_from_values(form)
        if path not in ("/generate", "/download/email", "/download/pack"):
            self._send_html(render_error_page("The requested action could not be found."), status=404)
            return

        errors = validate_employee_form(employee)
        if errors:
            self._send_html(render_form(employee, errors, date.today().isoformat()), status=400)
            return

        if path == "/generate":
            pack = generate_onboarding_pack(employee)
            self._send_html(render_results(pack))
            return
        if path == "/download/email":
            welcome = generate_welcome_email(employee)
            self._send_attachment(
                "welcome-email.txt",
                f"Subject: {welcome.subject}\n\n{welcome.body}\n",
                "text/plain; charset=utf-8",
            )
            return
        self._send_attachment(
            "onboarding-pack.md",
            build_markdown_pack(generate_onboarding_pack(employee)),
            "text/markdown; charset=utf-8",
        )

    def _read_form(self) -> dict[str, str]:
        """Read URL-encoded form values from the request body."""
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        raw = self.rfile.read(max(0, min(length, 1_000_000))).decode("utf-8", errors="replace")
        parsed = parse_qs(raw, keep_blank_values=True)
        return {key: values[0] if values else "" for key, values in parsed.items()}

    def _send_html(self, page: str, status: int = 200) -> None:
        """Send a UTF-8 HTML response."""
        payload = page.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_attachment(self, filename: str, body: str, content_type: str) -> None:
        """Send generated text as a downloadable attachment."""
        payload = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_static_css(self) -> None:
        """Serve the local stylesheet when it is available."""
        stylesheet = self.static_dir / "style.css"
        try:
            payload = stylesheet.read_bytes()
        except OSError:
            self._send_html(render_error_page("The stylesheet could not be found."), status=404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/css; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def _employee_from_values(values: Mapping[str, str]) -> EmployeeForm:
    """Build an immutable employee form from decoded request fields."""
    return EmployeeForm(
        name=values.get("name", ""),
        role=values.get("role", ""),
        department=values.get("department", ""),
        start_date=values.get("start_date", ""),
        role_other=values.get("role_other", ""),
        department_other=values.get("department_other", ""),
    )


def make_server(host: str, port: int, static_dir: Path | None = None) -> ThreadingHTTPServer:
    """Create a threaded HTTP server for the requested host and port."""
    handler = partial(OnboardingRequestHandler, static_dir=static_dir)
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    return server
