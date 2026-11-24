"""Rule-based role and department content used by the onboarding service."""

from models import ChecklistItem, FaqItem, TrainingResource


ROLE_OPTIONS: tuple[str, ...] = (
    "Software Engineer", "Product Manager", "Accountant", "HR Manager",
    "Sales Representative", "Marketing Specialist", "Other",
)
DEPARTMENT_OPTIONS: tuple[str, ...] = (
    "Engineering", "Human Resources", "Finance", "Sales", "Marketing", "Operations", "Other",
)
DEFAULT_ROLE: str = "Team Member"
DEFAULT_DEPARTMENT: str = "General"

DEFAULT_DOCUMENTS: tuple[ChecklistItem, ...] = (
    ChecklistItem("Government-issued identity document", "Provide the document through the approved HR process."),
    ChecklistItem("Tax and payroll forms", "Complete the forms requested by the People team."),
    ChecklistItem("Bank details for payroll", "Use the secure payroll portal to add payment details."),
    ChecklistItem("Signed offer and employment agreement", "Confirm that the signed copies are on file."),
    ChecklistItem("Emergency contact details", "Add a current contact in the HR portal."),
)

BASELINE_IT_ACCESS: tuple[ChecklistItem, ...] = (
    ChecklistItem("Company email", "Confirm sign-in and multi-factor authentication."),
    ChecklistItem("VPN", "Connect from an approved network when working remotely."),
    ChecklistItem("HR portal", "Review your profile, policies, and payroll tasks."),
    ChecklistItem("Slack or Teams", "Join your team workspace and key channels."),
)
DEPARTMENT_IT_ACCESS: dict[str, tuple[ChecklistItem, ...]] = {
    "Engineering": (
        ChecklistItem("GitHub", "Request access to the repositories used by your team."),
        ChecklistItem("Jira", "Join the engineering project boards."),
        ChecklistItem("Cloud console", "Request only the approved role and environment access."),
    ),
    "Human Resources": (
        ChecklistItem("HRIS", "Confirm the people-system permissions required for your role."),
        ChecklistItem("Payroll system", "Use role-approved access for payroll tasks."),
    ),
    "Finance": (
        ChecklistItem("ERP", "Request access to the finance modules you need."),
        ChecklistItem("Accounting tools", "Confirm your ledger and reporting permissions."),
    ),
    "Sales": (ChecklistItem("CRM", "Join the correct sales team and territory."),),
    "Marketing": (
        ChecklistItem("Analytics tools", "Request access to approved reporting dashboards."),
        ChecklistItem("Design tools", "Join the team's shared design workspace."),
    ),
}
DEFAULT_DEPARTMENT_IT_ACCESS: tuple[ChecklistItem, ...] = (
    ChecklistItem("Department workspace", "Ask your manager which shared tools are needed."),
)

DAY_THEMES: tuple[str, ...] = (
    "Welcome and setup", "People and processes", "Tools and ways of working",
    "Role foundations", "First contribution", "Feedback and collaboration", "Review and next steps",
)

