"""Render onboarding data into escaped HTML pages."""

from html import escape
from typing import Mapping

import content
from models import ChecklistItem, EmployeeForm, OnboardingPack


def _esc(value: object) -> str:
    """Escape a value for safe insertion into HTML text or an attribute."""
    return escape(str(value), quote=True)


def _page(title: str, body: str) -> str:
    """Wrap a page body in the shared document structure."""
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{_esc(title)}</title><link rel=\"stylesheet\" href=\"/static/style.css\"></head>"
        f"<body><main class=\"container\">{body}</main></body></html>"
    )


def _select_options(options: tuple[str, ...], selected: str) -> str:
    """Render escaped select options and retain an unknown submitted value."""
    values = list(options)
    unknown = selected and selected not in options and selected != "Other"
    markup = ""
    if unknown:
        markup += f"<option value=\"{_esc(selected)}\" selected>{_esc(selected)}</option>"
    for option in values:
        chosen = " selected" if option == selected else ""
        markup += f"<option value=\"{_esc(option)}\"{chosen}>{_esc(option)}</option>"
    return markup


def render_form(
    employee: EmployeeForm | None,
    errors: Mapping[str, str],
    today: str,
) -> str:
    """Render the employee form, preserving submitted values and errors."""
    name = employee.name if employee else ""
    role = employee.role if employee else content.ROLE_OPTIONS[0]
    role_other = employee.role_other if employee else ""
    department = employee.department if employee else content.DEPARTMENT_OPTIONS[0]
    department_other = employee.department_other if employee else ""
    start_date = employee.start_date if employee else today

    def error(field: str) -> str:
        """Return an escaped field error when one exists."""
        message = errors.get(field)
        return f"<p class=\"error\">{_esc(message)}</p>" if message else ""

    body = (
        "<header class=\"intro\"><p class=\"eyebrow\">People operations</p>"
        "<h1>Employee onboarding</h1><p>Create a personalized welcome email and first-week guide.</p></header>"
        "<form method=\"post\" action=\"/generate\" class=\"employee-form\">"
        "<div class=\"field\"><label for=\"name\">Employee name</label>"
        f"<input id=\"name\" name=\"name\" type=\"text\" required maxlength=\"120\" value=\"{_esc(name)}\">{error('name')}</div>"
        "<div class=\"field\"><label for=\"role\">Role</label>"
        f"<select id=\"role\" name=\"role\">{_select_options(content.ROLE_OPTIONS, role)}</select></div>"
        "<div class=\"field\"><label for=\"role_other\">Role if you selected Other</label>"
        f"<input id=\"role_other\" name=\"role_other\" type=\"text\" maxlength=\"120\" value=\"{_esc(role_other)}\">{error('role_other')}</div>"
        "<div class=\"field\"><label for=\"department\">Department</label>"
        f"<select id=\"department\" name=\"department\">{_select_options(content.DEPARTMENT_OPTIONS, department)}</select></div>"
        "<div class=\"field\"><label for=\"department_other\">Department if you selected Other</label>"
        f"<input id=\"department_other\" name=\"department_other\" type=\"text\" maxlength=\"120\" value=\"{_esc(department_other)}\">{error('department_other')}</div>"
        "<div class=\"field\"><label for=\"start_date\">Start date</label>"
        f"<input id=\"start_date\" name=\"start_date\" type=\"date\" required value=\"{_esc(start_date)}\">{error('start_date')}</div>"
        "<button class=\"primary\" type=\"submit\">Create onboarding pack</button></form>"
    )
    return _page("Employee onboarding", body)


def _checklist(items: tuple[ChecklistItem, ...]) -> str:
    """Render checklist items with escaped labels and descriptions."""
    rows = []
    for item in items:
        label = _esc(item.label)
        details = _esc(item.details)
        rows.append(
            f"<li><label class=\"check-item\"><input type=\"checkbox\">"
            f"<span><strong>{label}</strong><small>{details}</small></span></label></li>"
        )
    return "<ul class=\"checklist\">" + "".join(rows) + "</ul>"


