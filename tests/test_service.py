"""Tests for generated onboarding materials."""

import unittest

from models import EmployeeForm
from service import (
    generate_document_checklist,
    generate_faqs,
    generate_it_access_checklist,
    generate_onboarding_plan,
    generate_training_resources,
    generate_welcome_email,
)

class OnboardingServiceTests(unittest.TestCase):
    """Check section content, personalization, and fallback behavior."""

    def assert_complete_pack(self, employee: EmployeeForm, expected_role: str, expected_department: str) -> None:
        """Assert the required section counts and personalization for one employee."""
        welcome = generate_welcome_email(employee)
        plan = generate_onboarding_plan(employee)
        documents = generate_document_checklist(employee)
        it_access = generate_it_access_checklist(employee)
        faqs = generate_faqs(employee)
        training = generate_training_resources(employee)

        self.assertIn(employee.name, welcome.subject)
        self.assertIn(employee.name, welcome.body)
        self.assertIn(expected_role, welcome.body)
        self.assertIn(expected_department, welcome.body)
        self.assertEqual(len(plan), 7)
        self.assertEqual([day.day for day in plan], list(range(1, 8)))
        self.assertTrue(all(day.theme and 3 <= len(day.activities) <= 5 for day in plan))
        self.assertTrue(documents)
        self.assertTrue(it_access)
        self.assertTrue(8 <= len(faqs) <= 10)
        self.assertTrue(training)
        self.assertTrue(all(resource.title and resource.description for resource in training))

    def test_engineer_in_engineering(self) -> None:
        """Generate complete materials for an engineering hire."""
        employee = EmployeeForm("Avery Chen", "Software Engineer", "Engineering", "2026-12-01")
        self.assert_complete_pack(employee, "Software Engineer", "Engineering")
        self.assertIn("GitHub", {item.label for item in generate_it_access_checklist(employee)})
        self.assertIn("Development workflow guide", {item.title for item in generate_training_resources(employee)})

    def test_accountant_in_finance(self) -> None:
        """Generate complete materials for a finance hire."""
        employee = EmployeeForm("Jordan Patel", "Accountant", "Finance", "2026-12-08")
        self.assert_complete_pack(employee, "Accountant", "Finance")
        self.assertIn("ERP", {item.label for item in generate_it_access_checklist(employee)})
        self.assertIn("Accounting close guide", {item.title for item in generate_training_resources(employee)})

    def test_other_values_use_defaults(self) -> None:
        """Unknown Other values should receive fallback content without empty sections."""
        employee = EmployeeForm(
            "Riley Morgan", "Other", "Other", "2026-12-15", "Astronaut", "Research Lab"
        )
        self.assert_complete_pack(employee, "Astronaut", "Research Lab")
        self.assertEqual(len(generate_it_access_checklist(employee)), 5)
        self.assertIn("Role overview", {item.title for item in generate_training_resources(employee)})
        self.assertIn("What should I know about my department?", {item.question for item in generate_faqs(employee)})
        self.assertIn("What should I focus on in my role?", {item.question for item in generate_faqs(employee)})


if __name__ == "__main__":
    unittest.main()

