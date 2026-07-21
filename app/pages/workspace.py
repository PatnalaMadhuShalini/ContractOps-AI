import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.auth_state import AuthState, PLAN_ORDER


def _role_pill(role: str) -> rx.Component:
    return rx.match(
        role,
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
        rx.el.span(
            "Invited",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
        ),
    )


def _plan_pill(plan: str) -> rx.Component:
    return rx.el.span(
        plan,
        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
    )


def _plan_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Current plan",
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_company["plan"],
                        class_name="text-3xl font-semibold tracking-tight text-gray-900 leading-none",
                    ),
                    _plan_pill(AuthState.current_company["status"]),
                    class_name="mt-2 flex items-center gap-2",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.foreach(
                    AuthState.plan_options,
                    lambda p: rx.el.button(
                        p,
                        on_click=lambda: AuthState.change_plan(p),
                        class_name=rx.cond(
                            AuthState.current_company["plan"] == p,
                            "h-8 px-3 rounded-md bg-blue-600 text-[12px] font-semibold text-white",
                            "h-8 px-3 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                        ),
                    ),
                ),
                class_name="ml-auto flex items-center gap-1.5",
            ),
            class_name="flex items-center gap-2 flex-wrap",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Contracts reviewed",
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    AuthState.current_company["contracts_reviewed"].to_string()
                    + " / "
                    + AuthState.contracts_limit.to_string(),
                    class_name="ml-auto text-[12.5px] font-semibold text-gray-900",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        AuthState.usage_percent < 80,
                        "h-full bg-blue-600 rounded-full transition-all",
                        rx.cond(
                            AuthState.usage_percent < 100,
                            "h-full bg-amber-500 rounded-full transition-all",
                            "h-full bg-red-500 rounded-full transition-all",
                        ),
                    ),
                    style={"width": AuthState.usage_percent.to_string() + "%"},
                ),
                class_name="mt-2 h-1.5 w-full rounded-full bg-gray-100 overflow-hidden",
            ),
            rx.el.p(
                AuthState.contracts_remaining.to_string()
                + " remaining this cycle",
                class_name="mt-2 text-[11.5px] text-gray-500",
            ),
            class_name="mt-5 pt-5 border-t border-gray-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Seats used",
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    AuthState.seats_used.to_string()
                    + " / "
                    + AuthState.seats_limit.to_string(),
                    class_name="ml-auto text-[12.5px] font-semibold text-gray-900",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        AuthState.seats_percent < 80,
                        "h-full bg-blue-600 rounded-full transition-all",
                        rx.cond(
                            AuthState.seats_percent < 100,
                            "h-full bg-amber-500 rounded-full transition-all",
                            "h-full bg-red-500 rounded-full transition-all",
                        ),
                    ),
                    style={"width": AuthState.seats_percent.to_string() + "%"},
                ),
                class_name="mt-2 h-1.5 w-full rounded-full bg-gray-100 overflow-hidden",
            ),
            class_name="mt-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("sparkles", class_name="h-3.5 w-3.5"),
                    "Simulate contract review",
                    on_click=AuthState.increment_usage,
                    class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
                ),
                rx.el.a(
                    rx.icon("wallet", class_name="h-3.5 w-3.5"),
                    "Manage billing",
                    href="/billing",
                    class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md bg-blue-600 text-[12.5px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                class_name="flex items-center gap-2 flex-wrap",
            ),
            rx.el.p(
                "Pay via UPI, NEFT/RTGS or cheque. Request GST invoices and plan changes from the billing page.",
                class_name="text-[11.5px] text-gray-500",
            ),
            class_name="mt-5 pt-5 border-t border-gray-100 flex items-center justify-between gap-3 flex-wrap",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def _invite_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Invite by email",
                    class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.input(
                    name="email",
                    type="email",
                    placeholder="teammate@company.com",
                    required=True,
                    class_name="h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                ),
                class_name="flex flex-col flex-1 min-w-[220px]",
            ),
            rx.el.div(
                rx.el.label(
                    "Role",
                    class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Member", value="member"),
                        rx.el.option("Admin", value="admin"),
                        name="role",
                        default_value="member",
                        class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex flex-col w-32",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-3.5 w-3.5"),
                "Send invite",
                type="submit",
                class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors self-end",
            ),
            class_name="flex items-end gap-2 flex-wrap",
        ),
        rx.cond(
            AuthState.invite_error != "",
            rx.el.p(
                AuthState.invite_error,
                class_name="mt-2 text-[12px] text-red-600",
            ),
            rx.fragment(),
        ),
        on_submit=AuthState.invite_user,
        reset_on_submit=True,
    )