def _download_form(action: str, label: str, employee: EmployeeForm) -> str:
    """Render a small POST form carrying the entered values as hidden fields."""
    fields = (
        ("name", employee.name),
        ("role", employee.role),
        ("role_other", employee.role_other),
        ("department", employee.department),
        ("department_other", employee.department_other),
        ("start_date", employee.start_date),
    )
    hidden = "".join(
        f"<input type=\"hidden\" name=\"{_esc(name)}\" value=\"{_esc(value)}\">"
        for name, value in fields
    )
    return f"<form method=\"post\" action=\"{_esc(action)}\" class=\"download-form\">{hidden}<button type=\"submit\">{_esc(label)}</button></form>"


def render_results(pack: OnboardingPack) -> str:
    """Render all six onboarding sections and their anchor navigation."""
    employee = pack.employee
    name = _esc(employee.name.strip())
    role = _esc(employee.role_other.strip() if employee.role == "Other" else employee.role.strip())
    department = _esc(employee.department_other.strip() if employee.department == "Other" else employee.department.strip())
    start_date = _esc(employee.start_date)
    email = (
        f"<p><strong>Subject:</strong> {_esc(pack.welcome_email.subject)}</p>"
        f"<pre class=\"email-body\">{_esc(pack.welcome_email.body)}</pre>"
    )
    plan_days = []
    for day in pack.plan:
        activities = "".join(f"<li>{_esc(activity)}</li>" for activity in day.activities)
        plan_days.append(
            f"<article class=\"day-card\"><h3>Day {day.day}: {_esc(day.theme)}</h3><ul>{activities}</ul></article>"
        )
    faq_html = "".join(
        f"<details><summary>{_esc(faq.question)}</summary><p>{_esc(faq.answer)}</p></details>"
        for faq in pack.faqs
    )
    training_html = "".join(
        f"<li><strong>{_esc(resource.title)}</strong> <span class=\"tag\">{_esc(resource.category)}</span>"
        f"<p>{_esc(resource.description)}</p></li>"
        for resource in pack.training_resources
    )
    navigation = (
        "<nav class=\"section-nav\" aria-label=\"Onboarding sections\">"
        "<a href=\"#welcome\">Welcome email</a><a href=\"#plan\">7-day plan</a>"
        "<a href=\"#documents\">Documents</a><a href=\"#it-access\">IT access</a>"
        "<a href=\"#faqs\">FAQs</a><a href=\"#training\">Training</a></nav>"
    )
    downloads = (
        "<div class=\"download-actions\">"
        + _download_form("/download/email", "Download welcome email (.txt)", employee)
        + _download_form("/download/pack", "Download full pack (.md)", employee)
        + "</div>"
    )
    body = (
        f"<header class=\"results-header\"><p class=\"eyebrow\">Onboarding pack</p><h1>Welcome, {name}</h1>"
        f"<p>{role} · {department} · Starts {start_date}</p><a href=\"/\">Edit employee details</a></header>"
        f"{navigation}{downloads}"
        f"<section id=\"welcome\"><h2>1. Welcome email</h2>{email}</section>"
        f"<section id=\"plan\"><h2>2. 7-day onboarding plan</h2><div class=\"day-grid\">{''.join(plan_days)}</div></section>"
        f"<section id=\"documents\"><h2>3. Required documents checklist</h2>{_checklist(pack.documents)}</section>"
        f"<section id=\"it-access\"><h2>4. IT access checklist</h2>{_checklist(pack.it_access)}</section>"
        f"<section id=\"faqs\"><h2>5. Frequently asked questions</h2><div class=\"faq-list\">{faq_html}</div></section>"
        f"<section id=\"training\" class=\"last-section\"><h2>6. Training resources</h2><ul class=\"training-list\">{training_html}</ul></section>"
    )
    return _page(f"Onboarding pack for {employee.name.strip()}", body)


def render_error_page(message: str) -> str:
    """Render a small escaped error page for unsupported routes."""
    return _page("Request not found", f"<h1>Request not available</h1><p>{_esc(message)}</p><p><a href=\"/\">Return to the form</a></p>")





