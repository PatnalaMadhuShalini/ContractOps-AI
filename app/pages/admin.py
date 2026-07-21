import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.auth_state import AuthState, PLAN_ORDER


def _plan_pill(plan: str) -> rx.Component:
    return rx.el.span(
        plan,
        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
    )


def _status_pill(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "active",
            rx.el.span(
                rx.el.span(
                    class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                ),
                "Active",
                class_name="inline-flex items-center gap-1.5 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
        ),
        (
            "trialing",
            rx.el.span(
                "Trial",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
            ),
        ),
        rx.el.span(
            "Suspended",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
        ),
    )


def _role_pill(role: str) -> rx.Component:
    return rx.match(
        role,
        (
            "platform_admin",
            rx.el.span(
                "Platform admin",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
            ),
        ),
        (
            "owner",
            rx.el.span(
                "Owner",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
        ),
        (
            "admin",
            rx.el.span(
                "Admin",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-violet-50 text-violet-700",
            ),
        ),
        rx.el.span(
            "Member",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
        ),
    )


def _company_row(c: dict) -> rx.Component:
    usage_pct = (
        c["contracts_reviewed"].to(int) * 100 / c["contracts_limit"].to(int)
    ).to(int)
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("building-2", class_name="h-4 w-4 text-blue-600"),
                    class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        c["name"],
                        class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        f"{c['domain']} · created {c['created']}",
                        class_name="text-[11.5px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(_plan_pill(c["plan"]), class_name="px-4 py-3 align-middle"),
        rx.el.td(
            _status_pill(c["status"]), class_name="px-4 py-3 align-middle"
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("users", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.p(
                    c["users"].to_string()
                    + " / "
                    + c["seats_limit"].to_string(),
                    class_name="text-[12.5px] font-semibold text-gray-900",
                ),
                class_name="inline-flex items-center gap-1.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        c["contracts_reviewed"].to_string()
                        + " / "
                        + c["contracts_limit"].to_string(),
                        class_name="text-[12px] font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        usage_pct.to_string() + "%",
                        class_name="ml-auto text-[11px] font-medium text-gray-500",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name=rx.cond(
                            usage_pct < 80,
                            "h-full bg-blue-600 rounded-full",
                            rx.cond(
                                usage_pct < 100,
                                "h-full bg-amber-500 rounded-full",
                                "h-full bg-red-500 rounded-full",
                            ),
                        ),
                        style={"width": usage_pct.to_string() + "%"},
                    ),
                    class_name="mt-1 h-1.5 w-32 rounded-full bg-gray-100 overflow-hidden",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            AuthState.plan_options,
                            lambda p: rx.el.option(p, value=p),
                        ),
                        default_value=c["plan"].to(str),
                        key=c["plan"].to(str),
                        on_change=lambda v: AuthState.admin_change_plan(
                            c["id"], v
                        ),
                        class_name="h-8 pl-2 pr-7 rounded-md border border-gray-200 bg-white text-[12px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                rx.el.button(
                    rx.cond(
                        c["status"] == "suspended", "Reactivate", "Suspend"
                    ),
                    on_click=lambda: AuthState.admin_toggle_status(c["id"]),
                    class_name=rx.cond(
                        c["status"] == "suspended",
                        "inline-flex items-center h-8 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-emerald-700 hover:bg-emerald-50 hover:border-emerald-200 transition-colors",
                        "inline-flex items-center h-8 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                    ),
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _companies_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Companies",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Every workspace on the platform",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Company", class_name=header_cls),
                        rx.el.th("Plan", class_name=header_cls),
                        rx.el.th("Status", class_name=header_cls),
                        rx.el.th("Seats", class_name=header_cls),
                        rx.el.th("Usage", class_name=header_cls),
                        rx.el.th("Actions", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(AuthState.admin_companies, _company_row)
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _user_row(u: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        u["initials"],
                        class_name="text-[10.5px] font-semibold text-blue-700",
                    ),
                    class_name="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        u["name"],
                        class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        u["email"],
                        class_name="text-[11.5px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                u["company"],
                class_name="text-[12.5px] font-medium text-gray-800",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(_role_pill(u["role"]), class_name="px-4 py-3 align-middle"),
        rx.el.td(
            rx.el.p(
                u["last_active"],
                class_name="text-[12px] text-gray-600",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _users_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "All users",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Every user across every workspace",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("User", class_name=header_cls),
                        rx.el.th("Workspace", class_name=header_cls),
                        rx.el.th("Role", class_name=header_cls),
                        rx.el.th("Last active", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(rx.foreach(AuthState.admin_users, _user_row)),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _header_actions() -> rx.Component:
    return rx.el.button(
        rx.icon("log-out", class_name="h-3.5 w-3.5"),
        "Sign out",
        on_click=AuthState.logout,
        class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
    )


def admin_page() -> rx.Component:
    return page_shell(
        "admin",
        rx.el.div(
            page_header(
                "Platform admin",
                "Oversee every workspace, monitor usage across the platform, and manage plans.",
                _header_actions(),
            ),
            rx.el.div(
                stat_card(
                    "Companies",
                    AuthState.admin_stats["companies"].to_string(),
                    "Active workspaces on the platform",
                    "building-2",
                ),
                stat_card(
                    "Users",
                    AuthState.admin_stats["users"].to_string(),
                    "Total registered users",
                    "users",
                ),
                stat_card(
                    "Contracts reviewed",
                    AuthState.admin_stats["contracts"].to_string(),
                    "Aggregate this cycle",
                    "file-check-2",
                ),
                stat_card(
                    "Pending invites",
                    AuthState.admin_stats["invites"].to_string(),
                    "Awaiting acceptance",
                    "mail",
                ),
                class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
            ),
            _companies_table(),
            rx.el.div(_users_table(), class_name="mt-4"),
        ),
    )
