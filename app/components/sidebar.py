import reflex as rx
from app.states.auth_state import AuthState


def _side_item(
    icon: str, label: str, href: str, active: bool = False
) -> rx.Component:
    base = "flex items-center gap-2.5 h-8 px-2.5 rounded-md text-[13px] font-medium transition-colors"
    if active:
        cls = f"{base} bg-blue-50 text-blue-700"
    else:
        cls = f"{base} text-gray-600 hover:bg-gray-100 hover:text-gray-900"
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label),
        href=href,
        class_name=cls,
    )


def _section_label(text: str) -> rx.Component:
    return rx.el.p(
        text,
        class_name="px-2.5 pt-4 pb-1.5 text-[11px] font-semibold uppercase tracking-wider text-gray-400",
    )


def _auth_items(active: str) -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.div(
            _section_label("Account"),
            _side_item(
                "layout-grid",
                "Workspace",
                "/workspace",
                active=active == "workspace",
            ),
            _side_item(
                "wallet",
                "Billing",
                "/billing",
                active=active == "billing",
            ),
            rx.cond(
                AuthState.is_platform_admin,
                rx.el.div(
                    _side_item(
                        "shield-check",
                        "Platform admin",
                        "/admin",
                        active=active == "admin",
                    ),
                    _side_item(
                        "receipt-indian-rupee",
                        "Billing ops",
                        "/admin/billing",
                        active=active == "admin_billing",
                    ),
                    _side_item(
                        "contact-round",
                        "Sales & CRM",
                        "/leads",
                        active=active == "leads",
                    ),
                    class_name="flex flex-col gap-0.5",
                ),
                rx.fragment(),
            ),
            _side_item(
                "settings",
                "Settings",
                "/settings",
                active=active == "settings",
            ),
            _side_item(
                "circle-help",
                "Help",
                "/settings#help",
                active=active == "help",
            ),
            class_name="flex flex-col gap-0.5",
        ),
        rx.el.div(
            _section_label("Account"),
            _side_item(
                "log-in",
                "Sign in",
                "/login",
                active=active == "login",
            ),
            _side_item(
                "user-plus",
                "Create workspace",
                "/signup",
                active=active == "signup",
            ),
            _side_item(
                "settings",
                "Settings",
                "/settings",
                active=active == "settings",
            ),
            class_name="flex flex-col gap-0.5",
        ),
    )


def _user_card() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.a(
            rx.el.div(
                rx.el.p(
                    AuthState.current_user["initials"],
                    class_name="text-[11px] font-semibold text-blue-700",
                ),
                class_name="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.p(
                    AuthState.current_user["name"],
                    class_name="text-[13px] font-medium text-gray-900 leading-tight truncate",
                ),
                rx.el.p(
                    rx.cond(
                        AuthState.is_platform_admin,
                        "Platform admin",
                        AuthState.current_company["name"],
                    ),
                    class_name="text-[11px] text-gray-500 leading-tight truncate",
                ),
                class_name="flex flex-col min-w-0",
            ),
            href=rx.cond(AuthState.is_platform_admin, "/admin", "/workspace"),
            class_name="flex items-center gap-2.5 px-2.5 py-2.5 rounded-md hover:bg-gray-100 transition-colors cursor-pointer",
        ),
        rx.el.a(
            rx.el.div(
                rx.icon("log-in", class_name="h-4 w-4 text-gray-500"),
                class_name="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.p(
                    "Sign in",
                    class_name="text-[13px] font-medium text-gray-900 leading-tight",
                ),
                rx.el.p(
                    "or create a workspace",
                    class_name="text-[11px] text-gray-500 leading-tight",
                ),
                class_name="flex flex-col min-w-0",
            ),
            href="/login",
            class_name="flex items-center gap-2.5 px-2.5 py-2.5 rounded-md hover:bg-gray-100 transition-colors cursor-pointer",
        ),
    )


def sidebar(active: str = "home") -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-check-2", class_name="h-3.5 w-3.5 text-white"
                    ),
                    class_name="h-6 w-6 rounded bg-blue-600 flex items-center justify-center",
                ),
                rx.el.span(
                    "ContractOps",
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-2 px-2.5 h-12",
            ),
            rx.el.div(
                _section_label("Overview"),
                _side_item("home", "Home", "/", active=active == "home"),
                _side_item(
                    "layout-dashboard",
                    "Dashboard",
                    "/review",
                    active=active == "dashboard",
                ),
                _section_label("Workflow"),
                _side_item(
                    "file-text",
                    "Contracts",
                    "/review",
                    active=active == "contracts",
                ),
                _side_item(
                    "shield-check",
                    "Approvals",
                    "/approvals",
                    active=active == "approvals",
                ),
                _side_item(
                    "library",
                    "Clause library",
                    "/clauses",
                    active=active == "clauses",
                ),
                _section_label("Insights"),
                _side_item(
                    "chart-line",
                    "Analytics",
                    "/analytics",
                    active=active == "analytics",
                ),
                _side_item(
                    "bell",
                    "Alerts",
                    "/settings#notifications",
                    active=active == "alerts",
                ),
                _auth_items(active),
                class_name="flex flex-col gap-0.5 px-2 pb-4",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            _user_card(),
            class_name="px-2 py-2 border-t border-gray-200",
        ),
        class_name="hidden lg:flex flex-col justify-between w-60 shrink-0 border-r border-gray-200 bg-white h-[calc(100vh-3.5rem)] sticky top-14",
    )