DEPARTMENT_PLAN_ACTIVITIES: dict[str, tuple[tuple[str, ...], ...]] = {
    "Engineering": (
        ("Meet your engineering manager and team", "Set up your development environment", "Review the engineering handbook"),
        ("Meet your onboarding buddy", "Explore the service map", "Review the team's code review practices"),
        ("Walk through GitHub, Jira, and team chat", "Review the release process", "Learn how incidents are escalated"),
        ("Trace a request through the product", "Review the system architecture", "Discuss your team's quality standards"),
        ("Choose a small starter issue", "Pair with a teammate", "Submit a draft change for feedback"),
        ("Join a design or planning discussion", "Review feedback with your buddy", "Learn how engineering decisions are recorded"),
        ("Demo what you learned", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
    ),
    "Human Resources": (
        ("Meet your People team and manager", "Review the employee lifecycle", "Read the HR service guide"),
        ("Meet your onboarding buddy", "Explore the HRIS", "Review privacy and record-handling practices"),
        ("Walk through the HRIS and payroll workflows", "Review request routing", "Learn the escalation path for employee questions"),
        ("Review a sample employee journey", "Discuss policy ownership", "Learn how HR cases are documented"),
        ("Complete a supervised starter task", "Shadow a colleague", "Review your work with your manager"),
        ("Join a people-program discussion", "Review feedback with your buddy", "Explore cross-functional HR partnerships"),
        ("Summarize key workflows", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
    ),
    "Finance": (
        ("Meet your finance team and manager", "Review the finance calendar", "Read the controls overview"),
        ("Meet your onboarding buddy", "Explore the ERP environment", "Review approval and documentation standards"),
        ("Walk through accounting tools", "Review close and reporting workflows", "Learn how finance requests are escalated"),
        ("Trace a sample transaction", "Discuss reconciliation practices", "Review data access expectations"),
        ("Complete a supervised starter task", "Shadow a colleague", "Review your work with your manager"),
        ("Join a planning or close discussion", "Review feedback with your buddy", "Explore finance partnerships across teams"),
        ("Summarize key controls", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
    ),
    "Sales": (
        ("Meet your sales team and manager", "Review the sales process", "Read the territory overview"),
        ("Meet your onboarding buddy", "Explore the CRM", "Review customer communication guidelines"),
        ("Walk through pipeline and forecasting", "Review product positioning", "Learn how sales support is requested"),
        ("Listen to a customer conversation", "Practice a product overview", "Discuss qualification and handoff practices"),
        ("Prepare a supervised account brief", "Shadow a teammate", "Review your notes with your manager"),
        ("Join a pipeline discussion", "Review feedback with your buddy", "Explore cross-functional customer partnerships"),
        ("Summarize the sales workflow", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
    ),
    "Marketing": (
        ("Meet your marketing team and manager", "Review the campaign calendar", "Read the brand guidelines"),
        ("Meet your onboarding buddy", "Explore analytics dashboards", "Review the content approval process"),
        ("Walk through design and publishing tools", "Review campaign measurement", "Learn how creative requests are prioritized"),
        ("Review a recent campaign", "Discuss audience and channel strategy", "Explore asset management practices"),
        ("Draft a supervised content brief", "Shadow a teammate", "Review your work with your manager"),
        ("Join a campaign planning discussion", "Review feedback with your buddy", "Explore cross-functional marketing partnerships"),
        ("Summarize campaign workflows", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
    ),
}
DEFAULT_DEPARTMENT_PLAN_ACTIVITIES: tuple[tuple[str, ...], ...] = (
    ("Meet your manager and team", "Set up your workspace", "Read the company overview"),
    ("Meet your onboarding buddy", "Review team processes", "Learn where to find help"),
    ("Explore your team's tools", "Review communication norms", "Learn the escalation path"),
    ("Discuss your role's core responsibilities", "Observe a typical workflow", "Review quality expectations"),
    ("Choose a supervised starter task", "Shadow a teammate", "Review your work with your manager"),
    ("Join a team discussion", "Review feedback with your buddy", "Explore cross-functional partnerships"),
    ("Summarize what you learned", "Agree on a first-month goal", "Plan follow-up learning with your manager"),
)
ROLE_PLAN_ACTIVITIES: dict[str, tuple[str, ...]] = {
    "Software Engineer": (
        "Review the team's development workflow", "Discuss code review expectations", "Explore how changes reach production",
        "Learn how the team tests software", "Select a small code change", "Discuss technical growth goals", "Identify a first engineering milestone",
    ),
    "Accountant": (
        "Review accounting responsibilities", "Discuss documentation standards", "Explore the reporting calendar",
        "Learn the reconciliation process", "Select a supervised accounting task", "Discuss professional development goals", "Identify a first finance milestone",
    ),
    "Product Manager": (
        "Review product responsibilities", "Discuss customer discovery practices", "Explore roadmap decision records",
        "Learn the team's prioritization approach", "Select a small discovery or documentation task", "Discuss product growth goals", "Identify a first product milestone",
    ),
    "HR Manager": (
        "Review people leadership responsibilities", "Discuss employee support practices", "Explore HR policy ownership",
        "Learn the people program calendar", "Select a supervised process improvement task", "Discuss people leadership goals", "Identify a first HR milestone",
    ),
    "Sales Representative": (
        "Review territory responsibilities", "Discuss qualification and discovery", "Explore customer account planning",
        "Learn the sales stages and handoffs", "Prepare a supervised account brief", "Discuss customer relationship goals", "Identify a first sales milestone",
    ),
    "Marketing Specialist": (
        "Review campaign responsibilities", "Discuss audience and channel planning", "Explore the brand toolkit",
        "Learn the campaign measurement approach", "Draft a supervised content brief", "Discuss marketing growth goals", "Identify a first campaign milestone",
    ),
}
DEFAULT_ROLE_PLAN_ACTIVITIES: tuple[str, ...] = (
    "Review your role responsibilities", "Discuss success measures for your role", "Identify a useful first contribution",
    "Review role-specific learning materials", "Select a supervised starter task", "Discuss professional development goals", "Identify a first role milestone",
)

DEFAULT_FAQS: tuple[FaqItem, ...] = (
    FaqItem("Who should I contact with questions?", "Start with your manager or onboarding buddy. They can connect you with the right team."),
    FaqItem("Where can I find company policies?", "The HR portal links to current policies and employee guidance."),
    FaqItem("How do I get help with a system?", "Contact your manager or the service desk and include the system name and a short description."),
    FaqItem("How will I receive my first assignments?", "Your manager will agree on priorities with you and explain how the team tracks work."),
    FaqItem("When will I meet the rest of my team?", "Your manager will arrange introductions and invite you to relevant team meetings."),
    FaqItem("How do I share feedback about onboarding?", "You can raise feedback with your manager, buddy, or the People team at any time."),
    FaqItem("What should I focus on in my first month?", "Learn the team's workflows, complete required training, and agree on a practical first-month goal."),
)
DEFAULT_DEPARTMENT_FAQ: FaqItem = FaqItem("What should I know about my department?", "Your manager will explain the department's priorities, tools, and ways of working.")
DEPARTMENT_FAQS: dict[str, FaqItem] = {
    "Engineering": FaqItem("How are engineering changes reviewed?", "Use the team's code review process and ask a teammate to help with your first change."),
    "Human Resources": FaqItem("How should employee information be handled?", "Use approved HR systems and follow the privacy and access guidance for every record."),
    "Finance": FaqItem("Where can I find finance controls?", "Review the finance controls guide and confirm approval steps with your manager."),
    "Sales": FaqItem("Where can I find account information?", "Use the CRM as the source of truth and follow customer data handling guidance."),
    "Marketing": FaqItem("Where can I find brand and campaign guidance?", "Use the current brand guide and campaign workspace linked by your team."),
}
DEFAULT_ROLE_FAQ: FaqItem = FaqItem("What should I focus on in my role?", "Ask your manager to identify the first skills, workflows, and outcomes to learn for your role.")
ROLE_FAQS: dict[str, FaqItem] = {
    "Software Engineer": FaqItem("What is a good first task for a software engineer?", "Your manager or buddy can help choose a small, well-scoped change with a clear review path."),
    "Accountant": FaqItem("What is a good first task for an accountant?", "Start with a supervised task that introduces the team's documentation and review practices."),
    "Product Manager": FaqItem("How does a product manager learn the roadmap?", "Review the team's roadmap and discuss customer priorities and decision records with your manager."),
    "HR Manager": FaqItem("How does an HR manager learn local processes?", "Review the current People team guidance and confirm process owners with your manager."),
    "Sales Representative": FaqItem("How does a sales representative learn the territory?", "Review your territory and account notes with your manager before contacting customers."),
    "Marketing Specialist": FaqItem("How does a marketing specialist learn campaign priorities?", "Review the campaign calendar and ask your team about current briefs and approval steps."),
}

DEFAULT_ROLE_TRAINING: tuple[TrainingResource, ...] = (
    TrainingResource("Role overview", "Ask your manager for the team's current role guide and success measures.", "Role learning"),
    TrainingResource("Team workflow walkthrough", "Shadow a teammate and capture questions about the day-to-day workflow.", "Role learning"),
)
ROLE_TRAINING: dict[str, tuple[TrainingResource, ...]] = {
    "Software Engineer": (
        TrainingResource("Development workflow guide", "Read the repository, review, testing, and release guidance for your team.", "Role learning"),
        TrainingResource("Service architecture overview", "Use the team's service map and architecture notes as a guided reading session.", "Role learning"),
    ),
    "Product Manager": (
        TrainingResource("Product discovery guide", "Review the team's customer research and prioritization practices.", "Role learning"),
        TrainingResource("Roadmap and decision records", "Read current roadmap context and examples of product decisions.", "Role learning"),
    ),
    "Accountant": (
        TrainingResource("Accounting close guide", "Review the close calendar, reconciliations, and supporting documentation.", "Role learning"),
        TrainingResource("Finance reporting handbook", "Read the team's reporting definitions and review standards.", "Role learning"),
    ),
    "HR Manager": (
        TrainingResource("People operations guide", "Review employee lifecycle workflows and process ownership.", "Role learning"),
        TrainingResource("HRIS and case handling guide", "Read approved system and employee case handling practices.", "Role learning"),
    ),
    "Sales Representative": (
        TrainingResource("Sales methodology overview", "Review the sales stages, qualification approach, and handoff expectations.", "Role learning"),
        TrainingResource("Product and customer guide", "Read current product positioning and customer materials.", "Role learning"),
    ),
    "Marketing Specialist": (
        TrainingResource("Campaign planning guide", "Review briefs, channel planning, and campaign measurement practices.", "Role learning"),
        TrainingResource("Brand and content guide", "Read current brand guidance and content approval workflows.", "Role learning"),
    ),
}
COMPULSORY_TRAINING: tuple[TrainingResource, ...] = (
    TrainingResource("Security awareness", "Complete the required security and data protection course.", "Compulsory"),
    TrainingResource("Compliance essentials", "Complete the required compliance and workplace policy course.", "Compulsory"),
    TrainingResource("Code of conduct", "Read and acknowledge the company's code of conduct.", "Compulsory"),
)