def _member_row(u: dict) -> rx.Component:
    return rx.el.div(
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
            class_name="flex items-center gap-3 min-w-0 flex-1",
        ),
        rx.el.div(
            _role_pill(u["role"]),
            _status_pill(u["status"]),
            rx.el.p(
                u["last_active"],
                class_name="hidden md:block text-[11.5px] text-gray-500 w-24 text-right",
            ),
            rx.cond(
                (u["role"] != "owner") & AuthState.can_manage_company,
                rx.el.button(
                    "Remove",
                    on_click=lambda: AuthState.remove_user(u["id"]),
                    class_name="inline-flex items-center h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[11.5px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center gap-2 shrink-0",
        ),
        class_name="flex items-center gap-3 p-3 border-b border-gray-100 last:border-b-0",
    )


def _invite_row(inv: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("mail", class_name="h-4 w-4 text-gray-500 shrink-0"),
            rx.el.div(
                rx.el.p(
                    inv["email"],
                    class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    "Invited by " + inv["invited_by"] + " · " + inv["created"],
                    class_name="text-[11.5px] text-gray-500 leading-tight",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0 flex-1",
        ),
        rx.el.div(
            _role_pill(inv["role"]),
            rx.el.button(
                "Resend",
                on_click=lambda: AuthState.resend_invite(inv["id"]),
                class_name="inline-flex items-center h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[11.5px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
            ),
            rx.el.button(
                "Revoke",
                on_click=lambda: AuthState.revoke_invite(inv["id"]),
                class_name="inline-flex items-center h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[11.5px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
            ),
            class_name="flex items-center gap-1.5 shrink-0",
        ),
        class_name="flex items-center gap-3 p-3 border-b border-gray-100 last:border-b-0",
    )


def _members_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Team",
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    AuthState.company_users.length().to_string() + " active",
                    class_name="text-[11.5px] text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center px-4 h-12 border-b border-gray-100",
        ),
        rx.el.div(
            rx.foreach(AuthState.company_users, _member_row),
            class_name="flex flex-col",
        ),
        rx.cond(
            AuthState.company_invites.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Pending invites",
                        class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                    rx.el.span(
                        AuthState.company_invites.length().to_string(),
                        class_name="ml-auto inline-flex items-center h-5 px-1.5 rounded bg-amber-50 text-amber-700 text-[10.5px] font-semibold",
                    ),
                    class_name="flex items-center px-4 h-9 border-t border-b border-gray-100 bg-gray-50/60",
                ),
                rx.el.div(
                    rx.foreach(AuthState.company_invites, _invite_row),
                    class_name="flex flex-col",
                ),
            ),
            rx.fragment(),
        ),
        rx.cond(
            AuthState.can_manage_company,
            rx.el.div(
                _invite_form(),
                class_name="p-4 border-t border-gray-100 bg-gray-50/40",
            ),
            rx.fragment(),
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _workspace_meta() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Workspace details",
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Workspace",
                    class_name="text-[11px] font-medium text-gray-500",
                ),
                rx.el.p(
                    AuthState.current_company["name"],
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    "Domain", class_name="text-[11px] font-medium text-gray-500"
                ),
                rx.el.p(
                    AuthState.current_company["domain"],
                    class_name="text-[13px] font-medium text-gray-900",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    "Created",
                    class_name="text-[11px] font-medium text-gray-500",
                ),
                rx.el.p(
                    AuthState.current_company["created"],
                    class_name="text-[13px] font-medium text-gray-900",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    "Your role",
                    class_name="text-[11px] font-medium text-gray-500",
                ),
                rx.el.div(
                    _role_pill(AuthState.current_user["role"]),
                    class_name="mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            class_name="grid grid-cols-2 gap-3",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            "Go to contracts",
            rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
            href="/review",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        rx.el.button(
            rx.icon("log-out", class_name="h-3.5 w-3.5"),
            "Sign out",
            on_click=AuthState.logout,
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        class_name="flex items-center gap-2",
    )


def workspace_page() -> rx.Component:
    return page_shell(
        "workspace",
        rx.el.div(
            page_header(
                "Workspace",
                "Manage your team, monitor plan usage, and control who has access.",
                _header_actions(),
            ),
            rx.el.div(
                stat_card(
                    "Contracts this cycle",
                    AuthState.current_company["contracts_reviewed"].to_string(),
                    "of "
                    + AuthState.contracts_limit.to_string()
                    + " on the "
                    + AuthState.current_company["plan"]
                    + " plan",
                    "file-check-2",
                ),
                stat_card(
                    "Seats used",
                    AuthState.seats_used.to_string(),
                    "of "
                    + AuthState.seats_limit.to_string()
                    + " available seats",
                    "users",
                ),
                stat_card(
                    "Pending invites",
                    AuthState.company_invites.length().to_string(),
                    "Awaiting sign-up",
                    "mail",
                ),
                stat_card(
                    "Plan",
                    AuthState.current_company["plan"],
                    "Workspace status: " + AuthState.current_company["status"],
                    "badge-check",
                ),
                class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
            ),
            rx.el.div(
                rx.el.div(_plan_card(), class_name="lg:col-span-7"),
                rx.el.div(_workspace_meta(), class_name="lg:col-span-5"),
                class_name="grid grid-cols-1 lg:grid-cols-12 gap-4",
            ),
            rx.el.div(
                _members_card(),
                class_name="mt-4",
            ),
        ),
    )
