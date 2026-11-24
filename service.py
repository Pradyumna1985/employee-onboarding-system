"""Generate rule-based employee onboarding materials."""

from datetime import date

try:
    from . import content
    from .models import (
        ChecklistItem,
        DayPlan,
        EmployeeForm,
        FaqItem,
        OnboardingPack,
        TrainingResource,
        WelcomeEmail,
    )
except ImportError:
    import content
    from models import ChecklistItem, DayPlan, EmployeeForm, FaqItem, OnboardingPack, TrainingResource, WelcomeEmail


def _employee_role(employee: EmployeeForm) -> str:
    """Return the entered role, resolving the Other field when selected."""
    if employee.role == "Other":
        return employee.role_other.strip()
    return employee.role.strip()


def _employee_department(employee: EmployeeForm) -> str:
    """Return the entered department, resolving the Other field when selected."""
    if employee.department == "Other":
        return employee.department_other.strip()
    return employee.department.strip()


def _display_date(start_date: str) -> str:
    """Format an ISO date for display while keeping invalid input readable."""
    try:
        parsed = date.fromisoformat(start_date)
    except ValueError:
        return start_date
    return parsed.strftime("%B %d, %Y").replace(" 0", " ")


def validate_employee_form(employee: EmployeeForm) -> dict[str, str]:
    """Return field-specific validation messages for an employee form."""
    errors: dict[str, str] = {}
    if not employee.name.strip():
        errors["name"] = "Please enter the employee's name."
    if employee.role == "Other" and not employee.role_other.strip():
        errors["role_other"] = "Please enter the employee's role."
    if employee.department == "Other" and not employee.department_other.strip():
        errors["department_other"] = "Please enter the employee's department."
    try:
        date.fromisoformat(employee.start_date)
    except ValueError:
        errors["start_date"] = "Please choose a valid start date."
    return errors


def generate_welcome_email(employee: EmployeeForm) -> WelcomeEmail:
    """Create a personalized welcome email for an employee."""
    name = employee.name.strip()
    role = _employee_role(employee) or content.DEFAULT_ROLE
    department = _employee_department(employee) or content.DEFAULT_DEPARTMENT
    start_date = _display_date(employee.start_date)
    subject = f"Welcome to the team, {name}!"
    body = (
        f"Hi {name},\n\n"
        f"Welcome to the team! We are excited for you to join us as a {role} "
        f"in {department}, starting on {start_date}. Your manager will help you "
        "get settled, meet your teammates, and work through your first-week plan.\n\n"
        "Please bring any questions to your manager or onboarding buddy. We look forward to working with you!\n\n"
        "Welcome aboard,\nThe People Team"
    )
    return WelcomeEmail(subject=subject, body=body)


def generate_onboarding_plan(employee: EmployeeForm) -> tuple[DayPlan, ...]:
    """Build a seven-day onboarding plan tailored to role and department."""
    role = _employee_role(employee) or content.DEFAULT_ROLE
    department = _employee_department(employee) or content.DEFAULT_DEPARTMENT
    department_activities = content.DEPARTMENT_PLAN_ACTIVITIES.get(
        department, content.DEFAULT_DEPARTMENT_PLAN_ACTIVITIES
    )
    role_activities = content.ROLE_PLAN_ACTIVITIES.get(
        role, content.DEFAULT_ROLE_PLAN_ACTIVITIES
    )
    return tuple(
        DayPlan(
            day=index + 1,
            theme=content.DAY_THEMES[index],
            activities=department_activities[index] + (role_activities[index],),
        )
        for index in range(7)
    )


def generate_document_checklist(employee: EmployeeForm) -> tuple[ChecklistItem, ...]:
    """Return the standard required-document checklist."""
    return content.DEFAULT_DOCUMENTS


def generate_it_access_checklist(employee: EmployeeForm) -> tuple[ChecklistItem, ...]:
    """Return baseline and department-specific IT access items."""
    department = _employee_department(employee) or content.DEFAULT_DEPARTMENT
    department_items = content.DEPARTMENT_IT_ACCESS.get(
        department, content.DEFAULT_DEPARTMENT_IT_ACCESS
    )
    return content.BASELINE_IT_ACCESS + department_items


def generate_faqs(employee: EmployeeForm) -> tuple[FaqItem, ...]:
    """Return seven general FAQs plus role- and department-specific answers."""
    role = _employee_role(employee) or content.DEFAULT_ROLE
    department = _employee_department(employee) or content.DEFAULT_DEPARTMENT
    department_faq = content.DEPARTMENT_FAQS.get(department, content.DEFAULT_DEPARTMENT_FAQ)
    role_faq = content.ROLE_FAQS.get(role, content.DEFAULT_ROLE_FAQ)
    return content.DEFAULT_FAQS + (department_faq, role_faq)


def generate_training_resources(employee: EmployeeForm) -> tuple[TrainingResource, ...]:
    """Return role learning resources and compulsory training."""
    role = _employee_role(employee) or content.DEFAULT_ROLE
    role_resources = content.ROLE_TRAINING.get(role, content.DEFAULT_ROLE_TRAINING)
    return role_resources + content.COMPULSORY_TRAINING


def generate_onboarding_pack(employee: EmployeeForm) -> OnboardingPack:
    """Generate every onboarding section as an immutable data pack."""
    return OnboardingPack(
        employee=employee,
        welcome_email=generate_welcome_email(employee),
        plan=generate_onboarding_plan(employee),
        documents=generate_document_checklist(employee),
        it_access=generate_it_access_checklist(employee),
        faqs=generate_faqs(employee),
        training_resources=generate_training_resources(employee),
    )


def build_markdown_pack(pack: OnboardingPack) -> str:
    """Render an onboarding pack as a Markdown document."""
    employee = pack.employee
    role = _employee_role(employee) or content.DEFAULT_ROLE
    department = _employee_department(employee) or content.DEFAULT_DEPARTMENT
    lines = [
        f"# Onboarding pack: {employee.name.strip()}",
        "",
        f"**Role:** {role}  ",
        f"**Department:** {department}  ",
        f"**Start date:** {_display_date(employee.start_date)}",
        "",
        "## 1. Welcome email",
        "",
        f"**Subject:** {pack.welcome_email.subject}",
        "",
        pack.welcome_email.body,
        "",
        "## 2. Seven-day onboarding plan",
        "",
    ]
    for day in pack.plan:
        lines.extend((f"### Day {day.day}: {day.theme}", ""))
        lines.extend(f"- {activity}" for activity in day.activities)
        lines.append("")
    lines.extend(("## 3. Required documents checklist", ""))
    lines.extend(f"- [ ] {item.label} — {item.details}" for item in pack.documents)
    lines.extend(("", "## 4. IT access checklist", ""))
    lines.extend(f"- [ ] {item.label} — {item.details}" for item in pack.it_access)
    lines.extend(("", "## 5. Frequently asked questions", ""))
    for faq in pack.faqs:
        lines.extend((f"### {faq.question}", "", faq.answer, ""))
    lines.extend(("## 6. Training resources", ""))
    lines.extend(
        f"- **{resource.category}: {resource.title}.** {resource.description}"
        for resource in pack.training_resources
    )
    lines.append("")
    return "\n".join(lines)
