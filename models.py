"""Immutable data models for employee onboarding content."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EmployeeForm:
    """Employee details submitted through the onboarding form."""

    name: str
    role: str
    department: str
    start_date: str
    role_other: str = ""
    department_other: str = ""


@dataclass(frozen=True)
class WelcomeEmail:
    """A ready-to-use welcome email subject and body."""

    subject: str
    body: str


@dataclass(frozen=True)
class DayPlan:
    """One themed day in an employee's first-week plan."""

    day: int
    theme: str
    activities: tuple[str, ...]


@dataclass(frozen=True)
class ChecklistItem:
    """A single item in an onboarding checklist."""

    label: str
    details: str = ""


@dataclass(frozen=True)
class FaqItem:
    """A frequently asked onboarding question and its answer."""

    question: str
    answer: str


@dataclass(frozen=True)
class TrainingResource:
    """A training course, document, or reading resource."""

    title: str
    description: str
    category: str


@dataclass(frozen=True)
class OnboardingPack:
    """All generated onboarding materials for one employee."""

    employee: EmployeeForm
    welcome_email: WelcomeEmail
    plan: tuple[DayPlan, ...]
    documents: tuple[ChecklistItem, ...]
    it_access: tuple[ChecklistItem, ...]
    faqs: tuple[FaqItem, ...]
    training_resources: tuple[TrainingResource, ...]
